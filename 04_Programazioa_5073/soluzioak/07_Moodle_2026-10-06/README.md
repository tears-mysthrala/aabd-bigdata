# Soluciones propias de los cuadernos Moodle (2026-10-06)

Estas copias resuelven los tres cuadernos de ejercicios descargados desde Moodle. Los originales permanecen intactos en `04_Programazioa_5073/materialak/` para comparar después con las soluciones docentes.

- `1_Ariketa_koadernoa_RESUELTO.ipynb`: Python, JSON, archivos, Git y funciones.
- `2_Ariketa_Koadernoa_RESUELTO.ipynb`: NumPy, Pandas, limpieza y gráficos.
- `3_Ariketa_koadernoa_RESUELTO.ipynb`: scikit-learn, métricas, SMOTE, GridSearch, Pipeline, Joblib y Pydantic.

Se conservan los enunciados y las validaciones originales donde estaban incluidas. Los notebooks se ejecutan desde su propia carpeta de trabajo para que los datos generados no se mezclen con los originales.

La práctica de entornos virtuales requiere `uv` instalado y disponible en `PATH`. Este repositorio usa `uv venv` deliberadamente para conservar el aislamiento por ejercicio y reutilizar la caché global (véase `AGENTS.md`); la orden `python -m venv` del enunciado sirve como referencia conceptual. Instala primero `uv` siguiendo su documentación oficial: https://docs.astral.sh/uv/getting-started/installation/.
