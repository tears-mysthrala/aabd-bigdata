# %% [markdown]
# # Práctica ML 5072: del dato a la evaluación
#
# **Objetivo:** reconocer datos faltantes/extremos y comparar regresión y clasificación con preprocesamiento aprendido solo de train.
# **Entrada:** `../../04_Programazioa_5073/data/cnc_mock.csv`, 100 filas sintéticas. [Preparación, ejecución e interpretación](README.md).
# **Salida:** tablas y métricas impresas; no se guarda un modelo ni se exportan gráficos. La evaluación ilustra el método, no acredita un detector industrial.
#
# Ejecuta el script con el entorno indicado en el README. El notebook contiene código que usa `__file__`, variable propia de scripts que normalmente no existe en un kernel Jupyter: para ejecutar esa copia, adapta la celda de rutas a tu carpeta de trabajo o usa el `.py`. Esta revisión conserva las celdas de cálculo; no certifica una ejecución Jupyter de esta versión.

# %% [markdown]
# ## Preparar dependencias y localizar el CSV
#
# Se importan NumPy, Pandas y scikit-learn; `Path` construye la ruta al CSV. El control `is_file()` detiene la práctica si falta el dato. Tener el archivo evita descargas, pero no garantiza que su esquema sea correcto.

# %% imports
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Lasso, LinearRegression, LogisticRegression, Ridge
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DATA = (
    Path(__file__)
    .resolve()
    .parents[1]
    .joinpath("../04_Programazioa_5073/data/cnc_mock.csv")
    .resolve()
)
# Cuando se ejecuta desde 03_ML_5072/soluzioak/, DATA apunta a 04_Programazioa_5073/data/.
if not DATA.is_file():
    raise FileNotFoundError(f"Falta el dataset de la práctica: {DATA}")

# %% [markdown]
# ## 1. Identificar atributos y objetivo
#
# Se comprueba el esquema y las 100 filas. `makina_id` es categórico; temperatura y vibración son medidas; `errorea` es una etiqueta 0/1. Para regresión se predecirá temperatura y para clasificación, error: son dos preguntas diferentes.

# %% 1. Karga + tipologia X/y
df = pd.read_csv(DATA)
assert list(df.columns) == ["makina_id", "tenperatura", "bibrazioa", "errorea"], (
    df.columns.tolist()
)
assert len(df) == 100, len(df)
print(f"n={len(df)}, p=3 ezaugarri + 1 etiketa")
print(df.dtypes.to_string())
# Tipologia: makina_id nominala, tenperatura/bibrazioa kuantitatibo jarraiak, errorea bitarra.

# %% [markdown]
# ## 2. Explorar antes de entrenar
#
# `describe`, conteos de NaN, frecuencias y correlación revelan calidad y desbalance. El CSV tiene ausencias y extremos introducidos. Una correlación lineal pequeña no respalda un predictor lineal útil; una clase mayoritaria permite accuracy alta incluso sin detectar errores.

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

# %% [markdown]
# ## 3. Construir el preprocesamiento
#
# El IQR marca extremos para inspección; no los elimina. Hay **NaN reales** en el dato. Las variables numéricas se imputan con mediana y escalan; la máquina se codifica con one-hot. El ajuste efectivo del preprocesador ocurre al hacer `fit` sobre train dentro de cada Pipeline. El EDA global es descriptivo, no debe usarse para seleccionar parámetros con conocimiento de test.

# %% 3. Aurreprozesamendua: missing + outlier IQR + kodetze + eskalatze
# Datu hauetan NaN errealak daude; pipeline-ak train-eko estatistikekin inputatzen ditu.
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
        (
            "num",
            Pipeline(
                [("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]
            ),
            num_cols,
        ),
        (
            "cat",
            Pipeline(
                [
                    ("imp", SimpleImputer(strategy="most_frequent")),
                    ("oh", OneHotEncoder(handle_unknown="ignore")),
                ]
            ),
            cat_cols,
        ),
    ]
)
X = df[["makina_id", "tenperatura", "bibrazioa"]]
# La imputación y el escalado se ajustan dentro del pipeline con train.

# %% [markdown]
# ## 4. Regresión: comparar con una referencia sencilla
#
# Se retira la fila sin temperatura objetivo: no se puede entrenar con y ausente. Primero se predice temperatura desde vibración y luego se añade la máquina para comparar OLS, Ridge y Lasso con la misma separación. MSE mide error cuadrático (menor es mejor); R² puede ser negativo. Compara con predecir siempre la media de train y recuerda que el extremo 999 influye mucho en MSE. Finito no significa buen modelo.

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
r2_te = r2_score(yr_te, lin.predict(Xr_te))
baseline_mse = mean_squared_error(yr_te, np.full_like(yr_te, yr_tr.mean()))
print(
    f"lineal sinplea: MSE train={mse_tr:.2f} test={mse_te:.2f} R² test={r2_te:.3f} beta1={beta1:.3f}"
)
print(
    f"baseline media train: MSE test={baseline_mse:.2f}; correlación total={df_reg[['tenperatura', 'bibrazioa']].corr().iloc[0, 1]:.3f}"
)
print(
    "Este ajuste ilustra la API; una correlación casi nula no respalda una relación lineal útil."
)
assert np.isfinite(mse_te) and mse_te > 0

# 4b. Anizkoitza + Ridge/Lasso konparaketa (pipeline osoa):
# (Erregresioan helburua tenperatura da → ezaugarriak: makina_id + bibrazioa.)
pre_reg = ColumnTransformer(
    [
        (
            "num",
            Pipeline(
                [("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]
            ),
            ["bibrazioa"],
        ),
        (
            "cat",
            Pipeline(
                [
                    ("imp", SimpleImputer(strategy="most_frequent")),
                    ("oh", OneHotEncoder(handle_unknown="ignore")),
                ]
            ),
            ["makina_id"],
        ),
    ]
)
y_reg = df_reg["tenperatura"].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(
    df_reg[["makina_id", "bibrazioa"]],
    y_reg,
    test_size=0.25,
    random_state=42,
)
resultados = {}
for nombre, modelo in [
    ("lineala", LinearRegression()),
    ("ridge", Ridge(alpha=1.0)),
    ("lasso", Lasso(alpha=0.1, max_iter=5000)),
]:
    pipe = Pipeline([("pre", pre_reg), ("mdl", modelo)])
    pipe.fit(X_train, y_train)
    mse = mean_squared_error(y_test, pipe.predict(X_test))
    resultados[nombre] = mse
    print(f"{nombre}: MSE test={mse:.2f}")
assert all(np.isfinite(v) for v in resultados.values())
# Ridge-k koefizienteak mugatzen ditu, Lasso-k zero-ra eraman ditzake (hautaketa):
print("ridge/lasso MSE-ak:", {k: round(v, 2) for k, v in resultados.items()})

# %% [markdown]
# ## 5. Clasificación: leer la matriz y F1 junto a accuracy
#
# El split estratificado reserva 30 filas para test. La matriz usa filas de clase real y columnas predichas; F1 se refiere a la clase 1. Solo hay muy pocos errores positivos en test, así que un acierto cambia mucho las métricas. `balanced` cambia el peso durante el entrenamiento, sin garantizar mejora. El hueco train/test ayuda a detectar sobreajuste, pero un solo split pequeño no demuestra generalización.

# %% 5. Sailkapena: errorea (0/1) — train/test + overfitting kontrola
y_clf = df["errorea"].to_numpy()
Xc_tr, Xc_te, yc_tr, yc_te = train_test_split(
    X, y_clf, test_size=0.30, random_state=42, stratify=y_clf
)
clf = Pipeline([("pre", pre), ("mdl", LogisticRegression(max_iter=2000))])
clf.fit(Xc_tr, yc_tr)
print("X train preprocesado:", clf.named_steps["pre"].transform(Xc_tr).shape)
acc_tr = accuracy_score(yc_tr, clf.predict(Xc_tr))
acc_te = accuracy_score(yc_te, clf.predict(Xc_te))
f1 = f1_score(yc_te, clf.predict(Xc_te), zero_division=0)
cm = confusion_matrix(yc_te, clf.predict(Xc_te))
print(f"sailkapena: acc train={acc_tr:.3f} test={acc_te:.3f} F1={f1:.3f}")
print("confusion matrix:\n", cm)
assert 0.0 <= acc_te <= 1.0
# Overfitting seinalea: train >> test aldea handia bada, regularizatu (C txikiagoa) edo datu gehiago.
print(f"overfitting aldea (train-test)={acc_tr - acc_te:+.3f}")
# Klase-desoreka (95/5): testean 1-2 positibo soilik daude; F1 oso ezegonkorra.
# class_weight='balanced' aukera bat da, baina ezin da hobekuntza ziurtatu lagin honekin.
clf_bal = Pipeline(
    [("pre", pre), ("mdl", LogisticRegression(max_iter=2000, class_weight="balanced"))]
)
clf_bal.fit(Xc_tr, yc_tr)
print(
    f"balanced: acc test={accuracy_score(yc_te, clf_bal.predict(Xc_te)):.3f} "
    f"F1={f1_score(yc_te, clf_bal.predict(Xc_te), zero_division=0):.3f}"
)
print("OK — 5072 praktika osoa (EDA + preprocess + erregresio + sailkapena).")
