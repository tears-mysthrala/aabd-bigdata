# 5073, tema 3: cuaderno de ML y API

Soluciones de referencia para los 25 ejercicios de
[5073_3_Programazioa_Ariketak.ipynb](../../materialak/notebooks/5073_3_Programazioa_Ariketak.ipynb).
El [script](5073_3_Programazioa_Ariketak.py) y el
[notebook](5073_3_Programazioa_Ariketak.ipynb) comparten los ejercicios base.
El script contiene también ampliaciones de Drive; el notebook explica esa
diferencia y enlaza su código, pero no incorpora sus celdas ejecutables.

## Preparación y ejecución

Desde la raíz del repositorio, con Python 3 y `uv`:

```bash
cd 04_Programazioa_5073/soluzioak/06_Programazioa_Ariketak
uv venv .venv
uv pip install --python .venv/bin/python numpy pandas scikit-learn 'pydantic>=2,<3' joblib imbalanced-learn matplotlib
.venv/bin/python 5073_3_Programazioa_Ariketak.py
```

Este bloque no tiene lock propio: anota las versiones si comparas ejecuciones.
Los comandos parten de esta carpeta porque el script usa rutas relativas.
Sobrescribe `data/dataset.csv`, `data/eredua.pkl` y `grafikoa_3_8_pr.png`;
usa una copia para conservar resultados propios. Para Jupyter selecciona ese
intérprete, reinicia el kernel y ejecuta las celdas en orden.

**No se ha ejecutado en esta revisión documental.** El
[registro de 2026-09-28](../egiaztapena_2026-09-28.md) corresponde a los ejercicios
base, antes de las ampliaciones actuales. No cargues archivos joblib/pickle
ajenos: su deserialización puede ejecutar código; 4.5 carga el modelo que 4.4
acaba de generar localmente.

## Recorrido de los 25 ejercicios base

| Bloque | Método y resultado que debes interpretar |
|---|---|
| Preparación | 2.000 filas sintéticas, 20 atributos y `target` con desbalance aproximado 90/10; seed 42. No representan pacientes ni procesos reales. |
| 1.1–1.5 | Split estratificado 80/20 y escalado aprendido solo de train. La media de train queda cerca de 0; test no tiene por qué quedar centrado exactamente. |
| 2.1–2.5 | Regresión logística, accuracy, recall clase 1 y matriz de confusión (filas reales/columnas predichas). Recall = TP/(TP+FN); accuracy puede ocultar errores de la minoría. |
| 3.1–3.5 | Compara pesos de clase y Random Forest sobre el mismo test. `class_weight='balanced'` no garantiza mejora; un recall mayor puede acompañarse de más falsos positivos. |
| 4.1–4.5 | Pipeline de escalador+modelo, guardado y carga del artefacto propio. Pasar datos ya escalados al Pipeline produciría doble escalado. |
| 5.1–5.5 | Pydantic exige 20 atributos en la petición final; la función reconstruye su orden y devuelve clase y **P(clase 1)**, incluso si predice 0. No arranca un servidor HTTP; la probabilidad no es una estimación clínica o industrial. |

## Ampliaciones Drive: numeración distinta

El script añade 6.1 (request inicial con `list[float]`), 3.5–3.8
(SMOTE en train, RF, curva Precision–Recall y umbral `>0.30`) y 4.1
(GridSearchCV). Estos números reutilizan IDs de la versión base: identifica
la edición del enunciado antes de relacionar un resultado con un ejercicio.

SMOTE interpola ejemplos minoritarios de **train**; no modifica test. La curva
PR combina precision = TP/(TP+FP) y recall al variar el umbral. Bajarlo puede
mantener/subir recall, a costa de más falsos positivos; no demuestra mejora
global. El PNG se llama `grafikoa_3_8_pr.png`, aunque lo genera el paso 3.7.

El GridSearch actual usa el scoring por defecto de Random Forest (**accuracy**),
no optimiza recall. Recibe datos escalados antes de sus folds: para validar un
preprocesamiento dentro de CV habría que incluirlo en el Pipeline del buscador.
Aquí el bosque no necesita ese escalado, pero este ejemplo no debe extrapolarse
a un buscador de modelos sensibles a la escala. Los valores de CV no son una
evaluación final independiente del modelo seleccionado.
