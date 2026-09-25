# 03_ML_5072 — soluzioak ✅

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
