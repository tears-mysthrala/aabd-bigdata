"""Genera CNC_Guard.ipynb (fuente versionada) desde celdas declaradas aquí."""

import nbformat as nbf

MD = []
CODE = []


def md(src):
    MD.append(("markdown", src))


def code(src):
    MD.append(("code", src))


md("""# CNC Guard — Erronka 1: mantentze prediktiboa (analisia, ez prototipo hutsa)

**Helburua**: sentsore-fusio lausoa + anomalia-detektzioa, `cnc_10M.csv`-rekin (10M errenkada).
**Muga zintzoa**: datu sintetikoak dira (seed 42); %85 akats zarata purua da → F1-ren sabaia
datuena da, ez kodearena. Ez da balio industrialik, ez konektore errealik (OPC-UA/MQTT extrak gabe).""")

code("""from pathlib import Path
import os
import numpy as np
import pandas as pd

# Datu-resoluzioa: env > repo erlatiboa > errorea argia
def resolver_datos() -> Path:
    if os.environ.get("CNC_DATA"):
        p = Path(os.environ["CNC_DATA"])
        if p.is_file():
            return p
    root = Path.cwd()
    for base in (root, root.parent, root.parent.parent):
        p = base / "04_Programazioa_5073" / "data" / "cnc_10M.csv"
        if p.is_file():
            return p.resolve()
    p = Path("/home/tears/bigdata/04_Programazioa_5073/data/cnc_10M.csv")
    if p.is_file():
        return p
    raise FileNotFoundError(
        "Falta cnc_10M.csv: genéralo con 04_Programazioa_5073/data/generar_cnc_10M.py"
    )

DATA = resolver_datos()
print("DATA:", DATA)
assert DATA.stat().st_size > 100_000_000, "CSV oso txikia: birsortu?"
""")

md("""## 1. EDA (200k lagina, interaktiboa)

Egitura `X (n×p)` + `y`: ezaugarriak tenperatura/bibrazioa/presioa/makina, etiketa errorea.""")

code("""SAMPLE = 200_000
df = pd.read_csv(DATA, nrows=SAMPLE)
print(df.shape)
print(df.dtypes.to_string())
print(df.describe().to_string())
print("missing:\\n", df.isna().sum().to_string())
print("errorea:\\n", df["errorea"].value_counts(normalize=True).to_string())
print("korrelazioa:\\n", df[["tenperatura", "bibrazioa", "presioa"]].corr().round(3).to_string())
assert len(df) == SAMPLE and set(df.columns) == {"ts", "makina_id", "tenperatura", "bibrazioa", "presioa", "errorea"}
""")

md("""## 2. Sistema difuso (Ebazpena §3 → `src/cnc_guard/fuzzy.py`)

Tenperatura × bibrazioa × higadura (proxy: `txv` normalizatua) → arriskua [0, 100].
Mamdani MIN/MAX + zentroidea, numpy hutsez.""")

code("""from cnc_guard.fuzzy import riesgo, fuzzify, infer

# Adibide crisp (mahaiko baliozkotzea):
for t, v, w in [(52, 0.5, 0.05), (68, 3.5, 0.55), (90, 7.0, 0.9)]:
    print(f"T={t} V={v} W={w} -> riesgo={riesgo(t, v, w):.1f}")
assert riesgo(52, 0.5, 0.05) < 30 < riesgo(90, 7.0, 0.9)

# Banaketa 2k laginean (begizta eskalarra demo-tamainan):
sub = df.sample(2000, random_state=1).reset_index(drop=True)
txv = sub["tenperatura"] * sub["bibrazioa"]
wear = ((txv - txv.min()) / (txv.max() - txv.min())).clip(0, 1)
risks = np.array([riesgo(t, v, w) for t, v, w in zip(sub["tenperatura"], sub["bibrazioa"], wear)])
print(f"fuzzy 2k: media={risks.mean():.1f} p95={np.percentile(risks, 95):.1f} max={risks.max():.1f}")
assert risks.max() > 60, "muturreko kasurik gabe?"
""")

md("""## 3. Anomalías: IsolationForest (500k train, `src/cnc_guard/anomaly.py`)

Ezaugarriak + ingeniaritza (`txv`, `t2`): eredu linealak AND-eskualdea ezin duenez,
nahaste-matrizeak erakusten du zergatik.""")

code("""from cnc_guard.anomaly import build_features, fit_anomaly, anomaly_score

traint = pd.read_csv(DATA, nrows=500_000)
Xtr = build_features(traint)
model, scaler, dmin, dmax = fit_anomaly(Xtr, contamination=0.012, seed=42)
str_ = f"train 500k: decision<0 tasa={(model.decision_function(scaler.transform(Xtr)) < 0).mean():.4f}"
print(str_)
assert 0.005 < float((model.decision_function(scaler.transform(Xtr)) < 0).mean()) < 0.05
# Eskala globala fusiorako (ez holdout-lokala):
TXV_MIN = float((traint["tenperatura"] * traint["bibrazioa"]).min())
TXV_MAX = float((traint["tenperatura"] * traint["bibrazioa"]).max())
print(f"txv global: [{TXV_MIN:.1f}, {TXV_MAX:.1f}]")
""")

md("""## 4. Fusión por consenso + evaluación holdout (200k freskoak)

`final = max(fuzzy, anomalia)` alarma gisa; iragarpena **adostasunez**:
anomalia ALTA *eta* fuzzy ALTA. Bi seinaleek fisikotasuna eskatzen dute
(zarata puruak bata aktibatzen du, gutxitan biak). Umbralak validazioan.""")

code("""from cnc_guard.anomaly import riesgo_final
from cnc_guard.fuzzy import riesgo_norm
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score

hold = pd.read_csv(DATA, skiprows=range(1, 10_000_000 - 200_000), nrows=200_000)
Xh = build_features(hold)
yh = hold["errorea"].to_numpy()
anom = anomaly_score(model, scaler, Xh, dmin, dmax)
txv_h = hold["tenperatura"] * hold["bibrazioa"]
wear_h = (((txv_h - TXV_MIN) / (TXV_MAX - TXV_MIN)).clip(0, 1)).to_numpy()
fuzz = np.array([riesgo_norm(t, v, w) for t, v, w in
                 zip(hold["tenperatura"].to_numpy(), hold["bibrazioa"].to_numpy(), wear_h)])
final = np.maximum(fuzz, anom)
av, yv, at, yt = anom[:100_000], yh[:100_000], anom[100_000:], yh[100_000:]
fv, ft = fuzz[:100_000], fuzz[100_000:]
best, best_f = (0.5, 0.5), 0.0
for ta in (0.5, 0.7, 0.85):
    for tf in (0.3, 0.5, 0.7):
        f = f1_score(yv, ((av >= ta) & (fv >= tf)).astype(int), zero_division=0)
        if f > best_f:
            best, best_f = (ta, tf), f
ta, tf = best
pred = ((at >= ta) & (ft >= tf)).astype(int)
acc = accuracy_score(yt, pred)
f1 = f1_score(yt, pred, zero_division=0)
print(f"adostasuna: ta={ta} tf={tf} acc={acc:.4f} F1={f1:.4f} (max-fusio lagungarria: {riesgo_final(0.2, 0.8)})")
print(confusion_matrix(yt, pred))
assert acc > 0.95 and f1 > 0.15, (acc, f1)

import json
(Path.cwd() / "reports" / "metrikas.json").write_text(
    json.dumps({"ta": ta, "tf": tf, "acc": round(float(acc), 4), "f1": round(float(f1), 4),
                "n_holdout": 200_000}, indent=2), encoding="utf-8")
print("metrikas.json gordeta")
""")

md("""## 5. Ondorioak (taldearekin partekatzeko)

1. **Fusioak funtzionatzen du**: fuzzy-ak ezagutza aditua kodetzen du (monotonoa, mugak testatuta),
   IsolationForest-ek datu-ereduak, eta `max`-ek alarma pizten du bietako batek jotzen duenean.
2. **Datuak dira sabaia**: akatsen %85 zarata purua → F1 ≈ 0.2 da lorpen zintzoa, ez porrota.
   Seinale fisikoa (AND tenp×vib) feature engineering gabe ikusezina da (F1=0).
3. **Mugak**: sintetikoa (ez balio industrial), konektor­erik gabe, umbrala holdout-ean kalibratuta
   (produkzioan: kalibraketa rolling + alerta-fatiga kontrola).
4. **Hurrengoa**: OPC-UA irakurketa makina errealean, dashboard extra (`streamlit`), MongoDB sink DF2.2 erara.""")

nb = nbf.v4.new_notebook()
nb.metadata["language_info"] = {"name": "python"}
cells = []
for kind, src in MD:
    cells.append(nbf.v4.new_markdown_cell(src) if kind == "markdown" else nbf.v4.new_code_cell(src))
nb.cells = cells
nbf.write(nb, "CNC_Guard.ipynb")
print(f"CNC_Guard.ipynb: {len(cells)} celdas")
