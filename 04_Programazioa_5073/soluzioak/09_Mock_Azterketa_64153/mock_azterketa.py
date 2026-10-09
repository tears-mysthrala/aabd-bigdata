# %% [markdown]
# # Preparación del examen · Moodle 64153
# Fuente: [guía docente](../../materialak/Moodle_page_64153.md).
# La guía contiene cinco preguntas de ejemplo y seis habilidades prácticas,
# no un examen completo ni un CSV específico. Esta práctica usa el CSV sintético
# de máquinas ya versionado en `../../data/cnc_mock.csv`, sin modificarlo.
# Objetivo: recorrer limpieza Pandas, Pipeline, desbalance, métricas y Pydantic.
# Ejecutar aquí: `uv sync --frozen` y `uv run --frozen python mock_azterketa.py`.
# Solo sobrescribe resultados propios; no descarga datos, abre APIs ni usa pickle.

# %% [markdown]
# ## Teoría: respuestas razonadas a las cinco preguntas
# 1. **C. Java**: el ejemplo destaca rendimiento y sistemas de producción
# robustos del ecosistema Hadoop/Spark. A describe el énfasis estadístico de R,
# B el ecosistema de Python y D ejecución en navegador con JavaScript.
# No significa que Java sea obligatorio ni que los demás no sirvan en producción.
# 2. **B. MCP**: estandariza la conexión de aplicaciones/agentes con herramientas
# y fuentes externas. No instala Python, no comparte temas de IDE ni fusiona Git.
# El protocolo no concede por sí mismo autorización para ejecutar herramientas.
# 3. **B. Figure y Axes**: Figure contiene la figura completa; Axes representa
# cada área de gráfico con sus ejes. Una Figure puede contener varios Axes.
# 4. **C. dropna**: elimina filas o columnas con valores ausentes, según axis,
# subset y how. `fillna` imputa; `drop_duplicates` elimina duplicados.
# 5. **B. Cargar al arrancar**: una carga por proceso evita repetirla por petición.
# En una implementación actual puede usarse lifespan; varios workers cargan
# cada uno su copia. Solo cargar modelos de procedencia propia/verificada.
# La guía no concreta la penalización de errores del test: no inventamos una
# fórmula de nota ni añadimos 25 preguntas presentándolas como docentes.

# %%
import hashlib
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pydantic import BaseModel, ConfigDict, field_validator
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
)
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
SOURCE = HERE / ".." / ".." / "data" / "cnc_mock.csv"
FEATURES = ["tenperatura", "bibrazioa"]


def clean_data(raw):
    """Reglas de esta variante, fijadas antes de mirar métricas de test."""
    frame = raw.copy()
    frame.columns = [name.strip().lower().replace(" ", "_") for name in frame.columns]
    if set(frame.columns) != {"makina_id", *FEATURES, "errorea"}:
        raise ValueError("Columnas inesperadas en el CSV")
    if not frame.errorea.isin([0, 1]).all():
        raise ValueError("La etiqueta debe ser 0 o 1; no se imputa")
    if frame.makina_id.isna().any():
        raise ValueError("Identificadores de máquina ausentes")
    for name in FEATURES:
        frame[name] = pd.to_numeric(frame[name], errors="coerce")
    # Sin transformers de sklearn: filtros y eliminación de NaN con Pandas.
    valid = (
        frame[FEATURES].notna().all(axis=1)
        & np.isfinite(frame[FEATURES]).all(axis=1)
        & frame.tenperatura.between(0, 150)
        & frame.bibrazioa.ge(0)
    )
    return frame.loc[valid].copy(), frame.loc[~valid].copy()


class MachineInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tenperatura: float
    bibrazioa: float

    @field_validator("tenperatura", "bibrazioa")
    @classmethod
    def finite_nonnegative(cls, value):
        if not math.isfinite(value) or value < 0:
            raise ValueError("Se requiere un número finito no negativo")
        return value

    @field_validator("tenperatura")
    @classmethod
    def plausible_temperature(cls, value):
        if value > 150:
            raise ValueError("Fuera del rango de esta variante: 0–150 °C")
        return value


def predict_input(model, request):
    row = pd.DataFrame([request.model_dump()], columns=FEATURES)
    index = list(model.classes_).index(1)
    return {
        "errorea": int(model.predict(row)[0]),
        "probabilitatea_errorea_1": float(model.predict_proba(row)[0, index]),
    }


def fit_and_evaluate(clean):
    split = GroupShuffleSplit(n_splits=1, test_size=1 / 3, random_state=42)
    train_index, test_index = next(split.split(clean, groups=clean.makina_id))
    train, test = clean.iloc[train_index], clean.iloc[test_index]
    if train.errorea.nunique() != 2 or test.errorea.nunique() != 2:
        raise ValueError("Este split necesita ambas clases en train y test")
    model = make_pipeline(
        StandardScaler(), LogisticRegression(class_weight="balanced", max_iter=1000)
    )
    model.fit(train[FEATURES], train.errorea)
    pred = model.predict(test[FEATURES])
    matrix = confusion_matrix(test.errorea, pred, labels=[0, 1])
    tn, fp, fn, tp = matrix.ravel()
    metrics = {
        "accuracy": float(accuracy_score(test.errorea, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(test.errorea, pred)),
        "recall_class_1": float(recall_score(test.errorea, pred, zero_division=0)),
        "precision_class_1": float(
            precision_score(test.errorea, pred, zero_division=0)
        ),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
        "always_zero_accuracy": float((test.errorea == 0).mean()),
        "classification_report": classification_report(
            test.errorea, pred, labels=[0, 1], output_dict=True, zero_division=0
        ),
    }
    assert set(train.makina_id).isdisjoint(test.makina_id)
    assert model.named_steps["standardscaler"].n_samples_seen_ == len(train)
    assert tn + fp + fn + tp == len(test)
    assert metrics["recall_class_1"] == tp / (tp + fn)
    return model, train, test, pred, metrics


# %% [markdown]
# ## Práctica: por qué se hacen estos pasos
# **List comprehension** normaliza nombres; no transforma etiquetas a partir
# de la respuesta esperada. **Pandas** elimina NaN, valores no finitos y medidas
# fuera del rango declarado. El límite 150 °C pertenece a este ejercicio;
# no es una regla industrial universal. Los descartes se conservan para auditar.
# Eliminar filas evita imputación aprendida antes del split, pero puede sesgar
# los datos y perder fallos reales: hay que investigar su mecanismo de ausencia.
# **Pipeline** aprende StandardScaler exclusivamente con train y aplica luego
# el mismo escalado al test. IDs y etiqueta no son atributos predictivos.
# M1/M2/M3 aparecen varias veces: se reserva una máquina completa con
# GroupShuffleSplit y se entrenan las otras dos, evitando compartir máquina
# entre train y test. El reparto no es estratificado; se comprueban ambas clases
# y el número reducido de grupos impide estimar rendimiento con precisión.
# **balanced** pondera cada clase de forma inversa a su frecuencia en train:
# n/(n_clases*n_clase). No crea ejemplos ni garantiza mejor recall. No todos
# los estimadores aceptan class_weight; escoger siempre según tarea y evidencia.
# **Recall** importa si perder un fallo es costoso: TP/(TP+FN). Hay que revisar
# también FP y precisión, porque alertas falsas tienen coste. Accuracy sola
# puede ser alta prediciendo siempre la clase mayoritaria. La matriz usa filas
# reales y columnas predichas, orden [0,1]; support es el número real por clase.
# El umbral queda en 0.5; no lo ajustamos usando los resultados de test.
# **Pydantic** valida entradas futuras con las mismas reglas; aquí probabilidad
# significa P(errorea=1), también cuando la predicción es 0. No arrancamos FastAPI:
# la guía pide el esquema, no publicar un servicio ni una entrega a Moodle.


# %%
def run():
    output = HERE / "resultados"
    output.mkdir(exist_ok=True)
    raw = pd.read_csv(SOURCE)
    clean, rejected = clean_data(raw)
    model, train, test, pred, metrics = fit_and_evaluate(clean)
    clean.to_csv(output / "datu_garbiak.csv", index_label="registro_id")
    rejected.to_csv(output / "baztertutakoak.csv", index_label="registro_id")
    pd.DataFrame(
        {
            "registro_id": test.index,
            "makina_id": test.makina_id,
            "y_true": test.errorea,
            "y_pred": pred,
        }
    ).to_csv(output / "test_predictions.csv", index=False)
    report = {
        "source": "../../data/cnc_mock.csv; mock sintético previo, no CSV específico del examen",
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "raw_rows": len(raw),
        "clean_rows": len(clean),
        "rejected_rows": len(rejected),
        "train_rows": len(train),
        "test_rows": len(test),
        "train_machines": sorted(train.makina_id.unique().tolist()),
        "test_machines": sorted(test.makina_id.unique().tolist()),
        "train_row_ids": train.index.tolist(),
        "test_row_ids": test.index.tolist(),
        "class_counts": {
            str(k): int(v) for k, v in clean.errorea.value_counts().items()
        },
        "metrics": metrics,
        "example_validated_request": predict_input(
            model, MachineInput(tenperatura=60, bibrazioa=5)
        ),
    }
    (output / "validacion.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    ConfusionMatrixDisplay.from_predictions(
        test.errorea,
        pred,
        labels=[0, 1],
        display_labels=["Sin error", "Error"],
        colorbar=False,
    )
    plt.title("Mock de preparación · test reservado")
    plt.xlabel("Clase predicha")
    plt.ylabel("Clase real")
    plt.tight_layout()
    plt.savefig(output / "confusion.png", dpi=140)
    if "__file__" not in globals():
        from IPython.display import Image, display

        display(Image(filename=str(output / "confusion.png")))
    plt.show()
    plt.close("all")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


if __name__ == "__main__":
    results = run()

# %% [markdown]
# ## Interpretación y límites
# Ejecución de esta edición: 96 filas válidas, 56 train y 40 test; TN=26,
# FP=11, FN=2, TP=1. Recall=1/3 y precisión=1/12; accuracy=27/40=0.675.
# El baseline siempre-cero logra 37/40=0.925 de accuracy pero recall cero:
# demuestra por qué accuracy sola es insuficiente. El modelo detecta solo uno
# de los tres errores de test y emite once falsas alertas: resultado débil,
# no un sistema apto para decidir mantenimiento. Son cifras históricas de este
# CSV/split/configuración; validacion.json conserva las calculadas al ejecutar.
# Revisar las cifras impresas y compararlas con el clasificador siempre-cero.
# Hay solo cinco fallos en el CSV original: muy pocos para medir recall con
# precisión o justificar una decisión de mantenimiento. Los datos y sus etiquetas
# son sintéticos; esta ejecución demuestra el procedimiento, no capacidad real
# de anticipar averías. No confundas ejecutar esta solución con practicar sin
# ayuda: el examen teórico prohíbe apuntes y el práctico permite PDF pero no
# Internet ni asistentes. Antes del examen, intenta el enunciado por tu cuenta.
