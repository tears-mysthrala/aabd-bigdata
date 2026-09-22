"""Test estabilidad cnc_10M.csv (10M filas): conteo, agregados por chunks + SGD incremental.

Uso (venv CNC): .../proyecto_cnc_guard/.venv/bin/python test_estabilidad_10M.py [--csv cnc_10M.csv]
RAM: nunca carga el CSV entero (chunks de 1M).
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).parent
CHUNK = 1_000_000
FEATS = ["tenperatura", "bibrazioa", "presioa"]
DUMMIES = ["M1", "M2", "M3", "M4", "M5"]


def frame(chunk: pd.DataFrame) -> pd.DataFrame:
    d = pd.get_dummies(chunk["makina_id"])
    for m in DUMMIES:
        if m not in d:
            d[m] = 0
    num = chunk[FEATS].astype("float32")
    # Feature engineering: el fallo es (temp ALTA *Y* vib ALTA) → el modelo lineal
    # necesita el término de interacción para aislar la región AND.
    num["txv"] = num["tenperatura"] * num["bibrazioa"]
    num["t2"] = num["tenperatura"] ** 2
    return pd.concat([num, d[DUMMIES].astype("float32")], axis=1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=str(HERE / "cnc_10M.csv"))
    ap.add_argument("--chunksize", type=int, default=CHUNK)
    args = ap.parse_args()
    t0 = time.time()

    # 1) Conteo + agregados exactos por chunks
    n = 0
    suma = {}
    err = 0
    for ch in pd.read_csv(args.csv, chunksize=args.chunksize, usecols=["makina_id", "tenperatura", "errorea"]):
        n += len(ch)
        err += int(ch["errorea"].sum())
        for m, g in ch.groupby("makina_id")["tenperatura"].mean().items():
            suma.setdefault(m, []).append((float(g), len(ch[ch["makina_id"] == m])))
    assert n == 10_000_000, f"filas={n}"
    rate = err / n
    medias = {m: sum(v * k for v, k in vs) / sum(k for _, k in vs) for m, vs in suma.items()}
    print(f"conteo={n} err_rate={rate:.4f} t_medias={np.mean(list(medias.values())):.2f}")
    assert 0.005 < rate < 0.03, rate  # fallos raros (industria realista)
    assert 63.0 < np.mean(list(medias.values())) < 67.0, medias

    # 2) SGD incremental en chunks 0..7, umbral calibrado en chunk 8, holdout = chunk 9.
    # Sin calibrar (0.5), el desbalanceo 98.8/1.2 da F1=0: se calibra el umbral con F1.
    scaler = StandardScaler()
    clf = SGDClassifier(loss="log_loss", random_state=42)
    valid = None
    holdout = None
    n_chunks = 0
    for i, ch in enumerate(pd.read_csv(args.csv, chunksize=args.chunksize)):
        n_chunks += 1
        X = frame(ch)
        y = ch["errorea"].to_numpy()
        if i == 0:
            scaler.fit(X.iloc[:500_000])
        Xp = scaler.transform(X)
        if i == 8:
            valid = (Xp, y)
        elif i == 9:
            holdout = (Xp, y)
        else:
            clf.partial_fit(Xp, y, classes=np.array([0, 1]) if i == 0 else None)
    assert n_chunks == 10 and valid is not None and holdout is not None
    pv = clf.predict_proba(valid[0])[:, 1]
    best_t, best_f1 = 0.5, f1_score(valid[1], (pv >= 0.5).astype(int), zero_division=0)
    for t in (0.3, 0.2, 0.1, 0.05, 0.02, 0.01):
        f = f1_score(valid[1], (pv >= t).astype(int), zero_division=0)
        if f > best_f1:
            best_t, best_f1 = t, f
    ph = clf.predict_proba(holdout[0])[:, 1]
    yh = (ph >= best_t).astype(int)
    acc = accuracy_score(holdout[1], yh)
    f1 = f1_score(holdout[1], yh, zero_division=0)
    dt = time.time() - t0
    print(f"SGD 10M: umbral={best_t} acc={acc:.4f} F1={f1:.4f} ({dt:.0f}s)")
    assert acc > 0.90, acc
    assert f1 > 0.20, f1
    print(f"OK — estabilidad 10M ({dt:.0f}s, picos RAM por chunk de 1M).")


if __name__ == "__main__":
    main()
