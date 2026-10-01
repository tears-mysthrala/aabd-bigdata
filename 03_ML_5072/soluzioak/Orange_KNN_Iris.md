# KNN con Iris — informe de conclusiones

Asignatura 5072 · assign 63321. Workflow:
[`Orange_KNN_Iris.ows`](Orange_KNN_Iris.ows) (File → kNN k=3 →
Test & Score 10-fold estratificada → Confusion Matrix + Data Table).
Datos: [`datos/iris/iris.csv`](datos/iris/iris.csv) (150 flores).
Predicciones out-of-fold:
[`datos/iris/iris_knn_predicciones.csv`](datos/iris/iris_knn_predicciones.csv).

## Datos elegidos

Iris (150 muestras, 4 medidas, 3 clases). Clásico para KNN: el algoritmo
vive de distancias y aquí se ve en estado puro.

## Modelo aplicado

`KNNLearner(n_neighbors=3)`, distancia euclídea, 10-fold CV estratificada.

## Resultados documentados: requieren reconciliación

**Incidencia detectada en la revisión documental:** 90 de las 150 etiquetas
`iris_real` del CSV de predicciones no corresponden a las medidas de la misma
fila en `iris.csv`/Iris de scikit-learn. El CSV de entrada sí coincide con ese
dataset. Por tanto, el export de predicciones no permite acreditar estas
métricas por muestra hasta corregir su alineación y repetir la evaluación.
No se han cambiado datos ni recalculado resultados en esta revisión.

- **CA (10-fold): 0.9533** (143/150). Por k: k=1 → 0.96, k=3/5/9 → 0.9533,
  k=15 → 0.9667.
- Matriz (filas reales): setosa 50/0/0, versicolor 0/46/4, virginica 0/3/47.

## Conclusiones

1. La matriz guardada no contiene errores de setosa; los 7 fallos son
   confusiones entre versicolor y virginica. La matriz por sí sola no demuestra
   si la causa es solapamiento, ruido o una limitación del modelo.
2. k=1 obtiene algo más de accuracy en esta evaluación; k pequeño permite
   fronteras más sensibles a los vecinos. k=15 da 0.9667 en el resultado
   documentado: elegirlo después de comparar estas métricas requeriría otra
   evaluación independiente para estimar el rendimiento del modelo elegido.
3. KNN no aprende pesos: con 4 medidas a escalas parecidas funciona;
   con magnitudes dispares habría que normalizar (como en 03-01/03-02).

## Cómo abrir, reproducir e interpretar

Con Orange instalado, desde la raíz:

```bash
orange-canvas 03_ML_5072/soluzioak/Orange_KNN_Iris.ows
```

En File selecciona `datos/iris/iris.csv` respecto a la carpeta `soluzioak`
si la ruta guardada no se resuelve. Comprueba cuatro atributos numéricos y
`iris` como clase. En kNN, k=3 y distancia euclídea; en Test & Score, CV
estratificada de 10 folds. File envía Data directamente a Test & Score y kNN
le envía el Learner; el widget entrena un modelo por fold. Si añades escalado,
haz que se ajuste dentro de cada fold, evitando preprocesar toda la tabla antes.

`CA` es accuracy: diagonal de la matriz / 150. Las filas son clases reales y
las columnas predichas. El [JSON guardado](datos/iris/knn_iris.json) contiene la matriz y los 143
aciertos declarados. El CSV de predicciones tiene la incidencia de alineación
descrita arriba: comprobar que una suma coincida no valida el emparejamiento
entre features y etiquetas. El archivo no registra una
semilla de partición que permita exigir igualdad exacta en cualquier entorno;
guarda versión y configuración si reproduces la evaluación. Esta revisión no
ha vuelto a ejecutar el workflow ni ha recalculado sus métricas.

La [práctica visual LogReg/KNN](Iris_LogReg_KNN/README.md) utiliza dos atributos
y accuracy de entrenamiento: responde a otra pregunta y sus valores no deben
compararse directamente con esta CV.
