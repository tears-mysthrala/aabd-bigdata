# 5073, tema 3: cuaderno de ML y API

Soluciones de referencia para los 25 ejercicios de
[`5073_3_Programazioa_Ariketak.ipynb`](../../materialak/notebooks/5073_3_Programazioa_Ariketak.ipynb).
El [script](5073_3_Programazioa_Ariketak.py) y el
[notebook](5073_3_Programazioa_Ariketak.ipynb) contienen la misma secuencia.

Desde esta carpeta, `python 5073_3_Programazioa_Ariketak.py` crea
`data/dataset.csv` (2.000 filas sintéticas) y `data/eredua.pkl` (un modelo
generado localmente). Requiere `numpy`, `pandas`, `scikit-learn`, `pydantic` 2
y `joblib`. **No se ha ejecutado en esta revisión**; el código y el notebook
solo se han comprobado estáticamente. No cargues archivos `joblib` ajenos:
su deserialización puede ejecutar código.

La separación mantiene la proporción de clases y el escalador aprende solo
del conjunto de entrenamiento. `class_weight='balanced'` no garantiza mejor
recall; la comparación debe leerse junto con la matriz de confusión. La
probabilidad de la respuesta de ejemplo corresponde a la clase `1` y no es
una estimación clínica o industrial.
