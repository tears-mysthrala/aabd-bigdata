# %% [markdown]
# 5072 Ikasketa Automatikoa — Praktika (ML1+ML2)
# EDA + aurreprozesamendua + ikasketa gainbegiratua (erregresioa + sailkapena).
# Teoria: 03_ML_5072/materialak (1. atala: X/y, EDA, missing, outlier, kodetze, eskalatze;
# 2. atala: MSE, erregresio lineala/anizkoitza, Ridge/Lasso, train/test, overfitting).
# Datuak: ../../04_Programazioa_5073/data/cnc_mock.csv (makina_id, tenperatura, bibrazioa, errorea)

# %% imports
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, Ridge, Lasso, LogisticRegression
from sklearn.metrics import mean_squared_error, accuracy_score, f1_score, confusion_matrix

DATA = Path(__file__).resolve().parents[1].joinpath(
    "../04_Programazioa_5073/data/cnc_mock.csv"
).resolve()
# Cuando se ejecuta desde 03_ML_5072/soluzioak/, DATA apunta a 04_Programazioa_5073/data/.
# Fallback a ruta absoluta del lab:
if not DATA.is_file():
    DATA = Path("/home/tears/bigdata/04_Programazioa_5073/data/cnc_mock.csv")

# %% 1. Karga + tipologia X/y
df = pd.read_csv(DATA)
assert list(df.columns) == ["makina_id", "tenperatura", "bibrazioa", "errorea"], df.columns.tolist()
assert len(df) == 100, len(df)
print(f"n={len(df)}, p=3 ezaugarri + 1 etiketa")
print(df.dtypes.to_string())
# Tipologia: makina_id nominala, tenperatura/bibrazioa kuantitatibo jarraiak, errorea bitarra.

# %% 2. EDA laburra
desc = df[["tenperatura", "bibrazioa"]].describe()
n_missing = int(df[["tenperatura", "bibrazioa"]].isna().sum().sum())
assert desc.loc["count", "tenperatura"] == len(df) - int(df["tenperatura"].isna().sum())
print(f"missing conteen (NaN errealak praktikan): {n_missing}")
print(desc.to_string())
print("missing:\n", df.isna().sum().to_string())
print("errorea banaketa:\n", df["errorea"].value_counts().to_string())
# Korrelazioa (lineala):
corr = df[["tenperatura", "bibrazioa"]].corr(numeric_only=True)
assert corr.shape == (2, 2)
print("korrelazioa:\n", corr.to_string())

# %% 3. Aurreprozesamendua: missing + outlier IQR + kodetze + eskalatze
# (Datu hauetan ez dago NaN; pipeline-ak NaN hipotetikoak kudeatzen ditu.)
num_cols = ["tenperatura", "bibrazioa"]
cat_cols = ["makina_id"]

# Outlier detekzioa IQR bidez (informazioa, ez ezabaketa agresiboa):
for c in num_cols:
    q1, q3 = df[c].quantile([0.25, 0.75])
    iqr = q3 - q1
    n_out = int(((df[c] < q1 - 1.5 * iqr) | (df[c] > q3 + 1.5 * iqr)).sum())
    print(f"{c}: IQR-outlierrak={n_out}")

pre = ColumnTransformer(
    [
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), num_cols),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                          ("oh", OneHotEncoder(handle_unknown="ignore"))]), cat_cols),
    ]
)
X = df[["makina_id", "tenperatura", "bibrazioa"]]
Xtr = pre.fit_transform(X)
assert Xtr.shape[0] == 100 and Xtr.shape[1] >= 3, Xtr.shape
print("X preprocessed shape:", Xtr.shape)

# %% 4. Erregresioa: tenperatura ~ bibrazioa (+ makina)
# Helburuak NaN badu, errenkada hori ezin da entrenatu (X-ko NaN-ak pipeline-ak inputatzen ditu).
df_reg = df.dropna(subset=["tenperatura"]).reset_index(drop=True)
print(f"erregresioa: n={len(df_reg)} (NaN helburuak kenduta)")
# 4a. Sinplea (bibrazioa -> tenperatura), MSE (inputazioarekin):
Xr = df_reg[["bibrazioa"]]
yr = df_reg["tenperatura"].to_numpy()
Xr_tr, Xr_te, yr_tr, yr_te = train_test_split(Xr, yr, test_size=0.25, random_state=42)
lin = Pipeline([("imp", SimpleImputer(strategy="median")), ("mdl", LinearRegression())])
lin.fit(Xr_tr, yr_tr)
beta1 = lin.named_steps["mdl"].coef_[0]
mse_tr = mean_squared_error(yr_tr, lin.predict(Xr_tr))
mse_te = mean_squared_error(yr_te, lin.predict(Xr_te))
print(f"lineal sinplea: MSE train={mse_tr:.2f} test={mse_te:.2f} beta1={beta1:.3f}")
assert np.isfinite(mse_te) and mse_te > 0

# 4b. Anizkoitza + Ridge/Lasso konparaketa (pipeline osoa):
# (Erregresioan helburua tenperatura da → ezaugarriak: makina_id + bibrazioa.)
pre_reg = ColumnTransformer(
    [
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), ["bibrazioa"]),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                          ("oh", OneHotEncoder(handle_unknown="ignore"))]), ["makina_id"]),
    ]
)
y_reg = df_reg["tenperatura"].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(
    df_reg[["makina_id", "bibrazioa"]], y_reg, test_size=0.25, random_state=42,
)
resultados = {}
for nombre, modelo in [("lineala", LinearRegression()), ("ridge", Ridge(alpha=1.0)), ("lasso", Lasso(alpha=0.1, max_iter=5000))]:
    pipe = Pipeline([("pre", pre_reg), ("mdl", modelo)])
    pipe.fit(X_train, y_train)
    mse = mean_squared_error(y_test, pipe.predict(X_test))
    resultados[nombre] = mse
    print(f"{nombre}: MSE test={mse:.2f}")
assert all(np.isfinite(v) for v in resultados.values())
# Ridge-k koefizienteak mugatzen ditu, Lasso-k zero-ra eraman ditzake (hautaketa):
print("ridge/lasso MSE-ak:", {k: round(v, 2) for k, v in resultados.items()})

# %% 5. Sailkapena: errorea (0/1) — train/test + overfitting kontrola
y_clf = df["errorea"].to_numpy()
Xc_tr, Xc_te, yc_tr, yc_te = train_test_split(
    X, y_clf, test_size=0.30, random_state=42, stratify=y_clf
)
clf = Pipeline([("pre", pre), ("mdl", LogisticRegression(max_iter=2000))])
clf.fit(Xc_tr, yc_tr)
acc_tr = accuracy_score(yc_tr, clf.predict(Xc_tr))
acc_te = accuracy_score(yc_te, clf.predict(Xc_te))
f1 = f1_score(yc_te, clf.predict(Xc_te), zero_division=0)
cm = confusion_matrix(yc_te, clf.predict(Xc_te))
print(f"sailkapena: acc train={acc_tr:.3f} test={acc_te:.3f} F1={f1:.3f}")
print("confusion matrix:\n", cm)
assert 0.0 <= acc_te <= 1.0
# Overfitting seinalea: train >> test aldea handia bada, regularizatu (C txikiagoa) edo datu gehiago.
print(f"overfitting aldea (train-test)={acc_tr - acc_te:+.3f}")
# Klase-desoreka (95/5): F1=0 → ereduak dena 0 iragartzen du. Konponbidea: class_weight='balanced'.
clf_bal = Pipeline([("pre", pre), ("mdl", LogisticRegression(max_iter=2000, class_weight="balanced"))])
clf_bal.fit(Xc_tr, yc_tr)
print(f"balanced: acc test={accuracy_score(yc_te, clf_bal.predict(Xc_te)):.3f} "
      f"F1={f1_score(yc_te, clf_bal.predict(Xc_te), zero_division=0):.3f}")
print("OK — 5072 praktika osoa (EDA + preprocess + erregresio + sailkapena).")
