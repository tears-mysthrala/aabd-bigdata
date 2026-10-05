# Iris: comparar fronteras de Logistic Regression y KNN

Resuelve el [cuaderno de clasificación](../../materialak/ikaskuntza_gainbegiratua_ikaslea.ipynb).
El [notebook resuelto y ejecutado](iris_logreg_knn.ipynb) conserva los apartados
1–6 y sus salidas. La pregunta es visual: ¿cómo separa las clases un modelo lineal frente a un
modelo basado en vecinos? El [script](iris_logreg_knn.py) usa **solo dos
atributos** de Iris: longitud y anchura del sépalo, en centímetros, para poder
dibujar el plano. Las 150 flores pertenecen a setosa, versicolor o virginica.
Los datos se cargan desde scikit-learn, sin descargar un CSV.

## Ejecución y salida

Desde la raíz del repositorio, con Python 3 y `uv` disponibles:

```bash
cd 03_ML_5072/soluzioak/Iris_LogReg_KNN
uv venv .venv
uv pip install --python .venv/bin/python numpy matplotlib scikit-learn
.venv/bin/python iris_logreg_knn.py
```

Imprime la forma `X: (150, 2)` y las accuracies; **sobrescribe**
`erabaki_mugak.png` en esta carpeta. El backend `Agg` guarda la figura sin
abrir una ventana. [El informe](txostena_beteta.md) explica las fronteras.

## Cómo interpretar la figura y las métricas

Cada punto es una flor con su clase real; el fondo representa la clase que el
modelo predice para esa posición del plano. Logistic Regression produce
fronteras lineales; KNN con k=3 se adapta localmente a las clases de sus vecinos.
Ambos se ajustan con las 150 filas y se evalúan **sobre esas mismas filas**:
los valores 0.8200/0.8533 del informe son accuracy de entrenamiento. No hay
train/test ni validación cruzada, por lo que no prueban que KNN generalice mejor.

Para comprobar el ejercicio, abre el PNG, verifica los dos ejes y modelos,
identifica el solapamiento entre versicolor y virginica y explica cómo k
cambia la flexibilidad. Este script no escala los atributos ni experimenta
con k=1; esas comparaciones son razonamientos o trabajo adicional.

No confundas esta práctica con [Orange KNN Iris](../Orange_KNN_Iris.md):
esa utiliza cuatro atributos y predicciones out-of-fold. Sus métricas responden
a un protocolo diferente y no son comparables directamente con estas.

## Notebook comprobado · 2026-10-02

Ejecutado de principio a fin con `nbclient` en CPython 3.13.13: seis celdas
Python, sin errores, `nbformat` válido y figura inline inspeccionada. Accuracy
**de entrenamiento**: LogReg 0.8200 (123/150), KNN 0.8533 (128/150). Las
matrices verifican 50/50 setosa en ambos casos. El notebook guarda una figura
con ejes en cm, leyenda y marcadores de clase en `erabaki_mugak.png`.

Para reproducir el entorno y ejecutar sin usar estado de un kernel anterior:

```bash
uv venv .venv-notebook --python 3.13
uv pip install --python .venv-notebook/bin/python -r requirements-notebook.txt
source .venv-notebook/bin/activate
python -m jupyter nbconvert --execute --to notebook --inplace iris_logreg_knn.ipynb
```

Las versiones completas están en [requirements-notebook.txt](requirements-notebook.txt).
La ejecución no incluye k=1/k=50, holdout ni CV; la reflexión explica esos
límites y propone una comparación independiente como siguiente paso.
