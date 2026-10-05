# SVC y SVR con escalado

Esta práctica reproduce los dos ejemplos de **Python Inplementazioa**, página
física 9 (diapositiva «8 · Praktika») de
[5072_2_05_SVM.pdf](../../materialak/5072_2_05_SVM.pdf).
Existe la tarea [SVM - Ariketa en Moodle](https://elearning20.hezkuntza.net/012053/mod/assign/view.php?id=63380),
confirmada en la sesión autenticada del 05/10/2026. Su introducción está vacía;
solo aparece apertura el viernes 11/09/2026 a las 00:00, sin fecha límite visible.
El PDF ofrece ejemplos y no añade una consigna de entrega. Esta solución
educativa prepara esos ejemplos; no demuestra entrega ni cobertura de una
rúbrica o requisitos que no están visibles.

## Objetivo y archivos

[SVM ejecutable](svm_adibideak.py) y [notebook ejecutado](svm_adibideak.ipynb)
contienen los mismos datos y parámetros docentes: cuatro puntos para SVC;
diez filas aleatorias con cinco variables para SVR, `RandomState(0)`, generando
primero `y` y después `X`. Ambos modelos usan `StandardScaler` en un pipeline.
[emaitzak.json](emaitzak.json) conserva métricas, semillas y versiones verificadas.

SVC clasifica y `score` calcula accuracy; SVR predice un valor continuo y
`score` calcula R². Accuracy y R² no son porcentajes comparables. Un R² negativo
significa que esas predicciones son peores que usar la media de los valores
reales evaluados, según la definición de R².

## Preparación y ejecución

Desde la raíz del repositorio, con `uv` y Python 3.13:

```bash
cd 03_ML_5072/soluzioak/SVM
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python -r requirements-notebook.txt
.venv/bin/python svm_adibideak.py
```

Los pins principales coinciden con el entorno comprobado (NumPy 2.5.3,
scikit-learn 1.9.1, SciPy 1.18.1); no constituyen un lock de dependencias
transitivas. La ejecución del 05/10/2026 reutilizó el entorno `uv` ya existente
de Programación, sin instalar paquetes ni abrir servicios. El script resuelve
su carpeta desde `__file__` y funciona desde otra carpeta. Para el notebook,
selecciona ese intérprete y fija esta carpeta como directorio del kernel;
ejecuta todas las celdas en orden. El script/notebook actualiza solo
`emaitzak.json` en esta carpeta y no descarga datos.

## Resultados ejecutados el 05/10/2026

| Evaluación | Resultado | Interpretación |
|---|---:|---|
| SVC literal del PDF, entrenamiento, 4 filas | accuracy = 1,000000 | Clasifica bien los puntos que acaba de ver. No prueba generalización. |
| SVR literal del PDF, entrenamiento, 10 filas | R² = 0,576086 | Ajuste sobre los datos usados en `fit`. |
| SVC en Iris, entrenamiento, 105 filas | accuracy = 0,971429 | Extensión didáctica; no es el ejemplo de cuatro puntos del PDF. |
| SVC en Iris, test reservado, 45 filas | accuracy = 0,933333 | División estratificada 70/30, `random_state=42`, sin elegir parámetros con test. |
| SVR del PDF, predicciones fuera de muestra | R² = −0,443113; MAE = 1,033263 | Cinco folds con barajado, `random_state=42`; cada fila se predice sin entrenar con ella. |
| Baseline de media, mismos folds | R² = −0,176541; MAE = 0,894594 | En esta muestra, SVR obtiene peor resultado que el predictor de media. |

Las predicciones de todos los folds se juntan antes de calcular R²: es un
**R² OOF global**, no el promedio de cinco R² calculados sobre dos filas.
El baseline usa la media de entrenamiento de cada fold. `StandardScaler`
se ajusta dentro del pipeline en cada división; escalar todo el dataset antes
de separar entrenamiento/test filtraría información del test.

## Cómo interpretar y validar

1. Ejecuta el script y compara el JSON con esta tabla; semillas y versiones
   permiten repetir los datos y el cálculo.
2. En el notebook identifica qué filas usa cada `fit` y qué filas usa cada
   `score`. El `score(X, y)` literal del PDF usa entrenamiento.
3. Observa que SVR obtiene R² positivo en entrenamiento y negativo fuera de
   muestra. `X` e `y` se generan aleatoriamente, sin relación diseñada entre
   ellos; no hay motivo para esperar buena capacidad predictiva.

El script y todas las celdas del notebook nuevo se ejecutaron sin errores.
La división Iris es una sola partición y SVR tiene únicamente diez filas;
ninguna cifra garantiza rendimiento en datos nuevos reales. No se realizó
búsqueda de hiperparámetros, validación externa, publicación ni entrega en la
tarea confirmada. Los textos de alcance se actualizaron tras comprobar Moodle;
los resultados numéricos conservan la ejecución local anterior y no se repitieron
los experimentos para este ajuste documental.
