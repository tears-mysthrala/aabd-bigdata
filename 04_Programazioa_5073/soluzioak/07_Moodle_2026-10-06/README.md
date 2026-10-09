# Soluciones propias de los cuadernos Moodle (2026-10-06)

Estas copias resuelven los tres cuadernos de ejercicios descargados desde Moodle. Los originales permanecen intactos en `04_Programazioa_5073/materialak/` para comparar después con las soluciones docentes.

- `1_Ariketa_koadernoa_RESUELTO.ipynb`: Python, JSON, archivos, Git y funciones.
- `2_Ariketa_Koadernoa_RESUELTO.ipynb`: NumPy, Pandas, limpieza y gráficos.
- `3_Ariketa_koadernoa_RESUELTO.ipynb`: scikit-learn, métricas, SMOTE, GridSearch, Pipeline, Joblib y Pydantic.

Se conservan los enunciados y las validaciones originales donde estaban incluidas. Los notebooks se ejecutan desde su propia carpeta de trabajo para que los datos generados no se mezclen con los originales.

## Contraste con las soluciones docentes del 9 de octubre

El nuevo [cuaderno docente](../../materialak/3_SOLUZIOAK_URLa.ipynb) mantiene las seis secciones numeradas y añade conclusiones y ejemplos FastAPI de los apuntes. Estos últimos ya se desarrollan en [Frameworks](../05_Frameworkak_PDF_Ariketak/README.md) y [Pipeline/API](../08_Moodle_2026-10-07/README.md); no se atribuyen sus resultados a nuestra ejecución.

La solución propia del cuaderno 3 incluye ahora [script equivalente](3_Ariketa_koadernoa_RESUELTO.py), explicación de TN/FP/FN/TP, comparación de recall, límites de elegir umbral con test y el significado `probabilitatea=P(target=1)`. GridSearch aprende el escalado dentro de cada fold y usa balanced accuracy por el desequilibrio, conservando los cuatro candidatos docentes. Pydantic rechaza NaN e infinitos además de exigir longitud 20.

Desde **esta carpeta**, para el cuaderno 3:

```bash
uv sync --frozen
MPLBACKEND=Agg uv run --frozen python 3_Ariketa_koadernoa_RESUELTO.py
```

El entorno bloqueado cubre el cuaderno 3; no certifica las dependencias ni los pasos humanos de los cuadernos 1 y 2. Ejecutar crea o sobrescribe `data/dataset.csv` sintético y `data/eredua.pkl`, ignorados en Git. Se recarga únicamente el modelo creado en esta misma ejecución; no cargar pickle docente o ajeno. En Jupyter usar el kernel de `.venv` y trabajar desde esta carpeta.

[Ejecución del día 9](EJECUCION_2026-10-09.json) y [auditoría de dependencias](AUDITORIA_DEPENDENCIAS.json): script y notebook ejecutados; sin vulnerabilidades conocidas detectadas. Recall de Logistic Regression: 0.6098; balanced: 0.8049; RF balanced: 0.6341; SMOTE: 0.7317; umbral impuesto 0.30: 0.8293. Son resultados del dataset sintético y este split, no mejoras garantizadas en otros datos. La simulación devuelve clase 0 con probabilidad de **clase 1** 0.1, no confianza 0.1 en la clase predicha.

El ejemplo docente Streamlit actualizado ya realiza una predicción, pero solo recibe cinco de treinta variables y completa las restantes con medias del dataset completo. Ese comportamiento sigue siendo una demostración parcial; para una evaluación propia habría que aprender los valores de relleno únicamente de train y aclarar la procedencia de las otras variables. Nuestra práctica Streamlit de Frameworks ya predice con sus entradas y utiliza su propio dataset sintético; no se presenta como réplica del ejemplo breast cancer.

La práctica de entornos virtuales requiere `uv` instalado y disponible en `PATH`. Este repositorio usa `uv venv` deliberadamente para conservar el aislamiento por ejercicio y reutilizar la caché global (véase `AGENTS.md`); la orden `python -m venv` del enunciado sirve como referencia conceptual. Instala primero `uv` siguiendo su documentación oficial: https://docs.astral.sh/uv/getting-started/installation/.

[Erratas y contratos comparados con la fuente docente](CONTRASTE_DOCENTE_2026-10-09.md).
