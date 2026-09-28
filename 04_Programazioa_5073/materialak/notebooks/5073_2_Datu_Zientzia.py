#!/usr/bin/env python3
# Auto-converted from 5073_2_Datu_Zientzia.ipynb
# Executable in VS Code (supports # %% interactive cells) or terminal via `python3`.


# %% [markdown] Cell 1
# # 2. Gaia · Datu Zientziaren Stack-a — Python adibideak
#
#
# ---
#
# Notebook hau dokumentu didaktikoaren **osagarria** da.
# Bertan agertzen diren kode-adibide guztiak hemen exekutagarri bilakatu dira, ariketak banaka edo gelan ariketa praktiko gisa ebatzi ahal izateko.
#
# **Edukiak:**
# 1. NumPy — array-ak, broadcasting, indexazioa, estatistika eta algebra lineala
# 2. Pandas — Series/DataFrame, kargatzea, garbiketa, agregazioa, taulen batzea
# 3. Matplotlib eta Seaborn — bistaratzea
# 4. DVC — datuen bertsio-kontrola (bash komandoak)
# 5. Plataforma komertzialak — kontzeptuak
#
# > Notebook hau exekutatzeko: `numpy`, `pandas`, `matplotlib` eta `seaborn` instalatuta egon behar dute. Zelulak goitik behera exekuta daitezke ordenan.


# %% [markdown] Cell 2
# ## Setup
#
# Notebook osoan zehar erabiliko diren liburutegi nagusiak. Gelaxka hau **lehenik exekutatu behar da**.


# %% [code] Cell 3
# @title
# Liburutegi nagusien inportazioak
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Matplotlib-en grafikoak notebook-ean inline erakusteko
# IPython magic: %matplotlib inline

# Seaborn-en gai estetiko atsegina
sns.set_theme(style="whitegrid")

# Erreproduzigarritasunerako ausazko hazia
np.random.seed(42)

print("Liburutegiak prest:")
print(f"  numpy      = {np.__version__}")
print(f"  pandas     = {pd.__version__}")
print(f"  matplotlib = {plt.matplotlib.__version__}")
print(f"  seaborn    = {sns.__version__}")


# %% [markdown] Cell 4
# ---
#
# # 1. NumPy: Array-ak eta Eragiketa Bektorialak
#
# NumPy datu-zientziaren ekosistema osoaren zutabe nagusia da. Atal honetan array-ak nola sortu, broadcasting nola erabili, indexazioa eta estatistika oinarrizkoak ikusiko ditugu.


# %% [markdown] Cell 5
# ## 1.1 NumPy zer da eta zergatik erabili
#
# Python zerrenden eta NumPy array-en abiadura-konparaketa.


# %% [code] Cell 6
import time

# Denbora-konparaketa: 10 milioi elementuko zerrenda
#N = 10_000_000
iterazioak = [1000000,10000000,50000000]

for i in iterazioak:
  # Python zerrenda
  lista = list(range(i))
  hasiera = time.time()
  emaitza_zerrenda = [x * 2 for x in lista]
  denbora_zerrenda = time.time() - hasiera
  print(f"Python zerrenda ({i}): {denbora_zerrenda:.3f}s")

  # NumPy array
  array = np.arange(i)
  hasiera = time.time()
  emaitza_array = array * 2
  denbora_array = time.time() - hasiera
  print(f"NumPy array ({i}):    {denbora_array:.3f}s")

  # NumPy normalean 10-100 aldiz azkarragoa da
  print(f"Aldaketa-faktorea ({i}): {denbora_zerrenda / denbora_array:.1f}x azkarrago")


# %% [markdown] Cell 7
# ## 1.2 Array-ak sortu eta manipulatu
#
# Array bat NumPy-ren oinarrizko datu-egitura da: tamaina finkoko eta mota homogeneoko elementu-bilduma.


# %% [code] Cell 8
# Zerrendatik array sortu
a = np.array([1, 2, 3, 4, 5])
print("a =", a)
print("a.dtype =", a.dtype)    # int64

# Matrize bidimentsionala (2D)
matrizea = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
print("\nmatrizea =\n", matrizea)
print("matrizea.shape =", matrizea.shape)   # (3, 3) — 3 errenkada, 3 zutabe
print("matrizea.ndim  =", matrizea.ndim)    # 2 — dimentsio kopurua
print("matrizea.size  =", matrizea.size)    # 9 — elementu kopurua osoa


# %% [code] Cell 9
# Forma jakin batekin sortzeko funtzioak
zeros = np.zeros((3, 4))        # 3x4 matrizea, denok 0
ones = np.ones((2, 3))          # 2x3 matrizea, denok 1
beteak = np.full((3, 3), 7.5)   # 3x3 matrizea, denok 7.5
I = np.eye(4)                   # 4x4 identitate-matrizea (diagonalean 1)
#I = np.eye(4).astype(int)

print("zeros =\n", zeros)
print("\nones =\n", ones)
print("\nbeteak =\n", beteak)
print("\nI =\n", I)


# %% [code] Cell 10
# Sekuentziak
a = np.arange(0, 10, 2)         # [0 2 4 6 8] — 0tik 10era, 2ko pausuak
b = np.linspace(0, 1, 5)        # [0. 0.25 0.5 0.75 1.] — 5 balio berdin banatuta

print("arange:  ", a)
print("linspace:", b)

# Ausazko array-ak
np.random.seed(42)              # Erreproduzigarritasunerako
c = np.random.rand(3, 3)        # [0, 1) tarteko balioak
d = np.random.randn(3, 3)       # Banaketa normala (mu=0, sigma=1)

print("\nrand(3,3) [uniformea] =\n", c)
print("\nrandn(3,3) [normala]  =\n", d)


# %% [code] Cell 11
# Forma aldatzea (reshape)
a = np.arange(12)        # [0 1 2 ... 11]
b = a.reshape(3, 4)      # 3 errenkada, 4 zutabe
c = a.reshape(4, -1)     # 4 errenkada, zutabe-kopurua automatikoa (3)
laua = b.flatten()       # Berriz bektore bakar bihurtu

print("a (jatorrizkoa):", a)
print("\nb (3,4):\n", b)
print("\nc (4,-1):\n", c)
print("\nlaua:", laua)


# %% [markdown] Cell 12
# ## 1.3 Eragiketa bektorialak eta broadcasting
#
# NumPy-n eragiketa aritmetikoak elementuz elementu aplikatzen dira, `for`-begiztarik gabe.


# %% [code] Cell 13
# Oinarrizko eragiketa bektorialak
a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

print("a + b =", a + b)        # [11 22 33 44 55]
print("a * b =", a * b)        # [ 10  40  90 160 250]
print("a ** 2 =", a ** 2)      # [ 1  4  9 16 25]
print("sqrt(a) =", np.sqrt(a)) # [1.    1.414 1.732 2.    2.236]
print("a * 3 =", a * 3)        # [ 3  6  9 12 15] — eskalarra array osoari


# %% [code] Cell 14
# Broadcasting: forma desberdineko array-en arteko eragiketak
# 2D array + 1D array: errenkada "hedatu" egiten da
matrizea = np.array([[1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 9]])
errenkada = np.array([10, 20, 30])

print("matrizea =\n", matrizea)
print("\nerrenkada =", errenkada)
print("\nmatrizea + errenkada =\n", matrizea + errenkada)
# errenkada array-a 3 errenkadatan "hedatzen" da automatikoki


# %% [code] Cell 15
# Datuen normalizazioa (Z-score) broadcasting bidez
datuak = np.array([
    [2.0, 3.0, 4.0],
    [5.0, 6.0, 7.0],
    [8.0, 9.0, 10.0]
])

# Zutabe bakoitzaren batezbestekoa eta desbideratze estandarra
batezbestekoa = datuak.mean(axis=0)   # forma: (3,)
std = datuak.std(axis=0)              # forma: (3,)

print("Batezbestekoa zutabeka:", batezbestekoa)
print("Desbideratze estandarra:", std)

# Broadcasting bidez normalizatu (Z-score) — lerro bakarra!
normalizatua = (datuak - batezbestekoa) / std
print("\nNormalizatua (Z-score):\n", normalizatua)


# %% [markdown] Cell 16
# ## 1.4 Indexazioa eta zatiketa
#
# Indizeak, slicing eta boolean maskak: datu-zientziaren eguneroko teknikak.


# %% [code] Cell 17
# Oinarrizko indexazioa eta slicing 2D matrizeetan
m = np.array([
    [1,  2,  3,  4],
    [5,  6,  7,  8],
    [9,  10, 11, 12]
])

print("m =\n", m)
print("\nm[0, 0]    =", m[0, 0])     # 1 — lehen errenkada, lehen zutabea
print("m[1, 2]    =", m[1, 2])         # 7
print("m[1, :]    =", m[1, :])         # [5 6 7 8] — errenkada osoa
print("m[:, 2]    =", m[:, 2])         # [ 3  7 11] — zutabe osoa
print("m[0:2,1:3] =\n", m[0:2, 1:3])  # azpi-matrizea: [[2 3] [6 7]]


# %% [code] Cell 18
# Boolean indexazioa (maskak)
a = np.array([15, 3, 8, 22, 7, 19, 4, 11])

maska = a > 10
print("a     =", a)
print("maska =", maska)
print("a[maska] =", a[maska])        # [15 22 19 11]
print("a[a>10]  =", a[a > 10])       # Berdina, zuzenean

# Hainbat baldintza (parentesiak derrigorrezkoak!)
print("\na[(a > 5) & (a < 15)] =", a[(a > 5) & (a < 15)])   # [ 8  7 11]


# %% [code] Cell 19
# Balioak aldatu maskaren bidez
a = np.array([15, 3, 8, 22, 7, 19, 4, 11])
a[a > 15] = 0
print("15 baino handiagoak zerora:", a)   # [ 0  3  8  0  7  0  4 11]

# NaN balioak tratatu
datuak = np.array([1.0, np.nan, 3.0, np.nan, 5.0])
baliodunak = ~np.isnan(datuak)        # ~ = EZ logikoa
print("\nDatuak:    ", datuak)
print("Baliodunak:", baliodunak)
print("Batezbestekoa NaN gabe:", np.mean(datuak[baliodunak]))


# %% [markdown] Cell 20
# ## 1.5 Estatistika eta algebra linealaren oinarriak
#
# Estatistika deskribatzaileko funtzioak eta algebra linealeko eragiketa nagusiak.


# %% [code] Cell 21
# Estatistika deskribatzailea
datuak = np.array([4.0, 7.0, 13.0, 2.0, 1.0, 9.0, 6.0, 3.0, 8.0, 5.0])

print(f"Batezbestekoa:     {np.mean(datuak):.2f}")    # 5.80
print(f"Mediana:           {np.median(datuak):.2f}")  # 5.50
print(f"Desbideratze est.: {np.std(datuak):.2f}")     # 3.19
print(f"Pertzentila 25:    {np.percentile(datuak, 25):.2f}")
print(f"Min - Max:         {datuak.min():.2f} - {datuak.max():.2f}")
print(f"Batura:            {datuak.sum():.2f}")


# %% [code] Cell 22
# Matrizeetan: axis parametroa
m = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

print("m =\n", m)
print("\nm.mean(axis=0) =", m.mean(axis=0))   # [4. 5. 6.] — zutabeak
print("m.mean(axis=1) =", m.mean(axis=1))     # [2. 5. 8.] — errenkadak
print("\nm.sum(axis=0)  =", m.sum(axis=0))   # zutabeen batura
print("m.sum(axis=1)  =", m.sum(axis=1))     # errenkaden batura


# %% [code] Cell 23
# Algebra lineala
A = np.array([[1, 2],
              [3, 4]])

B = np.array([[5, 6],
              [7, 8]])

print("A =\n", A)
print("\nB =\n", B)

# Matrize-biderketa (ez elementuz elementu!)
C = A @ B
print("\nA @ B (matrize-biderketa) =\n", C)

# Transposazioa
print("\nA.T (transposazioa) =\n", A.T)


# %% [code] Cell 24
# np.linalg modulua: eragiketa aurreratuak
A = np.array([[1, 2],
              [3, 4]])

det = np.linalg.det(A)                  # Determinantea
A_inv = np.linalg.inv(A)                # Alderantzizkoa
balioak, bektoreak = np.linalg.eig(A)   # Balio/bektore propioak

print(f"Determinantea: {det:.4f}")
print(f"\nAlderantzizkoa:\n{A_inv}")
print(f"\nBalio propioak: {balioak}")
print(f"\nBektore propioak:\n{bektoreak}")
print(f"\nIdentitatea:\n{np.round(A@A_inv).astype(int)}") # biribilketa + castinga

# Egiaztapena: A @ A_inv = I
print(f"\nA @ A_inv =\n{A @ A_inv}")


# %% [markdown] Cell 25
# ---
#
# # 2. Pandas: Datu-taulen Kudeaketa
#
# Pandas-ek bi datu-egitura nagusi ditu: Series eta DataFrame. Excel/SQL bezala lan egiteko aukera ematen du, baina askoz aukera gehiagorekin.


# %% [markdown] Cell 26
# ## 2.1 Series eta DataFrame
#
# Series = zutabe bakarra; DataFrame = taula osoa.


# %% [code] Cell 27
# Series: zutabe bakarra, indize etiketatuarekin
populazioa = pd.Series({
    "Bilbo": 346_843,
    "Donostia": 187_698,
    "Gasteiz": 252_427,
})
print(populazioa)
print("\npopulazioa['Bilbo'] =", populazioa["Bilbo"]) # 346843
print("\npopulazioa.Bilbo =", populazioa.Bilbo)

print("\nHiri handiak (>200.000):")
print(populazioa[populazioa > 200_000])  # Boolean indexazioa



# %% [code] Cell 28
# DataFrame sortu hiztegitik
datuak = {
    "izena":   ["Ane", "Mikel", "Leire", "Jon", "Amaia"],
    "adina":   [25, 30, 22, 35, 28],
    "hiria":   ["Bilbo", "Donostia", "Gasteiz", "Bilbo", "Donostia"],
    "soldata": [28000, 35000, 24000, 42000, 31000]
}
df = pd.DataFrame(datuak)

print("df =\n", df)
print("\ndf.shape =", df.shape)          # (5, 4)
print("\ndf.dtypes =\n", df.dtypes)
print("\ndf.describe():\n", df.describe())


# %% [code] Cell 29
# Lehen errenkadak eta zutabe-aukeraketa
print("df.head(3) =\n", df.head(3))

# Zutabe bat (Series)
print("\ndf['izena'] (Series):")
print(df["izena"])            # print(df.izena)
# Zutabe bat (DataFrame) KONTUZ!!
print("\ndf.izena (DataFrame):")
print(df[["izena"]])

# Hainbat zutabe (DataFrame)
print("\ndf[['izena','adina']] (DataFrame):")
print(df[["izena", "adina"]])


# %% [code] Cell 30
# Errenkadak filtratu baldintza baten arabera
bilbotarrak = df[df["hiria"] == "Bilbo"]
print("Bilboko langileak:\n", bilbotarrak)

hautaketa = df[(df["adina"] < 30) & (df["soldata"] > 25000)]
print("\n30 urtetik behera ETA 25.000eutik gora:\n", hautaketa)

# iloc vs loc
print("\niloc[0] (lehen errenkada, posizioz):")
print(df.iloc[0])
print("\nloc[0] (lehen errenkada, etiketaz):")
print(df.loc[0])
print("\niloc[0:2] (lehen BI errenkadak, posizioz):")
print(df.iloc[0:2])
print("\nloc[0:2] (lehen HIRU errenkadak, etiketaz):")
print(df.loc[0:2])


# %% [markdown] Cell 31
# ## 2.2 Datuak kargatu iturri anizkoitzetatik
#
# Egoera errealetan datuak CSV, Excel, JSON edo SQL formatuan etorri ohi dira (Nifi). Notebook honetan, erreproduzigarritasun propiorako ez baldin bada ere, Seabornen barneko datu-multzoak erabiliko ditugu.
#
# > **Oharra:** MD dokumentuko `read_csv("datuak.csv")` adibideak fitxategi-arruntak suposatzen ditu. Hemen `sns.load_dataset(...)` erabiltzen dugu kanpoko fitxategirik gabe lan egiteko.


# %% [code] Cell 32
# Seaborn barneko datu-multzo bat kargatu (CSV irakurketa bezala)
tips = sns.load_dataset("tips")

print("tips.shape =", tips.shape)
print("\nLehen 5 errenkadak:")
print(tips.head())
print("\nZutabe-motak:")
print(tips.dtypes)


# %% [code] Cell 33
# CSV idatzi eta berriz irakurri (read_csv parametroen adibidea)
tips.head(20).to_csv("/tmp/tips_lagina.csv", index=False, sep=";", encoding="utf-8")

# Berriz irakurri parametro esplizituekin
df_csv = pd.read_csv(
    "/tmp/tips_lagina.csv",
    sep=";",
    encoding="utf-8",
)
print("CSV-tik kargatua:")
print(df_csv.head())
print("\nShape:", df_csv.shape)


# %% [code] Cell 34
# Hainbat fitxategi simulatuak concat-ekin batzea
# (errealean: glob.glob('datuak/*.csv') erabiliko genuke)
hilabete_1 = pd.DataFrame({
    "data": ["2024-01-05", "2024-01-12"],
    "produktua": ["A", "B"],
    "kopurua": [10, 5],
})
hilabete_2 = pd.DataFrame({
    "data": ["2024-02-03", "2024-02-15"],
    "produktua": ["A", "C"],
    "kopurua": [8, 12],
})

# Iturria adierazi
hilabete_1["iturria"] = "urtarrila"
hilabete_2["iturria"] = "otsaila"

df_osoa = pd.concat([hilabete_1, hilabete_2], ignore_index=True)
print("Bateratutako DataFrame:\n", df_osoa)


# %% [markdown] Cell 35
# ## 2.3 Datu-garbiketa: fillna, dropna eta beste
#
# Datu-garbiketa edozein ML proiektuaren denboraren %60-80 hartzen du.


# %% [code] Cell 36
# Balio falten azterketa
df_zikina = pd.DataFrame({
    "izena":   ["Ane", "Mikel", None, "Jon", "Leire"],
    "adina":   [25, np.nan, 30, np.nan, 28],
    "soldata": [28000, 35000, np.nan, 42000, 31000],
})

print("DataFrame zikina:\n", df_zikina)
print("\nBalio falten kopurua zutabeka:")
print(df_zikina.isnull().sum())
print("\nEhunekoa:")
print(df_zikina.isnull().sum() / len(df_zikina) * 100)
print("\nBalio faltadun errenkadak:")
print(df_zikina[df_zikina.isnull().any(axis=1)])


# %% [code] Cell 37
# dropna: balio faltadun errenkadak ezabatu
df_garbia_1 = df_zikina.dropna()
print("dropna() (errenkada osoak):\n", df_garbia_1)

df_garbia_2 = df_zikina.dropna(subset=["adina", "soldata"])
print("\ndropna(subset=['adina','soldata']):\n", df_garbia_2)

df_garbia_3 = df_zikina.dropna(thresh=3)  # Gutxienez 3 balio baliodun (beteta)
print("\ndropna(thresh=3):\n", df_garbia_3)


# %% [code] Cell 38
# fillna: balioak bete
df_beteta = df_zikina.fillna({
    "adina": df_zikina["adina"].mean(),   # Batezbestekoarekin
    "soldata": 0,                          # Zeroarekin
    "izena": "Ezezaguna",                  # Katearekin
})
print("fillna() konbinatua:\n", df_beteta)


# %% [code] Cell 39
# Denbora-serieetan: ffill eta interpolate
tenp = pd.Series([20.0, np.nan, 22.0, np.nan, 19.0])

print("Jatorrizkoa:   ", tenp.tolist())
print("ffill():       ", tenp.ffill().tolist())        # Aurreko balioarekin
print("bfill():       ", tenp.bfill().tolist())        # Ondorengo balioarekin
print("interpolate(): ", tenp.interpolate().tolist())  # Tartekatze lineala


# %% [code] Cell 40
# Bikoiztuak ezabatu eta mota-bihurketa
df_string = pd.DataFrame({
    "soldata": ["28.000€", "35.000€", "24.000€"],
    "data":    ["2024-01-15", "2024-02-20", "2024-03-10"],
    "izena":   ["  Ane  ", "MIKEL", " leire"]
})

print("Hasieran:\n", df_string)
print("\nMotak:\n", df_string.dtypes)

# Bikoiztuak kendu (adibide gisa)
df_string = df_string.drop_duplicates(subset=["izena"], keep="first")

# Kate garbitu eta zenbakira bihurtu
df_string["soldata"] = (
    df_string["soldata"]
    .str.replace("€", "")
    .str.replace(".", "", regex=False)
    .astype(float)
)

# Data-formatua eta kate-garbiketa
df_string["data"] = pd.to_datetime(df_string["data"])   # fitxategietatik kargatzean "parses_date" eginez gero, BEHARRIK EZ
df_string["izena"] = df_string["izena"].str.strip().str.capitalize()

print("\nGarbituta:\n", df_string)
print("\nMotak:\n", df_string.dtypes)


# %% [markdown] Cell 41
# ## 2.4 Agregazioa: groupby eta pivot
#
# `groupby` = "split-apply-combine" (SQL-eko GROUP BY-en baliokidea).


# %% [code] Cell 42
# groupby oinarrizkoa
df = pd.DataFrame({
    "departamentua": ["IT", "HR", "IT", "HR", "IT", "Finantza"],
    "hiria":         ["Bilbo", "Bilbo", "Donostia", "Bilbo", "Donostia", "Gasteiz"],
    "soldata":       [42000, 30000, 38000, 28000, 45000, 52000],
})

print("DataFrame:\n", df)

# Departamentuka batezbesteko soldata
print("\nDepartamentuka batezbesteko soldata:")
print(df.groupby("departamentua")["soldata"].mean())


# %% [code] Cell 43
# Hainbat agregazio aldi berean, izen pertsonalizatuekin
laburpena = df.groupby("departamentua").agg(
    soldata_batezb=("soldata", "mean"),
    soldata_max=("soldata", "max"),
    langile_kop=("soldata", "count"),
).round(2)
print("Laburpena:\n", laburpena)


# %% [code] Cell 44
# transform: talde-batezbestekoa errenkada bakoitzari gehitu
df["dep_batezb"] = df.groupby("departamentua")["soldata"].transform("mean")
df["proportzioa"] = df["soldata"] / df["dep_batezb"]
print("transform-ekin zutabe berriak:\n", df.round(3))


# %% [code] Cell 45
# pivot_table: taula dinamikoa (Excel-en pivot table bezala)
taula = pd.pivot_table(
    df,
    values="soldata",
    index="departamentua",   # Errenkadak
    columns="hiria",         # Zutabeak
    aggfunc="mean",
    fill_value=0,
)
print("Pivot-taula (departamentua x hiria):\n", taula)


# %% [markdown] Cell 46
# ## 2.5 Taulen batzea: merge eta concat
#
# `concat` = taulak pilatu; `merge` = SQL-eko JOIN-en baliokidea.


# %% [code] Cell 47
# Bi taula erlazional
langileak = pd.DataFrame({
    "id":              [1, 2, 3, 4],
    "izena":           ["Ane", "Mikel", "Leire", "Jon"],
    "departamentu_id": [10, 20, 10, 30]
})

departamentuak = pd.DataFrame({
    "id":      [10, 20, 30],
    "izena":   ["IT", "HR", "Finantza"],
    "lokazio": ["Bilbo", "Donostia", "Gasteiz"]
})

print("Langileak:\n", langileak)
print("\nDepartamentuak:\n", departamentuak)


# %% [code] Cell 48
# INNER JOIN: bi tauletan dauden errenkadak bakarrik
emaitza = pd.merge(
    langileak, departamentuak,
    left_on="departamentu_id", right_on="id",
    how="inner",
    suffixes=("_langilea", "_dep")
)
print("INNER JOIN emaitza:\n", emaitza)


# %% [code] Cell 49
# LEFT JOIN: ezkerreko taula osoa mantendu
# Gehitu langile bat existitzen ez den departamentuarekin
langileak_v2 = pd.concat([
    langileak,
    pd.DataFrame({"id": [5], "izena": ["Amaia"], "departamentu_id": [99]})
], ignore_index=True)

emaitza_left = pd.merge(
    langileak_v2, departamentuak,
    left_on="departamentu_id", right_on="id",
    how="left",
    suffixes=("_langilea", "_dep")
)
print("LEFT JOIN (departamentu ezezagunarekin):\n", emaitza_left)


# %% [code] Cell 50
# concat: taulak pilatu (bertikalki)
df_bateratua = pd.concat([langileak, langileak], ignore_index=True)
print("concat bertikala (axis=0, bi aldiz pilatuta):\n", df_bateratua)


# %% [markdown] Cell 51
# ---
#
# # 3. Bistaratzea: Matplotlib eta Seaborn
#
# Datuen bistaratzea analisi exploratzailearen funtsezko zatia da.


# %% [markdown] Cell 52
# ## 3.1 Matplotlib: oinarriak
#
# `fig, ax = plt.subplots()` da Matplotlib-en gako-egitura.


# %% [code] Cell 53
# Lerro-grafiko bakuna: sinua eta kosinua
fig, ax = plt.subplots(figsize=(8, 5))

x = np.linspace(0, 2 * np.pi, 100)
ax.plot(x, np.sin(x), label="sin(x)", color="blue", linewidth=2)
ax.plot(x, np.cos(x), label="cos(x)", color="red", linestyle="--")

ax.set_title("Sinua eta kosinua", fontsize=14)
ax.set_xlabel("x (erradianetan)")
ax.set_ylabel("Balioa")
ax.legend()
ax.grid(False)

plt.tight_layout()
plt.show()


# %% [code] Cell 54
# Lau grafiko mota subplot batean (2x2)
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

x = np.linspace(0, 10, 100)
axs[0, 0].plot(x, np.sin(x), "b-")            # Lerro-grafikoa
axs[0, 0].set_title("Lerroa: joerak")

axs[0, 1].bar(["A", "B", "C"], [23, 45, 12])  # Barra-grafikoa
axs[0, 1].set_title("Barrak: konparaketak")

np.random.seed(42)
axs[1, 0].scatter(np.random.randn(50), np.random.randn(50), alpha=0.7)  # Sakabanaketa
axs[1, 0].set_title("Sakabanaketa: erlazioak")

axs[1, 1].hist(np.random.normal(50, 15, 1000), bins=30)  # Histograma
axs[1, 1].set_title("Histograma: banaketa")

plt.suptitle("Grafiko motak", fontsize=16)
plt.tight_layout()
plt.show()


# %% [markdown] Cell 55
# ## 3.2 Seaborn: grafiko estatistikoak
#
# Seaborn Matplotlib-en gainean dago eta DataFrames-ekin zuzenean lan egiten du.


# %% [code] Cell 56
# Datu-multzoa kargatu
tips = sns.load_dataset("tips")
print(tips.head())
print("\nShape:", tips.shape)


# %% [code] Cell 57
# Histograma + KDE, sexuaren arabera
plt.figure(figsize=(8, 5))
sns.histplot(data=tips, x="total_bill", hue="sex", bins=20, kde=True)
plt.title("Faktura totalaren banaketa sexuaren arabera")
plt.show()


# %% [code] Cell 58
# Boxplot: banaketaren kuartilak eta atipikoak
plt.figure(figsize=(9, 5))
sns.boxplot(data=tips, x="day", y="total_bill", hue="sex")
plt.title("Faktura totala egunaren eta sexuaren arabera")
plt.show()


# %% [code] Cell 59
# Sakabanaketa: bi aldagairen arteko erlazioa
plt.figure(figsize=(9, 6))
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="time", size="size")
plt.title("Faktura vs propina (ordu-tartearen eta talde-tamainaren arabera)")
plt.show()


# %% [code] Cell 60
# Korrelazio-matrizea heatmap gisa
korr = tips[["total_bill", "tip", "size"]].corr()
print("Korrelazio-matrizea:")
print(korr)

plt.figure(figsize=(6, 5))
sns.heatmap(korr, annot=True, fmt=".2f", cmap="coolwarm",
            vmin=-1, vmax=1, square=True)
plt.title("Korrelazio-matrizea")
plt.show()


# %% [markdown] Cell 61
# ## 3.3 Konfigurazioa eta esportazioa
#
# Estiloa proiektu-mailan zehaztea eta grafikoak hainbat formatutan esportatzea.


# %% [code] Cell 62
# Estiloak eta gaiak ezarri
sns.set_theme(style="whitegrid")    # Sare zuriko hondoa
sns.set_palette("muted")            # Kolore lasaiak

# Adibide-grafiko bat estilo berriarekin
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot([1, 2, 3, 4, 5], [4, 5, 6, 5, 7], marker="o", linewidth=2)
ax.set_title("Estiloak ezarrita: whitegrid + muted paleta")
ax.set_xlabel("X")
ax.set_ylabel("Y")
plt.tight_layout()
plt.show()


# %% [code] Cell 63
# Grafikoak hainbat formatutan gorde
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot([1, 2, 3], [4, 5, 6])
ax.set_title("Esportazio-adibidea")

# Hainbat formatu (raster eta bektoriala)
fig.savefig("/tmp/grafikoa.png", dpi=150, bbox_inches="tight")   # Web/aurkezpena
fig.savefig("/tmp/grafikoa.pdf", bbox_inches="tight")            # Txostenak
fig.savefig("/tmp/grafikoa.svg", bbox_inches="tight")            # Eskala aldagarria

plt.show()

# Tamainak alderatu
import os
for fmt in ["png", "pdf", "svg"]:
    bidea = f"/tmp/grafikoa.{fmt}"
    tamaina = os.path.getsize(bidea)
    print(f"  grafikoa.{fmt}: {tamaina:>7} byte")


# %% [markdown] Cell 64
# ---
#
# # 4. Datuen Bertsio-Kontrola: DVC
#
# DVC bash komandoekin lan egiten du nagusiki. Atal honetan **ez dago Python koderik**: shell komandoak markdown gelaxketan erakusten dira, eta nahi izanez gero `!komando` magia-zelulekin notebook-etik bertan exekuta daitezke (DVC instalatuta egonez gero).
#
# ## 4.1 DVC zer da
#
# Git kodearentzat da; DVC datu eta eredu handientzat. Datu-fitxategi handiak kanpoko biltegian (S3, GCS, lokala) gordetzen ditu, eta Git-en **puntero txiki bat** (`.dvc` fitxategia, hash bat) baino ez du jartzen.
#
# **Ohiko fluxua DVC-rekin:**
#
# ```bash
# dvc add datuak.csv      # datuak.csv.dvc sortzen da (puntero txikia)
# git add datuak.csv.dvc  # Puntero txikia Git-era (ez datu-fitxategia)
# dvc push                # Datu handiak kanpoko biltegira
# ```
#
# ## 4.2 Instalazioa
#
# ```bash
# pip install dvc
# pip install "dvc[s3]"      # Amazon S3
# pip install "dvc[gs]"      # Google Cloud Storage
# ```
#
# ## 4.3 Proiektua hasieratzea
#
# ```bash
# # Proiektua hasieratu
# git init
# dvc init
# git commit -m "chore: DVC hasieratu"
#
# # Datu-fitxategi bat DVC kontrolpean jarri
# dvc add data/train.csv      # train.csv.dvc puntero-fitxategia sortzen da
#
# # Puntero-fitxategia Git-era (datu-fitxategia EZ)
# git add data/train.csv.dvc data/.gitignore
# git commit -m "data: entrenamenduko datu-multzoa gehitu"
# ```
#
# ## 4.4 Urruneko biltegia eta sinkronizazioa
#
# ```bash
# # Urruneko biltegia konfiguratu
# dvc remote add -d biltegia s3://nire-bucket/dvc
#
# # Datuak igo/jaitsi
# dvc push     # Datuak biltegira (git push bezala, baina datuentzat)
# dvc pull     # Datuak biltegitik (git pull bezala)
# ```
#
# > **Gogoratu:** `.dvc` puntero-fitxategiak Git-en doaz; datu-fitxategi handiak ez. Git eta DVC elkarrekin lan egiten dute, ez bata bestearen ordez.


# %% [markdown] Cell 65
# ---
#
# # 5. Plataforma Komertzialak
#
# Atal hau **kontzeptuala** da: ez dago Python koderik. Plataforma komertzial nagusien laburpen bisuala dakar.
#
# ## 5.1 Open source vs SaaS
#
# | Eredua | **Open source** (Python) | **SaaS / Plataforma komertziala** |
# |---|---|---|
# | Adibideak | NumPy, Pandas, scikit-learn | Azure ML, IBM Watson, Knime, SPSS |
# | Erabilera | Garatzaileek kodea idatzi | Drag-and-drop interfaze grafikoa |
# | Hasierako kostua | Doan | Lizentzia ordainpekoak |
# | Pertsonalizazioa | Erabatekoa | Plataformaren mugen barruan |
# | Ikasketa-kurba | Aldapatsua (kodea) | Errazagoa (bisuala) |
# | Erabiltzaile-profila | Datu-zientzialaria, ingeniaria | Negozio-analista, citizen data scientist |
#
# ## 5.2 Plataforma nagusiak
#
# - **Azure ML Studio** (Microsoft) — kodea + Designer (no-code) + AutoML; Microsoft ekosistema duten enpresentzat aukera naturala.
# - **IBM Watson Studio** — enpresa handi eta sektore arautuetarako (banku, aseguru, osasun); governance eta GDPR-ren indargunea.
# - **Knime Analytics Platform** — drag-and-drop nodoak; 4000+ nodo, Python/R integratua; doakoa (oinarrizko bertsioa).
# - **SPSS Modeler / SAS / DataRobot / Dataiku / RapidMiner / Alteryx** — plataforma klasikoak, banku-aseguru-osasun sektoreetan oraindik oso presente.
#
# ## 5.3 Erabaki-irizpideak
#
# | Irizpidea | Python | Azure ML | IBM Watson | Knime | SPSS |
# |---|---|---|---|---|---|
# | Profila | Garatzailea | Hibridoa | Enpresa-analista | Citizen DS | Estatistika klasikoa |
# | Kostua | Doan | Hodeia | Hodeia + lizentzia | Doan oinarriz. | Lizentzia handia |
# | Programatzea | Bai | Aukeran | Aukeran | Ez | Ez |
# | Governance | Eskuz | Natiboa | Bikaina | Ertaina | Ona |
#
# > **Ideia nagusia:** Ez dago plataforma onenik abstraktuan; testuingurura egokitzen dena da egokiena. Tekniko on batek **bietan moldatzen** jakin behar du: lan-merkatuan biak topatuko ditu.


# %% [markdown] Cell 66
# ---
#
# # 6. Laburpena
#
# Notebook honetan **2. gaiaren bost zutabeak** ikusi ditugu kode bidez:
#
# 1. **NumPy** — array-ak, broadcasting, indexazioa, estatistika eta algebra lineala.
# 2. **Pandas** — Series/DataFrame, datu-kargatzea, garbiketa (`fillna`, `dropna`), agregazioa (`groupby`, `pivot_table`) eta taulen batzea (`merge`, `concat`).
# 3. **Matplotlib eta Seaborn** — Figure/Axes, grafiko-mota egokia datuari, `hue` parametroa, korrelazio-heatmap-ak eta esportazioa.
# 4. **DVC** — bash komandoak (`dvc add`, `dvc push`); Git kodearentzat, DVC datuentzat.
# 5. **Plataforma komertzialak** — Azure ML, IBM Watson, Knime, SPSS; open source eta SaaS osagarriak.
#
# **Gako-kontzeptuak gogoratzeko:**
#
# - **NumPy array** = mota homogeneoko bloke trinkoa, 10-100 aldiz azkarragoa zerrendak baino.
# - **Broadcasting** = forma desberdineko array-en arteko eragiketa begiztarik gabe.
# - **Boolean maska** = baldintza bat -> True/False -> datuak iragazi.
# - **DataFrame** = Pandas-en taula, zutabe bakoitza Series bat.
# - **Datu-garbiketa** = proiektuaren denboraren %60-80; "garbage in, garbage out".
# - **groupby** = split-apply-combine (SQL GROUP BY bezala).
# - **merge** = SQL JOIN; JOIN-mota egokia kritikoa.
# - **Korrelazio-heatmap** = ML aurretik ezaugarri garrantzitsuak ikusteko.
# - **DVC** = Git datuentzat; erreproduzigarritasuna.
# - **Open source vs SaaS** = osagarriak, ez aurkari.


# %% [markdown] Cell 67
#
