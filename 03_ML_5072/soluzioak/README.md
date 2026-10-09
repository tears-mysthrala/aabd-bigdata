# 03_ML_5072 — soluzioak ✅

[Entregas Moodle del 05/10/2026](Entregas_Moodle_2026-10-05/README.md): seis trabajos individuales y revisión AI4I, con informes, capturas nativas, datos y paquetes autónomos preparados por tarea.

- `5072_ML_praktika.py` / `.ipynb` (7 gelaxka): EDA + aurreprozesamendua + erregresioa + sailkapena, `cnc_mock.csv`-rekin.
- Exekuzioa, **repoaren errotik**:
  `01_Erronka1_CNC_Guard/proyecto_cnc_guard/.venv/bin/python 03_ML_5072/soluzioak/5072_ML_praktika.py`.

Datu multzo sintetikoko aurkikuntzak (`cnc_mock.csv`, 100 errenkada):
- 1 NaN `tenperatura`/`bibrazioa`-n → inputazioa beharrezkoa.
- `bibrazioa`↔`tenperatura` korrelazioa ≈ 0.03 → erregresio linealak ez du seinale linealik (MSE sentikorra outlierrekiko: teoria 2.1).
- `errorea` 95/5 desorekatua → 30 errenkadako testean positibo gutxiegi dago F1 egonkorra ondorioztatzeko. `class_weight='balanced'` aukera bat da, ez hobekuntza bermatua.

## Orange Data Mining — Praktikak eta Entregagarriak ✅

### 1. Erregresio Lineala (Linear Regression - UCI Auto MPG) 🚗
- `Orange_Erregresio_Lineala.ows`: Orange Canvas workflow irekigarria. Erabiltzen ditu `weight` (iragarlea) eta `mpg` (helburua), scatter plota, Linear Regression eta 10-fold cross-validation.
- `Orange_Erregresio_Lineala_Entregagarria.pdf`: 3 orrialdeko txostena; datuaren hautaketa, ereduaren ekuazioa, out-of-fold iragarpenen analisia eta ondorioak azaltzen ditu. Sortzailea: Unai Urzainqui Perez.
- `datos/auto_mpg/`: UCI Auto MPG jatorrizko datuak, Orange-rako taula prestatuak, deskarga/prestaketa scripta eta iturria/lizentzia dokumentatzeko READMEa. 398 auto erabiltzen dira; `horsepower`-eko falta diren balioek ez dute erabilitako `weight` eta `mpg` eragiten. [Datu multzoaren iturri ofiziala](https://archive.ics.uci.edu/dataset/9/auto).
- `datos/auto_mpg/auto_mpg_cv_metrics.json` eta `auto_mpg_cv_iragarpenak.csv`: 10 fold-eko ebaluazioaren metrikak eta auto bakoitzaren out-of-fold iragarpena/hondarra.
- `orange_erregresio_lineala.py`: Orange Python APIa erabiliz datuak berriz kargatu, eredu lineala entrenatu eta CV emaitzak sortzen ditu.
- `sortu_erregresio_ows.py`, `sortu_erregresio_pdf.py` eta `irudiak/sortu_erregresio_irudiak.py`: workflow, txostena eta hiru irudiak berreraikitzen dituzte.
- Erabilitako irudiak: `irudiak/reg_workflow.png`, `reg_scatter_ols.png` eta `reg_residuals.png`.
- Irekitzeko: `orange-canvas 03_ML_5072/soluzioak/Orange_Erregresio_Lineala.ows`

### 2. Sailkapena (Classification — Heart Disease) 🫀
- `Orange_Bihotza_Ereduak.ows`: Orange Canvas fitxategia. Test & Score-k
  jatorrizko datuak eta Preprocessor sarrera bereizita jasotzen ditu, fold
  bakoitzean inputazioa/eskalatzea ikasteko. GUIko exekuzioa ez dago baieztatuta.
- `Orange_Data_Mining_Entregagarria.pdf`: PDF entregagarri ofiziala 6 orrialdetan (10-fold CV metrikak, ROC kurbak, matrizeak eta zuhaitz-arauak).
- `orange_bihotza_ereduak.py`: Orange API bidez 10-fold CV kalkulatzeko demo; ez da ebaluazio klinikoa.
- Irekitzeko: `orange-canvas 03_ML_5072/soluzioak/Orange_Bihotza_Ereduak.ows`

### 3. Erregresio Logistikoa (UCI Breast Cancer Wisconsin Diagnostic) 🧫
- `Orange_Regresion_Logistica.ows`: Orange workflow irekigarria, `texture_mean` iragarle bakarra, `diagnosis` helburua, 10-fold CV estratifikatua, ROC Analysis, Confusion Matrix eta out-of-fold taularekin.
- `Orange_Regresion_Logistica_Entregable.pdf`: 4 orrialdeko txostena; benigno (B) eta maligno (M) masen datuak, logit eredua, out-of-fold ebaluazioa, scatter-sigmoide grafikoa eta erabilera-mugak aztertzen ditu. Sortzailea: Unai Urzainqui Perez.
- `datos/breast_cancer_wisconsin/`: UCI jatorrizko `wdbc.data`/`wdbc.names`, Orange-rako `.tab`, iturriari buruzko READMEa, CV neurriak, iragarpenak eta doikuntza osoaren sigmoide puntuak.
- `orange_erregresio_logistica.py`, `sortu_erregresio_logistica_ows.py`, `sortu_erregresio_logistica_pdf.py` eta `irudiak/sortu_logistica_irudiak.py`: datuak berreraiki, Orange eredua ebaluatu eta entregagarriak sortzen dituzte. [Iturri ofiziala: UCI Breast Cancer Wisconsin Diagnostic](https://archive.ics.uci.edu/dataset/17/breast%2Bcancer).
- [Benigno/maligno datuak eta sigmoide logistikoa](irudiak/logistica_sigmoide_clasificacion.png). X ardatza puntuazio logistikoa da (z=β₀+β₁·texture_mean), Y ardatza P(M) estimatua; laginak beren benetako 0/1 diagnostikoetan ageri dira, jitterrik gabe, eta itzalek erabaki-eremuak erakusten dituzte. Ariketa didaktikoa da, ez erabilera klinikorako.
- Irekitzeko: `orange-canvas 03_ML_5072/soluzioak/Orange_Regresion_Logistica.ows`

## Entorno y recorrido de lectura

La práctica Python básica usa NumPy, Pandas y scikit-learn. Su comando inicial
reutiliza el entorno de CNC Guard: créalo antes con `uv sync --locked` dentro
de `01_Erronka1_CNC_Guard/proyecto_cnc_guard` si no existe. Para Jupyter,
lee la nota de rutas del notebook: su código usa `__file__` y necesita adaptación
al directorio del kernel; el comando `.py` es la entrada directa documentada.

Orange es **otro entorno**: no está incluido en las dependencias base de CNC
Guard. Puedes usar una instalación de Orange existente o preparar un entorno
local desde esta carpeta, con Python compatible con sus paquetes:

```bash
uv venv .venv-orange
uv pip install --python .venv-orange/bin/python Orange3 matplotlib
.venv-orange/bin/python orange_erregresio_lineala.py
.venv-orange/bin/python orange_erregresio_logistica.py
.venv-orange/bin/python orange_bihotza_ereduak.py
.venv-orange/bin/orange-canvas Orange_Erregresio_Lineala.ows
```

Se usan rangos resueltos por el instalador, no un lock propio del bloque.
Los scripts de regresión **sobrescriben** métricas/predicciones locales; el de
Heart Disease imprime resultados y puede requerir acceso al dataset de Orange.
Los generadores `sortu_*` y `irudiak/sortu_*` regeneran workflows, PDF o figuras:
consulta sus entradas antes de ejecutarlos, para conservar entregas propias.
No hace falta regenerar esos artefactos para estudiar los existentes.

| Práctica | Pregunta y método | Cómo interpretar la entrega |
|---|---|---|
| CNC, práctica básica | ¿Cómo tratar NaN y categorías antes de regresión/clasificación? | Compara MSE con la media de train y F1/matriz con accuracy. El dato pequeño y desbalanceado limita conclusiones. |
| Auto MPG | ¿Qué relación hay entre peso (`weight`, libras) y consumo (`mpg`, millas/galón)? | Diferencia recta ajustada con todos los coches de errores **out-of-fold**. R² no es un porcentaje genérico de aciertos; RMSE/MAE están en mpg. |
| [Heart Disease](Heart_Disease_Evaluacion.md) | ¿Cómo comparar cuatro clasificadores bajo CV? | Lee métricas de la clase objetivo, matriz y ROC; el workflow y el script pueden tener preprocesamientos distintos, así que no exijas igualdad sin comparar la configuración. |
| WDBC | ¿Cómo la textura media produce P(maligno) con regresión logística? | Los puntos del scatter son diagnósticos 0/1 y la sigmoide es probabilidad de un ajuste completo. Para evaluar usa las predicciones CV, no la curva completa. |
| [Iris, fronteras 2D](Iris_LogReg_KNN/README.md) | LogReg/KNN con dos atributos y ajuste sobre todas las flores. | La accuracy es de entrenamiento, no de generalización. |
| [Iris en Orange](Orange_KNN_Iris.md) | KNN con cuatro atributos y CV de 10 folds. | Exportación corregida y validada fila a fila: CA 0.9600, 144/150 aciertos; cuatro atributos, 10 folds y seed 42. Guía y PDF regenerados el 2026-10-02. |

En Orange abre File primero y, si necesita una ruta nueva, selecciona el `.tab`
o CSV local indicado en su guía de datos. Comprueba atributos/target y después
Test & Score, ROC y Confusion Matrix. El número de clase positiva y el orden de
clases importan al interpretar probabilidades. Los datasets de salud son
material docente; sus métricas no representan validación clínica.

Las figuras y PDF son entregas derivadas. Los scripts, tablas y JSON guardados
permiten seguir sus cálculos; la presencia de una figura no certifica que el
workflow GUI se haya ejecutado con la configuración actual.

La [entrega de interpretación de datos en Orange](Interpretacion_Datos/README.md) incluye el PDF específico de la tarea 63638 con capturas reales de Iris.

## SVM — material nuevo de Moodle

[Guía SVC/SVR y notebook ejecutado](SVM/README.md): ejemplos del PDF, evaluación de entrenamiento y extensión fuera de muestra separadas. La tarea SVM - Ariketa está confirmada (05/10), con introducción vacía y sin fecha límite visible; no se realizó entrega.

## Boosting — Moodle 8 de octubre

[Cuatro ejemplos Python, tres cálculos manuales y evaluación separada](Boosting/README.md): AdaBoost, Gradient Boosting y XGBoost, con script/notebook ejecutados, lock uv y pruebas de pesos/residuos/pruning.

- [Guía visual de 20 modelos: clasificación, regresión y Boosting](Guia_Visual_Modelos/README.md), con galería offline, datos reproducibles y los 14 gráficos originales conservados.
