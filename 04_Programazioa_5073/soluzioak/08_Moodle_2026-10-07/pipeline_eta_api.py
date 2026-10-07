# %% [markdown]
# # Programación — ampliación Pipeline/API del 7 de octubre
# Fuentes: [3_Adibide_koadernoa_URLa.ipynb](../../materialak/3_Adibide_koadernoa_URLa.ipynb) y [PDF tema 3](../../materialak/5073_3_Programazioa.pdf), bloque 1.5 y API 3.4.
# Las actividades de los cuadernos 1/2/3 permanecen en [soluciones de ayer](../07_Moodle_2026-10-06/README.md). El diff de hoy en esos cuadernos no añade ejercicios. Esta ampliación cubre los dos Pipeline y el nuevo lifespan/API, con modelo propio y ruta coherente. El `.pkl` descargado de Moodle **no se deserializa**.

# %% [markdown]
# ## Objetivo y decisiones
# Pipeline integra imputación, escalado/encoder y modelo; aprender preprocesamiento solo de train evita fuga. Guardar solo el estimador perdería esas transformaciones. El dataset de rotación es sintético, con target aleatorio: una accuracy no demuestra capacidad para evaluar empleados.
# Breast cancer es un dataset público incorporado en sklearn: 30 atributos, clase 0 malignant/Gaiztoa, clase 1 benign/Ona. Split 80/20 semilla 42 estratificado (adaptación declarada frente al ejemplo sin estratificación); RobustScaler y logística con max_iter=2000. La etiqueta y la probabilidad devuelta corresponden a **la clase predicha**, localizada en `classes_`, no siempre a columna 1. No es herramienta clínica.
# Archivos propios en `models/`, ignorados por Git. El script de entrenamiento crea la carpeta y recarga solo el artefacto que acaba de generar. La API carga esa misma ruta absoluta derivada de su módulo, para no depender del cwd. Joblib puede ejecutar código: no sustituir el archivo por uno descargado, aunque tenga hash.

# %%
import numpy as np
from fastapi.testclient import TestClient
from ml_api import create_app
from sklearn.metrics import classification_report
from train_pipeline import MODEL_PATH, train_breast_cancer, train_turnover

turnover_accuracy = train_turnover()
model, X_test, y_test = train_breast_cancer()
print("Accuracy sintética de rotación:", turnover_accuracy)
print(
    classification_report(
        y_test, model.predict(X_test), target_names=["malignant", "benign"]
    )
)
with TestClient(create_app(MODEL_PATH)) as client:
    assert client.get("/osasuna").status_code == 200
    predictions = model.predict(X_test)
    for target in [0, 1]:
        row = X_test[np.flatnonzero(predictions == target)[0]]
        response = client.post("/iragarri", json={"ezaugarriak": row.tolist()})
        assert response.status_code == 200
        data = response.json()
        assert data["iragarpena"] == data["probabilitate_klasea"] == target
        assert data["etiketa"] == {0: "Gaiztoa", 1: "Ona"}[target]
        print(data)
    assert client.post("/iragarri", json={"ezaugarriak": [1] * 29}).status_code == 422
    app = client.app
assert app.state.model is None

# %% [markdown]
# ## Ciclo de vida y comprobación
# Startup inicializa `app.state.model` y carga el modelo local si existe; si falta, salud y predicción devuelven 503. No se sirve una predicción silenciosa sin modelo. Shutdown limpia el estado en `finally`; cada app tiene estado propio. El contexto de TestClient ejecuta lifespan, no solo llamadas a funciones.
# `test_ml_api.py` prueba ambas clases/probabilidades, payloads inválidos, no finitos, ausencia del modelo y limpieza al salir. Esto no demuestra seguridad o disponibilidad de producción.
# Para HTTP real: `uv run uvicorn ml_api:app --host 127.0.0.1 --port 18087`, después `curl http://127.0.0.1:18087/osasuna`. Detener con Ctrl-C. El README incluye la evidencia actual separada de la receta. API de laboratorio sin autenticación, únicamente loopback; no publicar en una red.
# Fuentes: [dataset sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_breast_cancer.html), [lifespan FastAPI](https://fastapi.tiangolo.com/advanced/events/).
