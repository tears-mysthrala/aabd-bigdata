#!/usr/bin/env python3
# Auto-converted from 5073_3_Programazioa.ipynb
# Executable in VS Code (supports # %% interactive cells) or terminal via `python3`.


# %% [markdown] Cell 1
# # 3. Gaia · AA Frameworka — Python adibideak
#
# Notebook honek 3. gaiko (`AA Programazioa eta GenAI`) Python adibide guztiak biltzen ditu, gelan zuzenean exekutatu eta esperimentatzeko prest. Atalez atal jarraitzen du dokumentu didaktikoaren ordena:
#
# 1. **Scikit-Learn** — Ikasketa automatiko klasikoa
# 2. **Hugging Face** — Eredu aurreentrenatuak
# 3. **FastAPI** — REST API-ak (scriptak)
# 4. **Streamlit** — Datu-aplikazioak (scriptak)
# 5. **LangChain + Gemini** — LLM aplikazioak
# 6. **RAG** — Berreskurapen-oinarritutako sorkuntza
# 7. **Proiektu integratzailea** — RAG + Gemini API
#
# > **Oharra**: §3 (FastAPI) eta §4 (Streamlit) atalek script independenteak behar dituzte exekutatzeko (`uvicorn`/`streamlit run`). Notebook-ean kodea ageri da erreferentzia gisa.
# >
# > §5, §6 eta §7 atalek **`GOOGLE_API_KEY`** ingurune-aldagaia behar dute Gemini erabiltzeko ([Google AI Studio](https://aistudio.google.com/apikey)-tik doan lortzen da).
#


# %% [markdown] Cell 2
# ## Setup (inportazio globalak eta paketeen instalazioa)
#
# Hurrengo paketeak behar dira notebook hau exekutatzeko. Lehen exekuzioan instalatu (komentatuta dago):
#


# %% [code] Cell 3
# Instalazio paketeak (deskomentatu behar bada)
# Notebook shell: !pip install scikit-learn matplotlib seaborn pandas numpy
# Notebook shell: !pip install transformers datasets tokenizers torch
# Notebook shell: !pip install fastapi "uvicorn[standard]" pydantic
# Notebook shell: !pip install streamlit
# !pip install langchain langchain-google-genai langchain-community python-dotenv
# !pip install faiss-cpu pypdf



# %% [code] Cell 4
# Inportazio globalak — atal bakoitzak bere espezifikoak ere baditu
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# sklearn oinarrizkoa
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, GridSearchCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Ausazkotasuna kontrolatu
np.random.seed(42)



# %% [markdown] Cell 5
# ---
# # 1. Scikit-Learn: Ikasketa automatikoaren programazioa
#
# Atal honetan ML-proiektu baten ohiko urratsak landuko ditugu Scikit-Learn-ekin: datuak kargatu, aurreprozesatu, eredua entrenatu, ebaluatu eta hiperparametroak doitu.
#
#
#


# %% [markdown] Cell 6
# ## 1.1 Lan-fluxu klasikoa (5 urratsak)


# %% [code] Cell 7
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# 1. Datuak kargatu
X, y = load_iris(return_X_y=True)

# 2. Entrenamendu eta test multzoak banatu
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Aurreprozesatu
scale = StandardScaler()  # Z-Score egiten du eta balio guztiak estandarizatzen (homogeneizatzen ditu)
X_train = scale.fit_transform(X_train)   # fit + transform (entrenamendu datuetan)


# 4. Eredua entrenatu
X_test  = scale.transform(X_test)          # transform soilik (test datuetan!)
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)

# 5. Iragarpenak egin eta ebaluatu
prediction = model.predict(X_test)
print(f"Zehaztasuna: {accuracy_score(y_test, prediction):.3f}")



# %% [markdown] Cell 8
# ## 1.2 Aurreprozesatzea eta transformatzaileak
#
# ### Zenbakizko aldagaien eskala-aldaketa
#


# %% [code] Cell 9
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import numpy as np

X = np.array([[1, 100], [2, 200], [3, 300], [4, 400], [5, 500]], dtype=float)

# StandardScaler: (x - batezbestekoa) / desbideratze tipikoa -> batezbestekoa 0, desb. 1 (z-score da)
std = StandardScaler()
print("StandardScaler:")
print(std.fit_transform(X))

# MinMaxScaler: (x - min) / (max - min) -> [0, 1] tartean (normalizazioa da)
mm = MinMaxScaler()
print("\nMinMaxScaler:")
print(mm.fit_transform(X))

# RobustScaler: mediana eta kuartilak -> outlier-ei erresistente
rb = RobustScaler()
print("\nRobustScaler:")
print(rb.fit_transform(X))



# %% [markdown] Cell 10
# ### Kategoria-aldagaiak kodetu


# %% [code] Cell 11
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import numpy as np

# LabelEncoder: helburuko aldagairako (y)
le = LabelEncoder()
y = ["katu", "txakur", "katu", "txori", "txakur"]
print("LabelEncoder:", le.fit_transform(y))   # [0, 2, 0, 1, 2]
print("Klaseak:    ", le.classes_)            # ['katu', 'txori', 'txakur']

# OneHotEncoder: ezaugarri-aldagaietarako (X)
ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
X_kat = np.array([["bilbo"], ["donostia"], ["gasteiz"], ["bilbo"]])
print("\nOneHotEncoder:")
print(ohe.fit_transform(X_kat))



# %% [markdown] Cell 12
# ### Balio faltadunak bete (imputation)


# %% [code] Cell 13
from sklearn.impute import SimpleImputer
import numpy as np

X = np.array([[1, 2, np.nan], [3, np.nan, 6], [np.nan, 8, 9], [4, 5, 6]])

# Estrategiak: "mean", "median", "most_frequent", "constant"
imp = SimpleImputer(strategy="mean")
print(imp.fit_transform(X))



# %% [markdown] Cell 14
# ### ColumnTransformer: zutabe mota desberdinak aldi berean


# %% [code] Cell 15
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
import pandas as pd, numpy as np

df = pd.DataFrame({
    "adina":    [25, 30, np.nan, 35, 28],
    "lan_urte": [2, 5, 3, 7, 4],
    "hiria":    ["Bilbo", "Donostia", None, "Bilbo", "Gasteiz"],
})
zenbakizkoak = ["adina", "lan_urte"]
kategorikoak = ["hiria"]

aurreprozesatzailea = ColumnTransformer(transformers=[
    ("zenbak", Pipeline([
        ("bete",   SimpleImputer(strategy="mean")),
        ("eskala", StandardScaler())
    ]), zenbakizkoak),
    ("kateg", Pipeline([
        ("bete", SimpleImputer(strategy="most_frequent")),
        ("ohe",  OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ]), kategorikoak),
])
emaitza = aurreprozesatzailea.fit_transform(df)
print("Emaitzaren forma:", emaitza.shape)
print(emaitza)



# %% [markdown] Cell 16
# ## 1.3 Sailkapen-ereduak
#
# Hainbat sailkatzaile probatzen ditugu bular-minbiziaren datu-multzo binarioan.
#


# %% [code] Cell 17
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC

# Datu-multzoa: bular-minbiziaren detekzioa (sailkapen binarioa)
X, y = load_breast_cancer(return_X_y=True)
X_ent, X_test, y_ent, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
eskala = StandardScaler()
X_ent = eskala.fit_transform(X_ent)
X_test = eskala.transform(X_test)

ereduak = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest":       RandomForestClassifier(n_estimators=100, random_state=42),
    "Gradient Boosting":   GradientBoostingClassifier(n_estimators=100, random_state=42),
    "SVM":                 SVC(kernel="rbf", probability=True, random_state=42),
}
for izena, eredua in ereduak.items():
    eredua.fit(X_ent, y_ent)
    print(f"\n{izena}:")
    print(classification_report(y_test, eredua.predict(X_test)))



# %% [markdown] Cell 18
# ### Ebaluazio-metrikak: zehaztasuna ez da nahikoa


# %% [code] Cell 19
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, confusion_matrix)
import matplotlib.pyplot as plt
import seaborn as sns

rf = ereduak["Random Forest"]
y_irag  = rf.predict(X_test)
y_proba = rf.predict_proba(X_test)[:, 1]

print(f"Zehaztasuna:   {accuracy_score(y_test, y_irag):.4f}")
print(f"Doitasuna:     {precision_score(y_test, y_irag):.4f}")
print(f"Estaldura:     {recall_score(y_test, y_irag):.4f}")
print(f"F1 puntuazioa: {f1_score(y_test, y_irag):.4f}")
print(f"ROC-AUC:       {roc_auc_score(y_test, y_proba):.4f}")

# Nahasketaren matrizea
nahasket = confusion_matrix(y_test, y_irag)
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(nahasket, annot=True, fmt="d", cmap="Blues", ax=ax,
            xticklabels=["Negatiboa", "Positiboa"],
            yticklabels=["Negatiboa", "Positiboa"])
ax.set_ylabel("Benetako etiketa")
ax.set_xlabel("Iragarritako etiketa")
plt.tight_layout()
plt.show()



# %% [markdown] Cell 20
# ## 1.4 Erregresio-ereduak
#
# Diabetes datu-multzoa erabiliz hainbat erregresore konparatu.
#


# %% [code] Cell 21
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
import numpy as np

X, y = load_diabetes(return_X_y=True)
X_ent, X_test, y_ent, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
eskala = StandardScaler()
X_ent = eskala.fit_transform(X_ent)
X_test = eskala.transform(X_test)

def ebaluatu(izena, eredua):
    eredua.fit(X_ent, y_ent)
    y_irag = eredua.predict(X_test)
    print(f"\n{izena}:")
    print(f"  RMSE: {np.sqrt(mean_squared_error(y_test, y_irag)):.2f}")
    print(f"  MAE:  {mean_absolute_error(y_test, y_irag):.2f}")
    print(f"  R2:   {r2_score(y_test, y_irag):.4f}")

ebaluatu("Erregresio Lineala", LinearRegression())
ebaluatu("Ridge (L2)", Ridge(alpha=1.0))
ebaluatu("Lasso (L1)", Lasso(alpha=0.1))
ebaluatu("Random Forest", RandomForestRegressor(n_estimators=100, random_state=42))



# %% [markdown] Cell 22
# ## 1.5 Pipeline-ak
#
# Aurreprozesatzea eta eredua objektu bakar batean kateatu — datu-isuria saihestu eta produkziora bidaltzeko prest.
#


# %% [code] Cell 23
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd, numpy as np, joblib

# Datu sintetikoak (langile-txandaketa iragartzeko)
np.random.seed(42)
n = 500
df = pd.DataFrame({
    "adina":         np.random.randint(22, 60, n),
    "soldata":       np.random.randint(20000, 70000, n),
    "lan_urte":      np.random.randint(0, 20, n),
    "departamentua": np.random.choice(["IT", "HR", "Finantza", "Eragiketak"], n),
    "txandakatze":   np.random.randint(0, 2, n)   # Helburua
})
df.loc[np.random.choice(df.index, 30), "adina"] = np.nan

X = df.drop("txandakatze", axis=1)
y = df["txandakatze"]
X_ent, X_test, y_ent, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

aurreproz = ColumnTransformer([
    ("zenbak", Pipeline([("bete", SimpleImputer(strategy="mean")),
                         ("eskala", StandardScaler())]),
     ["adina", "soldata", "lan_urte"]),
    ("kateg", Pipeline([("bete", SimpleImputer(strategy="most_frequent")),
                        ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]),
     ["departamentua"]),
])

# Pipeline osoa: aurreprozesatzailea + eredua objektu BAKAR batean
pipeline = Pipeline([
    ("aurreproz", aurreproz),
    ("eredua",    RandomForestClassifier(n_estimators=100, random_state=42))
])
pipeline.fit(X_ent, y_ent)   # dena batera entrenatu
print(classification_report(y_test, pipeline.predict(X_test)))

# Pipeline OSOA gorde eta kargatu (produkziorako prest)
joblib.dump(pipeline, "txandakatze_pipeline.pkl")
berreskuratua = joblib.load("txandakatze_pipeline.pkl")
print("\nLehen 5 iragarpenak (berreskuratutako pipeline-arekin):")
print(berreskuratua.predict(X_test[:5]))



# %% [markdown] Cell 24
# ## 1.6 Ebaluazioa eta hiperparametroen doiketa
#
# ### Gurutze-balioztatzea
#


# %% [code] Cell 25
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_breast_cancer

X, y = load_breast_cancer(return_X_y=True)
rf = RandomForestClassifier(n_estimators=100, random_state=42)

puntuazioak = cross_val_score(rf, X, y, cv=5, scoring="roc_auc")
print(f"ROC-AUC (5-fold): {puntuazioak.mean():.4f} +/- {puntuazioak.std():.4f}")

skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
print(f"F1 (10-fold):     {cross_val_score(rf, X, y, cv=skf, scoring='f1').mean():.4f}")



# %% [markdown] Cell 26
# ### GridSearchCV
#
# > **Oharra**: ondoko GridSearch-ak 36 konbinazio x 5 fold = 180 entrenamendu eskatzen ditu. `n_jobs=-1` paraleloan exekutatzeko.
#


# %% [code] Cell 27
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

parametro_sarea = {
    "n_estimators":      [50, 100, 200],
    "max_depth":         [None, 5, 10, 20],
    "min_samples_split": [2, 5, 10],
}
rf = RandomForestClassifier(random_state=42)
bilaketa = GridSearchCV(rf, parametro_sarea, cv=5, scoring="roc_auc", n_jobs=-1, verbose=1)
bilaketa.fit(X, y)

print(f"\nParametro onenak: {bilaketa.best_params_}")
print(f"ROC-AUC onena:    {bilaketa.best_score_:.4f}")
eredu_onena = bilaketa.best_estimator_   # parametro onenekin prest



# %% [markdown] Cell 28
# ---
# # 2. Hugging Face: Eredu aurreentrenatuen ekosistema
#
# > **Oharra garrantzitsua**: atal honetako adibideek **eredu pisutsuak deskargatzen dituzte lehen exekuzioan** (ehunka MB-tatik GB-etaraino). Konexio onarekin egin, eta lehen exekuzioa motela izango da; ondorengoak azkarrak (cachean gordeta).
# >
# > CPU-an exekutatuz gero, modelo txikiak (`distilbert` familia) gomendatzen dira.
#


# %% [markdown] Cell 29
# ## 2.2 Pipeline API: inferentzia azkarra
#
# `pipeline` funtzioa Hugging Face-ren abstrakzio mailarik altuena da: zeregin baten izena ematea aski da eta eredua automatikoki deskargatu eta prestatzen du.
#


# %% [code] Cell 30
from transformers import pipeline

# ---- Sentimenduen analisia ----
# Lehen aldian eredua deskargatzen du (distilbert-sst2, ~250 MB)
sailkatzailea = pipeline("sentiment-analysis")
emaitzak = sailkatzailea([
    "I love this product, it's amazing!",
    "This is the worst experience I have ever had.",
])
for e in emaitzak:
    print(f"Etiketa: {e['label']}, Konfiantza: {e['score']:.4f}")



# %% [code] Cell 31
# ---- Galdera-erantzun sistema (extractive QA) ----
qna = pipeline("question-answering")
testuingurua = """Scikit-learn Python-en ikasketa automatikoaren liburutegi nagusia da.
2007an David Cournapeau-k sortu zuen."""
erantzuna = qna(question="Noiz sortu zen Scikit-learn?", context=testuingurua)
print(f"{erantzuna['answer']} (konfiantza: {erantzuna['score']:.4f})")



# %% [code] Cell 32
# ---- Testu-laburpena (abstractive) ----
# OHARRA: bart-large-cnn eredua handia da (~1.6 GB). Aurrezteko, distilbart probatu.
laburtzailea = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
testu_luzea = ("Deep learning is a subset of machine learning that uses "
               "neural networks with many layers to model complex patterns "
               "in data. It has revolutionized fields like computer vision "
               "and natural language processing.")
print(laburtzailea(testu_luzea, max_length=40, min_length=10))



# %% [code] Cell 33
# ---- Irudi-sailkapena (Vision Transformer) ----
# OHARRA: deskomentatu probatzeko (eredu pisutsua)
# irudi_sailk = pipeline("image-classification", model="google/vit-base-patch16-224")
# emaitza = irudi_sailk("irudia.jpg")
# print(emaitza)



# %% [markdown] Cell 34
# ## 2.3 Tokenizatzaileak eta ereduak
#
# BERT-en tokenizatzailea eta ereduaren erabilera zuzena, embedding-ak lortzeko.
#


# %% [code] Cell 35
from transformers import AutoTokenizer, AutoModel
import torch

eredu_izena = "bert-base-multilingual-cased"   # euskara ere ulertzen du
tokenizatzailea = AutoTokenizer.from_pretrained(eredu_izena)
eredua = AutoModel.from_pretrained(eredu_izena)

testua = "Ikasketa automatikoa oso interesgarria da."
tokenak = tokenizatzailea(testua, return_tensors="pt", padding=True, truncation=True)

print("Token zatituak:")
print(tokenizatzailea.convert_ids_to_tokens(tokenak["input_ids"][0]))

with torch.no_grad():
    irteera = eredua(**tokenak)
embedding = irteera.last_hidden_state[:, 0, :]   # CLS tokena = testu osoaren embedding
print(f"\nEmbedding forma: {embedding.shape}")     # [1, 768]



# %% [markdown] Cell 36
# ## 2.4 Datasets liburutegia
#
# > **Oharra**: `load_dataset("imdb")` 80 MB inguru deskargatzen ditu lehen aldian.
#


# %% [code] Cell 37
from datasets import load_dataset, Dataset
import pandas as pd

# Datu-multzo bat kargatu (lehen kargatzean deskargatu, gero cachean)
datu_multzoa = load_dataset("imdb")
print(datu_multzoa)
# train: 25000 errenkada, test: 25000 errenkada

entren = datu_multzoa["train"]
print("\nLehen lagina:", entren[0])

# Pandas-era bihurtu (lehen 100ekin lan egitea memoria-eraginkorragoa)
df = entren.select(range(100)).to_pandas()
print(f"\nDataFrame forma: {df.shape}")



# %% [code] Cell 38
# Filtrak eta transformazioak
positiboak = entren.filter(lambda x: x["label"] == 1)
print(f"Iritzi positiboak: {len(positiboak)}")

# Pandas DataFrame batetik Dataset sortu
df_propio = pd.DataFrame({"testua": ["Adibide bat", "Beste bat"], "etiketa": [0, 1]})
datu_propioa = Dataset.from_pandas(df_propio)
print(datu_propioa)



# %% [markdown] Cell 39
# ---
# # 3. FastAPI: REST API-ak Python-ekin
#
# > **OHARRA garrantzitsua**: atal honetako kodea **ez da exekutagarria notebook batean modu tradizionalean**. FastAPI aplikazioak `uvicorn` zerbitzariarekin abiarazi behar dira terminal independente batean.
# >
# > Kasu bakoitzeko code cell-aren goian zer fitxategi gisa gorde eta nola exekutatu adieraziko da.
# >
# > Alternatiba aurreratua (aukerakoa): `nest_asyncio` + `uvicorn.Server` notebook barruan exekutatzeko — ez da gomendatzen ikasketa-fasean.
#


# %% [markdown] Cell 40
# ## 3.2 Oinarrizko ibilbideak eta HTTP metodoak
#
# **Script-a `aplikazioa.py` gisa gorde eta exekutatu:**
#
# ```bash
# uvicorn aplikazioa:app --reload --port 8000
# ```
#
# Gero `http://localhost:8000/docs` bisitatu Swagger UI ikusteko.
#


# %% [code] Cell 41
# aplikazioa.py
from fastapi import FastAPI, HTTPException, Query, Path
from typing import Optional

app = FastAPI(title="Nire Lehen API")

produktuak = {
    1: {"izena": "Ordenagailu eramangarria", "prezioa": 899.99, "stock": 15},
    2: {"izena": "Teklatua", "prezioa": 49.99, "stock": 50},
}

@app.get("/")
def hasiera():
    return {"mezua": "Ongi etorri APIra!"}

@app.get("/produktuak")
def produktu_guztiak(prezio_max: Optional[float] = Query(None)):
    emaitzak = list(produktuak.values())
    if prezio_max is not None:
        emaitzak = [p for p in emaitzak if p["prezioa"] <= prezio_max]
    return {"kopurua": len(emaitzak), "produktuak": emaitzak}

@app.get("/produktuak/{produktu_id}")
def produktu_bat(produktu_id: int = Path(..., ge=1)):
    if produktu_id not in produktuak:
        raise HTTPException(status_code=404, detail="Produktua ez da aurkitu")
    return produktuak[produktu_id]

@app.post("/produktuak", status_code=201)
def produktu_sortu(produktu: dict):
    id_berria = max(produktuak.keys()) + 1
    produktuak[id_berria] = produktu
    return {"id": id_berria, **produktu}

@app.delete("/produktuak/{produktu_id}", status_code=204)
def produktu_ezabatu(produktu_id: int):
    if produktu_id not in produktuak:
        raise HTTPException(status_code=404, detail="Produktua ez da aurkitu")
    del produktuak[produktu_id]



# %% [markdown] Cell 42
# ## 3.3 Pydantic: datu-balioztatze automatikoa
#
# **Script-a `aplikazio_pydantic.py` gisa gorde eta `uvicorn` bidez exekutatu.**
#


# %% [code] Cell 43
# aplikazio_pydantic.py
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from typing import Optional

app = FastAPI()

class ProduktuSarrera(BaseModel):
    izena:   str   = Field(..., min_length=2, max_length=100)
    prezioa: float = Field(..., gt=0, description="Prezioa euroan")
    stock:   int   = Field(default=0, ge=0)
    kategoria: Optional[str] = None

    @field_validator("izena")
    @classmethod
    def izena_garbitu(cls, balioa: str) -> str:
        return balioa.strip().title()

@app.post("/produktuak", status_code=201)
def produktu_sortu(produktua: ProduktuSarrera):
    # Hona iristen bada, datuak DAGOENEKO balioztatuta daude
    return {"izena": produktua.izena, "prezioa": produktua.prezioa}



# %% [markdown] Cell 44
# ## 3.4 ML eredua API bidez eskaini
#
# **Script-a `ml_api.py` gisa gorde.**
#
# Aurretik `models/pipeline.pkl` fitxategia behar da (1.5 ataleko pipeline-a `joblib.dump`-ekin gordeta).
#


# %% [code] Cell 45
# ml_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import joblib, numpy as np, os

app = FastAPI(title="ML Iragarpen API", version="1.0.0")

EREDU_BIDE = "models/pipeline.pkl"
eredua = None

@app.on_event("startup")
def eredua_kargatu():
    global eredua
    if os.path.exists(EREDU_BIDE):
        eredua = joblib.load(EREDU_BIDE)
        print(f"Eredua kargatuta: {EREDU_BIDE}")

class IragarpenEskaera(BaseModel):
    ezaugarriak: List[float] = Field(..., min_length=30, max_length=30)

class IragarpenErantzuna(BaseModel):
    iragarpena: int
    etiketa: str
    probabilitatea: float

@app.get("/osasuna")
def osasun_egiaztatu():
    return {"egoera": "martxan", "eredu_prest": eredua is not None}

@app.post("/iragarri", response_model=IragarpenErantzuna)
def iragarri(eskaera: IragarpenEskaera):
    if eredua is None:
        raise HTTPException(status_code=503, detail="Eredua ez dago prest.")
    X = np.array(eskaera.ezaugarriak).reshape(1, -1)
    irag = int(eredua.predict(X)[0])
    proba = float(eredua.predict_proba(X)[0][1])
    return IragarpenErantzuna(
        iragarpena=irag,
        etiketa="Gaiztoa" if irag == 1 else "Ona",
        probabilitatea=round(proba, 4)
    )



# %% [markdown] Cell 46
# ## 3.5 Autentifikazioa eta middleware-a
#
# **Script-a `api_segurua.py` gisa gorde. Token-a ingurune-aldagai gisa ezarri:**
#
# ```bash
# export API_TOKEN="zure_token_sekretua"
# uvicorn api_segurua:app --reload
# ```
#


# %% [code] Cell 47
# api_segurua.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
import time, os

app = FastAPI()

# CORS middleware-a (web nabigatzaileetarako)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nire-aplikazioa.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Denbora-neurketako middleware-a
@app.middleware("http")
async def denbora_neurtu(eskaera, deitu_hurrengoa):
    hasiera = time.time()
    erantzuna = await deitu_hurrengoa(eskaera)
    erantzuna.headers["X-Prozesatze-Denbora"] = str(round(time.time() - hasiera, 4))
    return erantzuna

# Token bidezko autentifikazioa
TOKEN_BALIOA = os.getenv("API_TOKEN", "")   # ingurune-aldagaitik!
segurtasuna = HTTPBearer()

def token_egiaztatu(kredentzialak: HTTPAuthorizationCredentials = Depends(segurtasuna)):
    if kredentzialak.credentials != TOKEN_BALIOA:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token baliogabea")
    return kredentzialak.credentials

@app.get("/babestua", dependencies=[Depends(token_egiaztatu)])
def ibilbide_babestua():
    return {"mezua": "Token egiazkoa! Ongi etorri."}



# %% [markdown] Cell 48
# ---
# # 4. Streamlit: Datu-aplikazioak azkar sortu
#
# > **OHARRA garrantzitsua**: Streamlit aplikazioak **ez dira notebook-ean exekutatzen**. Fitxategi independente baten beharra dute, terminaletik abiaraztekoa:
# >
# > ```bash
# > streamlit run aplikazioa.py
# > ```
# >
# > Automatikoki `http://localhost:8501` irekitzen du nabigatzailean.
#


# %% [markdown] Cell 49
# ## 4.1 Oinarrizko egitura
#
# **Script-a `aplikazioa.py` gisa gorde eta exekutatu `streamlit run aplikazioa.py`.**
#


# %% [code] Cell 50
# aplikazioa.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Nire Aplikazioa", page_icon="🤖", layout="wide")

st.title("Nire Lehen Streamlit Aplikazioa")
st.markdown("**Lodia**, *etzana* eta `kode` formatua Markdown bidez.")
st.info("Informazio-mezua")
st.success("Arrakasta-mezua")

df = pd.DataFrame({"izena": ["Ane", "Mikel"], "soldata": [28000, 35000]})
st.dataframe(df, use_container_width=True)
st.metric("Batezbesteko soldata", f"{df['soldata'].mean():,.0f} EUR", delta="2.3%")

col1, col2, col3 = st.columns(3)
col1.metric("Langileak", 2)
col2.metric("Soldata max", "35.000 EUR")
col3.metric("Soldata min", "28.000 EUR")



# %% [markdown] Cell 51
# ## 4.2 Sarrera-osagaiak eta egoera
#
# **Script-a `sarrera_osagaiak.py` gisa gorde eta `streamlit run` bidez exekutatu.**
#


# %% [code] Cell 52
# sarrera_osagaiak.py
import streamlit as st

st.title("Sarrera-osagaiak")

with st.sidebar:
    st.header("Konfigurazioa")
    hizkuntza = st.selectbox("Hizkuntza", ["Euskara", "Gaztelania", "Ingelesa"])

izena = st.text_input("Zure izena:", placeholder="Ane Etxebarria")
adina = st.number_input("Adina:", min_value=0, max_value=120, value=25)
soldata = st.slider("Urteko soldata (EUR):", 15_000, 100_000, 30_000, step=1_000)
departamentua = st.selectbox("Departamentua:", ["IT", "HR", "Finantza"])
baldintza = st.checkbox("Baldintzak onartzen ditut")

if st.button("Bidali", type="primary", disabled=not baldintza):
    st.success(f"Eskerrik asko, {izena}!")
    st.json({"izena": izena, "adina": adina, "soldata": soldata})

# Session state: aldagaiak saioaren artean gorde
if "klik_kopurua" not in st.session_state:
    st.session_state.klik_kopurua = 0
if st.button("Klik egin!"):
    st.session_state.klik_kopurua += 1
st.write(f"Klik kopurua: {st.session_state.klik_kopurua}")



# %% [markdown] Cell 53
# ## 4.3 Grafikoak eta datuak erakutsi
#
# **Script-a `grafikoak.py` gisa gorde.**
#


# %% [code] Cell 54
# grafikoak.py
import streamlit as st
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.title("Grafikoak Streamlit-en")

np.random.seed(42)
df = pd.DataFrame({
    "data":      pd.date_range("2024-01-01", periods=90),
    "salmenta":  np.random.randint(100, 500, 90),
    "produktua": np.random.choice(["A", "B", "C"], 90),
})

# Streamlit barne-grafikoak (azkarrak)
st.line_chart(df.set_index("data")["salmenta"])
st.bar_chart(df.groupby("produktua")["salmenta"].sum())

# Matplotlib (pertsonalizagarria) — gogoratu plt.close!
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(df["salmenta"], bins=20, color="#2ecc71", edgecolor="white")
ax.set_title("Salmenten banaketa")
st.pyplot(fig)
plt.close(fig)

# Plotly (interaktiboa: zoom, hover)
fig_plotly = px.scatter(df, x="data", y="salmenta", color="produktua",
                        size="salmenta", title="Salmenta denboran zehar")
st.plotly_chart(fig_plotly, use_container_width=True)



# %% [markdown] Cell 55
# ## 4.4 ML aplikazio osoa Streamlit-ekin
#
# **Script-a `ml_aplikazioa.py` gisa gorde eta `streamlit run` bidez abiarazi.**
#


# %% [code] Cell 56
# ml_aplikazioa.py
import streamlit as st
import pandas as pd, numpy as np
import matplotlib.pyplot as plt, seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

st.set_page_config(page_title="Minbizi Detekzioa", page_icon="🏥", layout="wide")

@st.cache_resource   # Eredua behin bakarrik kargatu/entrenatu
def eredua_kargatu():
    d = load_breast_cancer()
    X_ent, X_test, y_ent, y_test = train_test_split(
        d.data, d.target, test_size=0.2, random_state=42)
    eskala = StandardScaler()
    X_ent = eskala.fit_transform(X_ent)
    X_test = eskala.transform(X_test)
    rf = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_ent, y_ent)
    return rf, eskala, d, X_test, y_test

eredua, eskala, d, X_test, y_test = eredua_kargatu()

st.title("Bular-minbizi Detekzio Tresna")
orria = st.sidebar.radio("Orria:", ["Iragarri", "Ebaluazioa", "Ereduaz"])

if orria == "Iragarri":
    st.header("Iragarpen pertsonalizatua")
    with st.form("forma"):
        balioak = [st.number_input(izena, value=float(d.data[:, i].mean()), key=f"e{i}")
                   for i, izena in enumerate(d.feature_names[:5])]   # adibide soilik
        bidali = st.form_submit_button("Iragarri", type="primary")
    if bidali:
        st.success("Iragarpena egina (adibide-interfazea)")

elif orria == "Ebaluazioa":
    st.header("Ereduaren errendimendua")
    y_irag = eredua.predict(X_test)
    col1, col2 = st.columns(2)
    col1.metric("Zehaztasuna", f"{accuracy_score(y_test, y_irag):.3f}")
    col2.metric("F1", f"{f1_score(y_test, y_irag):.3f}")
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(confusion_matrix(y_test, y_irag), annot=True, fmt="d", cmap="Blues", ax=ax)
    st.pyplot(fig)
    plt.close(fig)

else:
    st.markdown("**Algoritmoa:** Random Forest · **Datuak:** Breast Cancer (569 lagin)")
    st.info("Aplikazio hau hezkuntza-helburuekin soilik sortua da.")



# %% [markdown] Cell 57
# ---
# # 5. LangChain: LLM aplikazioak eraikitzen (Gemini-rekin)
#
# > **Beharrezkoa**: `GOOGLE_API_KEY` ingurune-aldagaia ezarrita izan behar duzu Gemini API erabiltzeko. API-gakoa doan lortzen da [Google AI Studio](https://aistudio.google.com/apikey)-tik.
# >
# > Gomendatutakoa: `.env` fitxategi batean gorde eta `python-dotenv` bidez kargatu:
# >
# > ```
# > GOOGLE_API_KEY=zure_gako_pribatua_hemen
# > ```
#


# %% [markdown] Cell 58
# ## 5.2 Prompt template-ak eta chain-ak


# %% [code] Cell 59
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()   # GOOGLE_API_KEY .env fitxategitik irakurri

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

# ---- Mezua zuzenean bidali ----
erantzuna = llm.invoke([
    SystemMessage(content="Laguntzaile tekniko bat zara. Erantzun laburki eta argiro."),
    HumanMessage(content="Zer da Python-eko list comprehension bat?")
])
print(erantzuna.content)



# %% [code] Cell 60
# ---- Prompt template parametrizatua ----
txantiloia = ChatPromptTemplate.from_messages([
    ("system", "Aditu bat zara {arloa} arloan. Erantzun {hizkuntza} hizkuntzan."),
    ("human",  "{galdera}")
])

# ---- LCEL: chain-a | operadorearekin ----
chain = txantiloia | llm | StrOutputParser()

emaitza = chain.invoke({
    "arloa":     "ikasketa automatikoa",
    "hizkuntza": "euskara",
    "galdera":   "Zer da Random Forest algoritmoa?"
})
print(emaitza)   # Testu soila, ez objektua



# %% [markdown] Cell 61
# ## 5.3 Memoria eta elkarrizketa-historia
#
# Erabiltzaile bakoitzaren elkarrizketa-historia `session_id` baten arabera kudeatzen da.
#


# %% [code] Cell 62
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)

txantiloia = ChatPromptTemplate.from_messages([
    ("system", "Laguntzaile adimendun bat zara. Erantzun labur eta argian."),
    MessagesPlaceholder(variable_name="history"),
    ("human",  "{sarrera}")
])

saio_historioak: dict[str, ChatMessageHistory] = {}

def historia_lortu(saio_id: str) -> ChatMessageHistory:
    if saio_id not in saio_historioak:
        saio_historioak[saio_id] = ChatMessageHistory()
    return saio_historioak[saio_id]

chain = txantiloia | llm
chain_memoriarekin = RunnableWithMessageHistory(
    chain, historia_lortu,
    input_messages_key="sarrera", history_messages_key="history"
)

config = {"configurable": {"session_id": "erabiltzaile-001"}}
print(chain_memoriarekin.invoke(
    {"sarrera": "Kaixo! Nire izena Mikel da."}, config=config).content)
print(chain_memoriarekin.invoke(
    {"sarrera": "Zer da nire izena?"}, config=config).content)
# "Zure izena Mikel da." -> testuingurua gogoan du



# %% [markdown] Cell 63
# ## 5.4 Tresnak eta agentziak
#
# LLM-ari Python funtzioak "tresna" gisa eskaintzen zaizkio. Agentziak erabakitzen du noiz eta zein erabili.
#
# > **Kontuz**: `eval()` arriskutsua da sarrera ez-fidagarriekin — adibide didaktikoa baino ez.
#


# %% [code] Cell 64
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from datetime import datetime
import math

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

@tool
def kalkulatu(eragiketa: str) -> str:
    """Matematikako eragiketa bat kalkulatu. Adibidez: '2**10', 'math.sqrt(16)'."""
    try:
        return f"Emaitza: {eval(eragiketa, {'math': math, '__builtins__': {}})}"
    except Exception as e:
        return f"Errorea: {e}"

@tool
def data_lortu(formatu: str = "%Y-%m-%d") -> str:
    """Gaur egungo data lortu. Formatua: '%Y-%m-%d' edo '%d/%m/%Y'."""
    return datetime.now().strftime(formatu)

tresnak = [kalkulatu, data_lortu]

agente_txantiloia = ChatPromptTemplate.from_messages([
    ("system", "Laguntzaile adimendun eta zehatza zara. Beharrezkoak diren tresnak erabili."),
    ("human",  "{sarrera}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

agentea = create_tool_calling_agent(llm, tresnak, agente_txantiloia)
exekutagailua = AgentExecutor(agent=agentea, tools=tresnak, verbose=True, max_iterations=5)

for galdera in ["Zenbat da 2 hamarrera berretuta?", "Gaur zein data da?"]:
    print(exekutagailua.invoke({"sarrera": galdera})["output"])



# %% [markdown] Cell 65
# ---
# # 6. RAG: Berreskurapen-oinarritutako sorkuntza
#
# > **Beharrezkoa**: `GOOGLE_API_KEY` ingurune-aldagaia (Gemini-rentzat eta embedding-entzat).
# >
# > Paketeak: `langchain-google-genai`, `langchain-community`, `faiss-cpu`, `pypdf`.
#


# %% [markdown] Cell 66
# ## 6.2 Dokumentuak kargatu eta zatitu
#
# Dokumentu-iturri ohikoenak (PDF, testua, web) eta `RecursiveCharacterTextSplitter`-rekin zatitu.
#
# > **Oharra**: ondoko adibideak bertako fitxategiak/URLak eskatzen ditu. Hurrengo cell-ean alternatiba inline-a erakusten dugu.
#


# %% [code] Cell 67
# Adibide osoa — fitxategiak/URLak behar ditu
# from langchain_community.document_loaders import PyPDFLoader, TextLoader, WebBaseLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.schema import Document
#
# # ---- Dokumentuak kargatu (hainbat iturri) ----
# pdf_dok  = PyPDFLoader("txostena.pdf").load()
# testu_dok = TextLoader("dokumentua.txt", encoding="utf-8").load()
# web_dok  = WebBaseLoader("https://python.org/about/").load()
#
# # ---- Dokumentuak zatitu (chunking) ----
# zatitzailea = RecursiveCharacterTextSplitter(
#     chunk_size=1000,
#     chunk_overlap=200,
#     separators=["\n\n", "\n", ". ", " ", ""]
# )
# zatiak = zatitzailea.split_documents(pdf_dok)
# print(f"Zatiak: {len(zatiak)}")
# print(f"Lehen zatiaren metadatuak: {zatiak[0].metadata}")



# %% [code] Cell 68
# Alternatiba inline: testu luze bat eskuz sortu eta zatitu
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

testu_luzea = """FastAPI Python-en REST API-ak sortzeko esparru modernoa da.
Pydantic-ekin datu-balioztatzea egiten du eta Swagger UI dokumentazioa sortzen du.

Streamlit datu-aplikazioak azkar sortzeko liburutegia da. Goitik beherako
exekuzio-eredua erabiltzen du eta web-ezagutzarik gabe Python soilik erabiliz
aplikazio profesionalak sortzeko aukera ematen du.

LangChain LLM-en gainean aplikazioak eraikitzeko esparrua da. Prompt-en kudeaketa,
chain-en kateaketa, memoria eta agentziak biltzen ditu modulu bateratuetan.

RAG (Retrieval-Augmented Generation) patroia dokumentu pribatuei galderak egiteko
sistema bat eraikitzeko erabiltzen da. Embedding-ak eta bektore-dendak konbinatzen ditu."""

dokumentuak = [Document(page_content=testu_luzea, metadata={"iturria": "azalpena.txt"})]

zatitzailea = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""]
)
zatiak = zatitzailea.split_documents(dokumentuak)
print(f"Zatiak: {len(zatiak)}")
for i, z in enumerate(zatiak):
    print(f"\n--- Zatia {i} ({len(z.page_content)} karaktere) ---")
    print(z.page_content)



# %% [markdown] Cell 69
# ## 6.3 Bektore-dendak eta bilaketa semantikoa
#
# Gemini-ren embedding-eredua erabiliz FAISS bektore-denda lokala sortzen dugu.
#


# %% [code] Cell 70
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

# ---- Embedding-ak: testua bektore zenbakira (esanahia mantenduz) ----
embedding_eredua = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

dokumentuak = [
    Document(page_content="Scikit-Learn ikasketa automatikorako liburutegia da.",
             metadata={"iturria": "1"}),
    Document(page_content="Random Forest hainbat erabaki-zuhaitzen multzoa da.",
             metadata={"iturria": "2"}),
    Document(page_content="FastAPI REST API-ak azkar sortzeko esparrua da.",
             metadata={"iturria": "3"}),
]

bektore_denda = FAISS.from_documents(dokumentuak, embedding_eredua)

# ---- Bilaketa semantikoa ----
emaitzak = bektore_denda.similarity_search("Zer da ikasketa automatikoa?", k=2)
for dok in emaitzak:
    print(f"(iturria {dok.metadata['iturria']}): {dok.page_content}")

# ---- Diskoan gorde eta retriever gisa erabili ----
bektore_denda.save_local("bektore_denda_faiss")
berreskuratzailea = bektore_denda.as_retriever(search_kwargs={"k": 3})



# %% [markdown] Cell 71
# ## 6.4 RAG pipeline osoa
#
# Dena LCEL-ekin kateatuta: berreskuratzailea + prompt + Gemini + parser.
#


# %% [code] Cell 72
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# ---- 1. Dokumentuak prestatu ----
dokumentuak_gordinak = [
    Document(page_content="""FastAPI Python-en REST API-ak sortzeko esparru modernoa da.
    Pydantic-ekin datu-balioztatzea egiten du eta Swagger UI dokumentazioa sortzen du.""",
             metadata={"iturria": "fastapi_gida.txt"}),
    Document(page_content="""RAG metodoak LLM-ari kanpoko dokumentuetara sarbidea ematen dio.
    Galdera bat jasotakoan, dokumentu garrantzitsuenak berreskuratzen dira.""",
             metadata={"iturria": "rag_gida.txt"}),
]

# ---- 2. Zatitu, embed eta bektore-denda ----
zatiak = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=100).split_documents(dokumentuak_gordinak)
embedding_eredua = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
bektore_denda = FAISS.from_documents(zatiak, embedding_eredua)
berreskuratzailea = bektore_denda.as_retriever(search_kwargs={"k": 3})

# ---- 3. Prompt template RAGerako (alucinazioak murrizteko) ----
rag_txantiloia = ChatPromptTemplate.from_template("""
Beheko testuingurua erabiliz, galderari erantzun. Testuinguruan informazioa
ez badago, esan "Ez dakit, informazioa ez dago eskuragarri." Asmatu gabe erantzun.

Testuingurua:
{testuingurua}

Galdera: {galdera}

Erantzuna:""")

# ---- 4. RAG chain osoa (LCEL) ----
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

def dok_formatu(dokumentuak):
    return "\n\n---\n\n".join(
        f"[Iturria: {d.metadata.get('iturria', 'ezezaguna')}]\n{d.page_content}"
        for d in dokumentuak)

rag_chain = (
    {"testuingurua": berreskuratzailea | dok_formatu, "galdera": RunnablePassthrough()}
    | rag_txantiloia | llm | StrOutputParser()
)

# ---- 5. Probatu ----
galderak = [
    "Nola erabiltzen da FastAPI?",
    "Nola funtzionatzen du RAG-ek?",
    "Zein da Python-en asmatzailea?"   # azkena ez dago testuinguruan
]
for galdera in galderak:
    print(f"\n? {galdera}")
    print(f"> {rag_chain.invoke(galdera)}")



# %% [markdown] Cell 73
# ---
# # 7. Proiektu integratzailea: GenAI aplikazio osoa
#
# Dena batera: **FastAPI** (backend) + **LangChain + RAG + Gemini** (logika) + **Streamlit** (frontend).
#
# > **OHARRA**: hurrengo bi script-ak fitxategi independenteetan gorde eta exekutatu behar dira (ez notebook batean). `GOOGLE_API_KEY` ingurune-aldagaia ezinbestekoa da.
# >
# > Bi terminal beharko dituzu:
# >
# > ```bash
# > # 1. terminala: backend-a
# > uvicorn rag_api:app --reload --port 8000
# >
# > # 2. terminala: frontend-a
# > streamlit run rag_streamlit.py
# > ```
#


# %% [markdown] Cell 74
# ## `rag_api.py` — Backend osoa (Gemini-rekin)
#
# **Script-a `rag_api.py` gisa gorde.**
#


# %% [code] Cell 75
# rag_api.py
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.schema import Document
from typing import Optional

app = FastAPI(title="Dokumentuen Galdera-Erantzun Sistema")

bektore_denda: Optional[FAISS] = None
embedding_eredua = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

class GalderaEskaera(BaseModel):
    galdera: str
    k_dokumentu: int = 3

class GalderaErantzuna(BaseModel):
    erantzuna: str
    iturriak: list[str]
    dokumentu_kopurua: int

@app.post("/dokumentuak/kargatu")
async def dokumentuak_kargatu(fitxategiak: list[UploadFile] = File(...)):
    global bektore_denda
    dokumentuak = []
    for f in fitxategiak:
        edukia = (await f.read()).decode("utf-8", errors="ignore")
        dokumentuak.append(Document(page_content=edukia, metadata={"iturria": f.filename}))
    zatiak = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200).split_documents(dokumentuak)
    if bektore_denda is None:
        bektore_denda = FAISS.from_documents(zatiak, embedding_eredua)
    else:
        bektore_denda.add_documents(zatiak)
    return {"mezua": f"{len(fitxategiak)} fitxategi kargatuta",
            "zati_kopurua": len(zatiak)}

@app.post("/galdera", response_model=GalderaErantzuna)
def galdera_egin(eskaera: GalderaEskaera):
    if bektore_denda is None:
        raise HTTPException(status_code=400, detail="Dokumenturik ez dago kargatuta.")
    berreskuratzailea = bektore_denda.as_retriever(
        search_kwargs={"k": eskaera.k_dokumentu})
    rag_txantiloia = ChatPromptTemplate.from_template("""
Beheko testuingurua erabiliz, galderari zehaztasunez erantzun.
Testuinguruan informazioa ez badago, esan hori argi.

Testuingurua:
{testuingurua}

Galdera: {galdera}

Erantzuna:""")
    berreskuratutako_dok = []
    def gorde_eta_formatu(dok_zerrenda):
        berreskuratutako_dok.extend(dok_zerrenda)
        return "\n\n".join(d.page_content for d in dok_zerrenda)
    chain = (
        {"testuingurua": berreskuratzailea | gorde_eta_formatu,
         "galdera": RunnablePassthrough()}
        | rag_txantiloia | llm | StrOutputParser()
    )
    erantzuna = chain.invoke(eskaera.galdera)
    iturriak = list({d.metadata.get("iturria", "ezezaguna")
                     for d in berreskuratutako_dok})
    return GalderaErantzuna(erantzuna=erantzuna, iturriak=iturriak,
                            dokumentu_kopurua=len(berreskuratutako_dok))

@app.get("/osasuna")
def osasuna():
    return {"egoera": "martxan", "dokumentuak_kargatuta": bektore_denda is not None}



# %% [markdown] Cell 76
# ## `rag_streamlit.py` — Frontend-a
#
# **Script-a `rag_streamlit.py` gisa gorde eta `streamlit run` bidez abiarazi.**
#


# %% [code] Cell 77
# rag_streamlit.py
import os
import streamlit as st
import requests

st.set_page_config(page_title="Dokumentuen Galdera-Erantzun Sistema",
                   page_icon="📚", layout="wide")
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("Dokumentuen Galdera-Erantzun Sistema")
st.markdown("Zure dokumentuak igo eta galderak egin (Gemini-z elikatua).")

with st.sidebar:
    st.header("Dokumentuak")
    igotakoak = st.file_uploader("Fitxategiak (TXT)", type=["txt"],
                                 accept_multiple_files=True)
    if igotakoak and st.button("Kargatu", type="primary"):
        fitx = [("fitxategiak", (f.name, f.read(), "text/plain"))
                for f in igotakoak]
        try:
            r = requests.post(f"{API_URL}/dokumentuak/kargatu",
                              files=fitx, timeout=60)
            if r.status_code == 200:
                d = r.json()
                st.success(f"{d['mezua']} ({d['zati_kopurua']} zati)")
            else:
                st.error(f"Errorea: {r.text}")
        except requests.exceptions.ConnectionError:
            st.error("APIarekin konektatu ezin izan da.")

galdera = st.text_area("Galdera idatzi:",
                       placeholder="Adibidez: Zer da RAG?", height=100)
k_dok = st.number_input("Dokumentu kopurua", min_value=1, max_value=10, value=3)

if st.button("Galdetu", type="primary") and galdera:
    with st.spinner("Erantzuna bilatzen..."):
        try:
            r = requests.post(f"{API_URL}/galdera",
                              json={"galdera": galdera, "k_dokumentu": k_dok},
                              timeout=60)
            if r.status_code == 200:
                d = r.json()
                st.subheader("Erantzuna")
                st.write(d["erantzuna"])
                st.info(f"Iturria(k): {', '.join(d['iturriak'])}")
            elif r.status_code == 400:
                st.warning(r.json()["detail"])
        except requests.exceptions.ConnectionError:
            st.error("APIarekin konektatu ezin izan da.")



# %% [markdown] Cell 78
# ---
#
# ## Amaiera
#
# Notebook honek 3. gaiaren Python adibide guztiak biltzen ditu, zazpi atal nagusietan:
#
# - **§1 Scikit-Learn** — Bost urratseko lan-fluxua, transformatzaileak, sailkapena, erregresioa, pipeline-ak, GridSearchCV.
# - **§2 Hugging Face** — `pipeline()` API, BERT eleaniztuna, `datasets`.
# - **§3 FastAPI** — REST API-ak, Pydantic, ML zerbitzaratzea, autentifikazioa (script gisa).
# - **§4 Streamlit** — Interfaze interaktiboak, grafikoak, ML aplikazio osoa (script gisa).
# - **§5 LangChain + Gemini** — Prompt template-ak, LCEL chain-ak, memoria, agentziak.
# - **§6 RAG** — Dokumentuen zatiketa, embedding-ak, FAISS, RAG pipeline osoa.
# - **§7 Proiektu integratzailea** — FastAPI + RAG + Gemini + Streamlit.
#
# *5073 Modulua — Adimen Artifizialaren Programazioa | 3. Gaia: AA Frameworka | Laneki — FP Euskadi*
#
