# Pipeline y API — ampliación del 7 de octubre

[Cuaderno](pipeline_eta_api.ipynb) y [script equivalente](pipeline_eta_api.py) explican los dos Pipeline y el ciclo de vida/API incorporado a los ejemplos y al [PDF tema 3](../../materialak/5073_3_Programazioa.pdf). Los ejercicios de ayer siguen en [07_Moodle_2026-10-06](../07_Moodle_2026-10-06/README.md).

## Ejecutar desde esta carpeta

```bash
uv sync --frozen
uv run --frozen python pipeline_eta_api.py
uv run --frozen pytest -q test_ml_api.py
uv run --frozen uvicorn ml_api:app --host 127.0.0.1 --port 18087
```

En otra terminal: `curl http://127.0.0.1:18087/osasuna`. Detener con Ctrl-C. Para Jupyter seleccionar el Python de `.venv` y ejecutar desde esta carpeta.

[train_pipeline.py](train_pipeline.py) crea y sobrescribe exclusivamente sus modelos propios en `models/` (ignorados), con imputación/escalado/encoder aprendido solo de train. Genera rotación sintética (target aleatorio) y el Pipeline breast cancer. Nunca carga el `.pkl` descargado de Moodle; joblib/pickle puede ejecutar código y un hash no acredita confianza en su contenido. No sustituir el modelo local por un artefacto ajeno.

[ml_api.py](ml_api.py) usa la misma ruta para guardar/cargar, resuelta respecto al módulo. Lifespan carga al arrancar y limpia al cerrar. Si falta el modelo devuelve 503; si está corrupto el arranque falla. Modelo solo de configuración del operador, nunca un path recibido por request. La clase 0 es malignant/Gaiztoa; 1 benign/Ona. La probabilidad corresponde a la clase predicha y `probabilitate_klasea` lo declara. Petición: exactamente 30 números finitos; campos extra rechazados, coerción numérica estándar de Pydantic. Es una API docente local sin autenticación: mantener en loopback.

## Validación actual

[EJECUCION.json](EJECUCION.json): notebook ejecutado; script ejecutado por separado. Rotación sintética accuracy 0.49: no demuestra predicción útil de abandono laboral. Breast cancer: 114 muestras de test estratificado, accuracy 0.9825; no acredita utilidad clínica ni calibración de probabilidades.

Ocho pruebas: clases y probabilidades 0/1, limpieza de lifespan, longitudes 29/31, no numéricos, nulos, NaN/±inf, modelo ausente y metadata del dataset. [HTTP_VERIFICACION.json](HTTP_VERIFICACION.json): uvicorn real en loopback, salud 200, dos predicciones 200, request inválida 422 y cierre del servidor verificado. No equivale a despliegue de producción/carga sostenida. El cuaderno guarda únicamente la prueba TestClient; la evidencia HTTP está separada.

El entorno actual emite una deprecación de Starlette sobre httpx en TestClient; las pruebas pasan y no se ha ocultado el aviso. [Auditoría de dependencias](AUDITORIA_DEPENDENCIAS.json): sin vulnerabilidades conocidas detectadas.
