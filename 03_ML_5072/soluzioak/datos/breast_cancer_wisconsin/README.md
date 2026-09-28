# Wisconsin Breast Cancer Diagnostic - regresión logística

Este ejercicio usa el conjunto **Breast Cancer Wisconsin (Diagnostic)** de UCI. Cada fila describe características numéricas de núcleos celulares calculadas a partir de una imagen digital de una aspiración con aguja fina (FNA) de una masa mamaria. El objetivo distingue **B** (benigno) de **M** (maligno); hay 569 muestras, 357 benignas y 212 malignas, sin valores ausentes.

Para mostrar más solapamiento entre las clases se usa un solo predictor: `texture_mean` (media de la desviación estándar de los niveles de gris en la imagen del núcleo celular). El archivo Orange conserva únicamente ese predictor y `diagnosis`; `sample_id` queda como meta para rastrear las salidas. Las otras 29 características originales siguen disponibles en `wdbc.data` pero no entran en este modelo univariable.

La gráfica usa la puntuación logística `z = β0 + β1 · texture_mean` en X y `P(M) = σ(z)` en Y, con las muestras observadas en sus etiquetas binarias exactas: B=0 o M=1. No se desplazan los puntos con jitter. Las regiones muestran la clasificación a cada lado de `z=0`, `P(M)=0,5`. El rendimiento se evalúa aparte con validación cruzada de 10 folds.

**Uso didáctico, no clínico.** Son mediciones históricas de una colección concreta; un único predictor no representa una valoración médica completa, no debe diagnosticar ni guiar decisiones sobre pacientes y no demuestra causalidad.

Fuente: Wolberg, W., Mangasarian, O., Street, N. y Street, W. (1993), [UCI Breast Cancer Wisconsin (Diagnostic)](https://archive.ics.uci.edu/dataset/17/breast%2Bcancer), DOI [10.24432/C5DW2B](https://doi.org/10.24432/C5DW2B), licencia CC BY 4.0.

Regenerar la tabla Orange:

```bash
python 03_ML_5072/soluzioak/datos/breast_cancer_wisconsin/preparatu_breast_cancer.py
```
