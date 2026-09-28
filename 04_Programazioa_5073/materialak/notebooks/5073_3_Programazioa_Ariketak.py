#!/usr/bin/env python3
# Auto-converted from 5073_3_Programazioa_Ariketak.ipynb
# Executable in VS Code (supports # %% interactive cells) or terminal via `python3`.


# %% [markdown] Cell 1
# # 03 Programazioa - Ariketak
#
# Helburua: Machine Learning eta API garapenerako oinarriak lantzea.


# %% [markdown] Cell 2
# ## Setup (Datuen sorkuntza)
# Exekutatu beheko gelaxka `data` karpeta eta beharrezko fitxategiak sortzeko.


# %% [code] Cell 3
# @title
import os
import pandas as pd
from sklearn.datasets import make_classification

os.makedirs('data', exist_ok=True)
X, y = make_classification(n_samples=2000, n_features=20, n_classes=2, weights=[0.9, 0.1], random_state=42)
df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(20)])
df['target'] = y
df.to_csv('data/dataset.csv', index=False)
print("✅ Datuak ondo sortu eta 'data/dataset.csv' fitxategian gorde dira!")
del X, y, df  # 1.1 eta 1.2 ariketek aldagai hauek berriro sortu behar dituzte.


# %% [markdown] Cell 4
# ## 1. Atala: Scikit-Learn Split eta Leakage
# ### 1.1 Ariketa: Datuak Kargatu
# Kargatu `data/dataset.csv` fitxategia Pandas bidez `df` izeneko aldagai batean.


# %% [code] Cell 5
import pandas as pd

# Zure kodea hemen:


# Balioztatzea (EZ UKITU)
assert 'df' in locals(), "'df' aldagaia ez da sortu"
assert type(df) == pd.DataFrame, "'df' ez da Pandas DataFrame bat"
assert df.shape == (2000, 21), "Datuen tamaina ez da zuzena"
print("✅ Zuzena!")


# %% [markdown] Cell 6
# ### 1.2 Ariketa: X eta y banatu
# Sortu bi aldagai: `X` (ezaugarri guztiak 'target' izan ezik) eta `y` ('target' zutabea).


# %% [code] Cell 7
# Zure kodea hemen:

# Balioztatzea
assert 'X' in locals() and 'y' in locals(), "Aldagaiak falta dira"
assert X.shape == (2000, 20), "X-ren dimentsioak ez dira zuzenak"
assert y.shape == (2000,), "y-ren dimentsioak ez dira zuzenak"
print("✅ Zuzena!")


# %% [markdown] Cell 8
# ### 1.3 Ariketa: Train/Test banaketa
# Erabili `train_test_split` datuak banatzeko. Train %80 eta Test %20. Erabili `random_state=42`.


# %% [code] Cell 9
from sklearn.model_selection import train_test_split
# Zure kodea hemen:

# Balioztatzea
assert X_train.shape[0] == 1600, "Train multzoa ez da %80"
assert X_test.shape[0] == 400, "Test multzoa ez da %20"
print("✅ Zuzena!")


# %% [markdown] Cell 10
# ### 1.4 Ariketa: Data Leakage saihestea (StandardScaler)
# Sortu `StandardScaler` bat. Erabili `.fit_transform()` `X_train` multzoan eta gorde `X_train_scaled` aldagaian. Ondoren erabili `.transform()` `X_test` multzoan eta gorde `X_test_scaled` aldagaian.


# %% [code] Cell 11
from sklearn.preprocessing import StandardScaler
# Zure kodea hemen:


# Balioztatzea
assert X_train_scaled.shape == (1600, 20), "Dimentsioak ez daude ondo"
print("✅ Zuzena!")


# %% [markdown] Cell 12
# ### 1.5 Ariketa: Egiaztapena
# Egiaztatu `X_train_scaled` barruan lehenengo zutabearen batezbestekoa ia 0 dela.


# %% [code] Cell 13
import numpy as np
# Zure kodea hemen:

# Balioztatzea
assert abs(batezbestekoa) < 1e-10, "Batezbestekoa ez dago 0tik oso gertu"
print("✅ Zuzena!")


# %% [markdown] Cell 14
# ## 2. Atala: Metrikak (Accuracy vs Recall)
#


# %% [markdown] Cell 15
# ### 2.1 Ariketa: Logistic Regression
# Sortu eta entrenatu `LogisticRegression` eredu bat (`model_lr` aldagaian) `X_train_scaled` eta `y_train` erabiliz.


# %% [code] Cell 16
from sklearn.linear_model import LogisticRegression
# Zure kodea hemen:

# Balioztatzea
assert 'model_lr' in locals(), "Eredua ez da sortu"
assert hasattr(model_lr, 'coef_'), "Eredua ez dago entrenatuta"
print("✅ Zuzena!")


# %% [markdown] Cell 17
# ### 2.2 Ariketa: Iragarpenak
# Egin iragarpenak `X_test_scaled` erabiliz eta gorde `y_pred` aldagaian.


# %% [code] Cell 18
# Zure kodea hemen:

# Balioztatzea
assert len(y_pred) == 400, "Iragarpenen kopurua ez da 400"
print("✅ Zuzena!")


# %% [markdown] Cell 19
# ### 2.3 Ariketa: Accuracy
# Kalkulatu 'Accuracy' (zehaztasuna) eta gorde `acc` aldagaian.


# %% [code] Cell 20
from sklearn.metrics import accuracy_score
# Zure kodea hemen:


# Balioztatzea
assert 0 <= acc <= 1, "Accuracy balioa ez da zuzena"
print(f"✅ Zuzena! Accuracy = {acc:.4f}")


# %% [markdown] Cell 21
# ### 2.4 Ariketa: Recall
# Kalkulatu 'Recall' (sentsibilitatea) eta gorde `rec` aldagaian.


# %% [code] Cell 22
from sklearn.metrics import recall_score
# Zure kodea hemen:

# Balioztatzea
assert 0 <= rec <= 1, "Recall balioa ez da zuzena"
print(f"✅ Zuzena! Recall = {rec:.4f}")


# %% [markdown] Cell 23
# ### 2.5 Ariketa: Confusion Matrix
# Sortu konfusio-matrizea (`cm` aldagaian) `confusion_matrix` erabiliz.


# %% [code] Cell 24
from sklearn.metrics import confusion_matrix
# Zure kodea hemen:


# Balioztatzea
assert cm.shape == (2, 2), "Matrizeak 2x2 izan behar du"
print(f"✅ Zuzena!\n{cm}")


# %% [markdown] Cell 25
# ## 3. Atala: Klase Desorekatuak
#


# %% [markdown] Cell 26
# ### 3.1 Ariketa: Klaseen Banaketa
# Erabili `.value_counts()` `y_train` aldagaian train multzoko klaseen banaketa ikusteko (`counts` aldagaian gorde).


# %% [code] Cell 27
# Zure kodea hemen:

# Balioztatzea
assert len(counts) == 2, "Bi klase egon beharko lirateke"
print(f"✅ Zuzena!\n{counts}")


# %% [markdown] Cell 28
# ### 3.2 Ariketa: Eredu Orekatu bat entrenatu
# Sortu `LogisticRegression` berri bat (`model_balanced`) `class_weight='balanced'` argumentuarekin, eta entrenatu.


# %% [code] Cell 29
# Zure kodea hemen:

# Balioztatzea
assert model_balanced.class_weight == 'balanced', "class_weight ez da 'balanced'"
print("✅ Zuzena!")


# %% [markdown] Cell 30
# ### 3.3 Ariketa: Konparatu Recall-ak
# Egin iragarpenak eredu berriarekin eta kalkulatu recall berria (`rec_balanced`).


# %% [code] Cell 31
# Zure kodea hemen:

# Balioztatzea
assert 0 <= rec_balanced <= 1, "Recall balioa ez da zuzena"
# class_weight='balanced' ez da recall handiagoaren bermea; konparatu emaitzak.
print(f"✅ Zuzena! Aurrekoa: {rec:.4f} -> Orekatu ondoren: {rec_balanced:.4f}")


# %% [markdown] Cell 32
# ### 3.4 Ariketa: Random Forest
# Orain probatu `RandomForestClassifier` batekin (`rf_balanced`), `class_weight='balanced_subsample'` erabiliz.


# %% [code] Cell 33
from sklearn.ensemble import RandomForestClassifier
# Zure kodea hemen:

# Balioztatzea
assert rf_balanced.class_weight == 'balanced_subsample', "Ez duzu class_weight egokia erabili"
print("✅ Zuzena!")


# %% [markdown] Cell 34
# ### 3.5 Ariketa: Egiaztatu Random Forest Recall-a
# Kalkulatu Random Forest ereduaren iragarpenak eta atera recall-a (`rf_rec`).


# %% [code] Cell 35
# Zure kodea hemen:

# Balioztatzea
assert 0 <= rf_rec <= 1, "Recall balioa ez da zuzena"
print(f"✅ Zuzena! Random Forest Recall = {rf_rec:.4f}")


# %% [markdown] Cell 36
# ## 4. Atala: Pipeline eta Joblib
#


# %% [markdown] Cell 37
# ### 4.1 Ariketa: Pipeline-a sortu
# Sortu `Pipeline` bat bi pausorekin: 1) `StandardScaler` ('scaler') eta 2) `RandomForestClassifier(class_weight='balanced')` ('classifier'). Gorde `pipeline` aldagaian.


# %% [code] Cell 38
from sklearn.pipeline import Pipeline
# Zure kodea hemen:

# Balioztatzea
assert len(pipeline.steps) == 2, "Pipeline-ak bi pauso eduki behar ditu"
assert 'scaler' in pipeline.named_steps, "Ez dago 'scaler' pausorik"
assert 'classifier' in pipeline.named_steps, "Ez dago 'classifier' pausorik"
print("✅ Zuzena!")


# %% [markdown] Cell 39
# ### 4.2 Ariketa: Pipeline-a entrenatu
# Entrenatu `pipeline` zuzenean *datu gordinekin* (`X_train` eta `y_train`), Pipelineak berak egingo baitu eskalatzea barnean.


# %% [code] Cell 40
# Zure kodea hemen:

# Balioztatzea
assert hasattr(pipeline, 'classes_'), "Pipeline ez dago entrenatuta"
print("✅ Zuzena!")


# %% [markdown] Cell 41
# ### 4.3 Ariketa: Pipeline Iragarpenak
# Egin iragarpena `X_test` (gordina) erabiliz eta kalkulatu Accuracy (`pipe_acc`).


# %% [code] Cell 42
# Zure kodea hemen:

# Balioztatzea
assert 0 <= pipe_acc <= 1, "Accuracy okerra da"
print(f"✅ Zuzena! Pipeline Accuracy = {pipe_acc:.4f}")


# %% [markdown] Cell 43
# ### 4.4 Ariketa: Eredua Gorde
# Erabili `joblib.dump` liburutegia entrenatutako `pipeline` eredua `data/eredua.pkl` fitxategian gordetzeko.


# %% [code] Cell 44
import joblib
# Zure kodea hemen:


# Balioztatzea
assert os.path.exists('data/eredua.pkl'), "Eredua ez da fitxategian aurkitu"
print("✅ Zuzena!")


# %% [markdown] Cell 45
# ### 4.5 Ariketa: Eredua Kargatu
# Erabili `joblib.load` eredua disko batetik kargatzeko (`eredu_kargatua`), eta frogatu testeko lehen instantziarekin iragarpena egiten.


# %% [code] Cell 46
# Zure kodea hemen:

# Balioztatzea
assert iragarpen_1[0] in [0, 1], "Iragarpena ez da klase logikoa"
print(f"✅ Zuzena! Lehenengo instantziaren iragarpena: {iragarpen_1[0]}")


# %% [markdown] Cell 47
# ## 5. Atala: Pydantic eta API Eskemak
# ### 5.1 Ariketa: Request Eskema
# Sortu `PredictionRequest` Pydantic `BaseModel` bat. `features` izeneko lista bat izango du, `float` motako elementuekin (`List[float]`).


# %% [code] Cell 48
from pydantic import BaseModel, ValidationError, field_validator
from typing import List

# Zure kodea hemen:


# Balioztatzea
assert issubclass(PredictionRequest, BaseModel), "Ez da BaseModel-etik heredatzen"
print("✅ Zuzena!")


# %% [markdown] Cell 49
# ### 5.2 Ariketa: Balioztatze pertsonalizatua (@field_validator)
# Berridatzi eredua: gehitu `@field_validator('features')` funtzio bat, listaren luzera zehazki 20 ez bada `ValueError` bat jaurtitzeko.


# %% [code] Cell 50
# Zure kodea hemen:

# Balioztatzea (hurrengo ariketan egingo da)


# %% [markdown] Cell 51
# ### 5.3 Ariketa: Error kudeaketa (ValidationError)
# Sortu instantzia bat 3 elementurekin soilik, eta erabili `try/except ValidationError` bloke bat errorea ondo harrapatzeko eta mezua inprimatzeko.


# %% [code] Cell 52
# Zure kodea hemen:


# Balioztatzea
assert errorea_dago, "Errorea ez da jaurti eta harrapatu ValidationError bezala"
print("\n✅ Zuzena! Errorea ondo harrapatu da.")


# %% [markdown] Cell 53
# ### 5.4 Ariketa: Response Eskema
# Sortu `PredictionResponse` BaseModel bat, `klasea` (int) eta `probabilitatea` (float) eremuekin.


# %% [code] Cell 54
# Zure kodea hemen:

# Balioztatzea
assert issubclass(PredictionResponse, BaseModel), "Ez da BaseModel"
print("✅ Zuzena!")


# %% [markdown] Cell 55
# ### 5.5 Ariketa: API funtzio simulatua
# Sortu `egin_iragarpena(req: PredictionRequest) -> PredictionResponse` funtzio bat. Funtzio horrek `eredu_kargatua` erabiliko du `req.features` bektorea iragartzeko (gogoratu 2D array gisa pasa behar dela sklearn-era) eta erantzuna itzuliko du.


# %% [code] Cell 56
import numpy as np

# Zure kodea hemen:


# Balioztatzea
req_test = PredictionRequest(features=[0.0]*20)
resp = egin_iragarpena(req_test)
assert isinstance(resp, PredictionResponse), "Ez du PredictionResponse bat itzuli"
print(f"✅ Zuzena! Test erantzuna: {resp.model_dump()}")
