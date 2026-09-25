"""Tema 3, cuaderno práctico: soluciones de referencia para 25 ejercicios.

Ejecutar desde esta carpeta para que `data/` quede junto a la solución.
El conjunto de datos es sintético y no representa pacientes ni procesos reales.
"""

# %% Preparación: mismos datos que el enunciado
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError, field_validator
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
X_sintetico, y_sintetico = make_classification(
    n_samples=2000, n_features=20, n_classes=2,
    weights=[0.9, 0.1], random_state=42,
)
pd.DataFrame(
    X_sintetico, columns=[f"feature_{i}" for i in range(20)]
).assign(target=y_sintetico).to_csv(DATA_DIR / "dataset.csv", index=False)
del X_sintetico, y_sintetico

# %% 1.1–1.5: separación y escalado sin fuga de información
# 1.1: cargar el CSV, aunque la celda de preparación ya haya creado los datos.
df = pd.read_csv(DATA_DIR / "dataset.csv")

# 1.2: separar atributos y objetivo.
X = df.drop(columns="target")
y = df["target"]

# 1.3: conservar la proporción 90/10 en ambos conjuntos.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y,
)

# 1.4: aprender media y desviación solo con train.
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 1.5: la media de train queda aproximadamente en cero.
batezbestekoa = float(np.mean(X_train_scaled[:, 0]))
print(f"1.5 Media de la primera columna de train: {batezbestekoa:.3g}")

# %% 2.1–2.5: métricas de la clase minoritaria
# 2.1: entrenar regresión logística con los datos escalados de train.
model_lr = LogisticRegression(max_iter=1000)
model_lr.fit(X_train_scaled, y_train)

# 2.2: predecir solo el conjunto de test.
y_pred = model_lr.predict(X_test_scaled)

# 2.3–2.5: accuracy, recall de clase 1 y matriz de confusión.
acc = accuracy_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
print(f"2.3 Accuracy: {acc:.3f}; 2.4 Recall clase 1: {rec:.3f}")
print(f"2.5 Matriz de confusión (filas reales, columnas predichas):\n{cm}")

# %% 3.1–3.5: comparar ponderación y Random Forest
# 3.1: comprobar el desbalance en train.
counts = y_train.value_counts().sort_index()
print(f"3.1 Clases en train:\n{counts}")

# 3.2: ponderar clases según sus frecuencias en train.
model_balanced = LogisticRegression(class_weight="balanced", max_iter=1000)
model_balanced.fit(X_train_scaled, y_train)

# 3.3: medir; class_weight no garantiza que el recall aumente.
y_pred_balanced = model_balanced.predict(X_test_scaled)
rec_balanced = recall_score(y_test, y_pred_balanced)
print(f"3.3 Recall sin ponderar: {rec:.3f}; ponderado: {rec_balanced:.3f}")

# 3.4: bosque con pesos calculados en cada muestra bootstrap.
rf_balanced = RandomForestClassifier(
    class_weight="balanced_subsample", random_state=42,
)
rf_balanced.fit(X_train_scaled, y_train)

# 3.5: mismo test y misma definición de recall.
rf_pred = rf_balanced.predict(X_test_scaled)
rf_rec = recall_score(y_test, rf_pred)
print(f"3.5 Recall Random Forest: {rf_rec:.3f}")

# %% 4.1–4.5: Pipeline y persistencia
# 4.1: el escalador estará dentro del Pipeline.
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", RandomForestClassifier(
        class_weight="balanced", random_state=42,
    )),
])

# 4.2–4.3: pasar datos sin escalar; Pipeline ajusta con train.
pipeline.fit(X_train, y_train)
pipe_acc = accuracy_score(y_test, pipeline.predict(X_test))
print(f"4.3 Accuracy del Pipeline: {pipe_acc:.3f}")

# 4.4–4.5: cargar únicamente el artefacto que acabamos de crear.
MODEL_PATH = DATA_DIR / "eredua.pkl"
joblib.dump(pipeline, MODEL_PATH)
eredu_kargatua = joblib.load(MODEL_PATH)
iragarpen_1 = eredu_kargatua.predict(X_test.iloc[[0]])
print(f"4.5 Primera predicción tras cargar: {iragarpen_1[0]}")

# %% 5.1–5.5: esquemas y función de predicción
# 5.1: modelo inicial del request.
class PredictionRequestInitial(BaseModel):
    features: list[float]


# 5.2: versión final, con exactamente 20 atributos.
class PredictionRequest(BaseModel):
    features: list[float]

    @field_validator("features")
    @classmethod
    def validar_longitud(cls, values: list[float]) -> list[float]:
        if len(values) != 20:
            raise ValueError("Se necesitan exactamente 20 características")
        return values


# 5.3: capturar el error que Pydantic presenta al usuario.
errorea_dago = False
try:
    PredictionRequest(features=[0.0, 0.0, 0.0])
except ValidationError as error:
    errorea_dago = True
    print(f"5.3 Validación esperada: {error.errors()[0]['msg']}")


# 5.4: esquema de respuesta.
class PredictionResponse(BaseModel):
    klasea: int
    probabilitatea: float


# 5.5: preservar el orden y los nombres de las columnas del entrenamiento.
def egin_iragarpena(req: PredictionRequest) -> PredictionResponse:
    features = pd.DataFrame([req.features], columns=X_train.columns)
    klasea = int(eredu_kargatua.predict(features)[0])
    probabilitatea = float(eredu_kargatua.predict_proba(features)[0, 1])
    return PredictionResponse(klasea=klasea, probabilitatea=probabilitatea)


req_test = PredictionRequest(features=[0.0] * 20)
resp = egin_iragarpena(req_test)
print(f"5.5 Respuesta de ejemplo: {resp.model_dump()}")
