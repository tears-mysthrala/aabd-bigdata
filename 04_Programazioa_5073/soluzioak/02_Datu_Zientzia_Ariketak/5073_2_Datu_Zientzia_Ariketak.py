#!/usr/bin/env python3
# Auto-converted from 5073_2_Datu_Zientzia_Ariketak.ipynb
# Executable in VS Code (supports # %% interactive cells) or terminal via `python3`.


# %% [markdown] Cell 1
# # 02 Datu Zientzia Ariketak
# Helburua: NumPy, Pandas eta Seaborn lantzea.
# 
# ## Setup (Datuen sorkuntza)
# Lehenik, exekutatu hurrengo gelaxka datuak prestatzeko.


# %% [code] Cell 2
# @title
import os
import pandas as pd
import numpy as np

# Sortu data karpeta
os.makedirs('data', exist_ok=True)

# Sortu datu faltsuak (mock data)
np.random.seed(42)
data = {
    'makina_id': ['M1', 'M2', 'M3', 'M1', 'M2', 'M3', 'M1', 'M2', 'M3', 'M1'] * 10,
    'tenperatura': np.random.normal(60, 10, 100),
    'bibrazioa': np.random.normal(5, 2, 100),
    'errorea': np.random.choice([0, 1], 100, p=[0.9, 0.1])
}
df_mock = pd.DataFrame(data)

# Sartu anomaliak eta NaNak
df_mock.loc[5, 'tenperatura'] = np.nan
df_mock.loc[12, 'bibrazioa'] = np.nan
df_mock.loc[45, 'tenperatura'] = 999  # Outlier
df_mock.loc[78, 'bibrazioa'] = -50  # Outlier

df_mock.to_csv('data/cnc_mock.csv', index=False)
print('✅ data/cnc_mock.csv fitxategia sortu da anomalia eta NaNekin!')


# %% [markdown] Cell 3
# ## 1. NumPy


# %% [markdown] Cell 4
# **Ariketa 1.1:** Inportatu `numpy` eta sortu `arr1` izeneko 1D array bat 1etik 10era bitarteko zenbakiekin.


# %% [code] Cell 5
import numpy as np
# Zure kodea hemen:
arr1 = np.arange(1, 11)

# Balioztapena:
assert type(arr1) == np.ndarray, "arr1 numpy array bat izan behar da!"
assert len(arr1) == 10, "10 elementu izan behar ditu!"
assert arr1[0] == 1 and arr1[-1] == 10, "1etik 10era bitartekoa izan behar da!"
print('✅ Zuzena!')


# %% [markdown] Cell 6
# **Ariketa 1.2:** Sortu `arr2` izeneko 3x3 matrize bat, zeroz betea (`np.zeros`).


# %% [code] Cell 7
# Zure kodea hemen:
arr2 = np.zeros((3, 3))

# Balioztapena:
assert arr2.shape == (3, 3), "3x3 tamaina izan behar du!"
assert np.all(arr2 == 0), "Zeroz betea egon behar da!"
print('✅ Zuzena!')


# %% [markdown] Cell 8
# **Ariketa 1.3:** Sortu `arr3` izeneko 10 balio aleatorioko array bat (`np.random.rand`) eta gorde bere balio maximoa `max_val` aldagaian.


# %% [code] Cell 9
# Zure kodea hemen:
arr3 = np.random.rand(10)
max_val = np.max(arr3)

# Balioztapena:
assert len(arr3) == 10, "10 elementu izan behar ditu!"
assert max_val == np.max(arr3), "max_val balio maximoa izan behar da!"
print('✅ Zuzena!')


# %% [markdown] Cell 10
# **Ariketa 1.4:** Sortu `arr4` non `arr1`-eko elementu guztiak 2rekin biderkatuta dauden.


# %% [code] Cell 11
# Zure kodea hemen:
arr4 = arr1 * 2

# Balioztapena:
assert np.all(arr4 == arr1 * 2), "arr1-eko elementuak bider 2 izan behar dira!"
print('✅ Zuzena!')


# %% [markdown] Cell 12
# **Ariketa 1.5:** Sortu `arr5` izeneko array bat 0tik 11ra bitarteko balioekin (12 elementu). Gero, bihurtu 3x4 matrize batean eta gorde `mat1` aldagaian (`reshape`).


# %% [code] Cell 13
# Zure kodea hemen:
arr5 = np.arange(12)
mat1 = arr5.reshape(3, 4)

# Balioztapena:
assert len(arr5) == 12, "12 elementu izan behar ditu!"
assert mat1.shape == (3, 4), "3x4 matrizea izan behar da!"
print('✅ Zuzena!')


# %% [markdown] Cell 14
# ## 2. Boolean Indexazioa


# %% [markdown] Cell 15
# **Ariketa 2.1:** Erabili `arr1` eta sortu `arr_bikoitiak` array bat bakarrik zenbaki bikoitiekin.


# %% [code] Cell 16
# Zure kodea hemen:
arr_bikoitiak = arr1[arr1 % 2 == 0]

# Balioztapena:
assert np.all(arr_bikoitiak % 2 == 0), "Bikoitiak bakarrik egon behar dira!"
assert len(arr_bikoitiak) == 5, "5 zenbaki bikoiti egon behar dira 1-10 artean!"
print('✅ Zuzena!')


# %% [markdown] Cell 17
# **Ariketa 2.2:** Sortu `arr6` 1etik 20ra. Lortu 15 baino handiagoak diren elementuak eta gorde `arr_handiak` aldagaian.


# %% [code] Cell 18
# Zure kodea hemen:
arr6 = np.arange(1, 21)
arr_handiak = arr6[arr6 > 15]

# Balioztapena:
assert len(arr_handiak) == 5, "15 baino handiagoak 5 balio dira!"
assert np.all(arr_handiak > 15), "Balio guztiek 15 baino handiagoak izan behar dute!"
print('✅ Zuzena!')


# %% [markdown] Cell 19
# **Ariketa 2.3:** `arr6` erabiliz, ordezkatu 5 baino txikiagoak diren balioak 0-rekin. Gorde aldaketa array berdinean.


# %% [code] Cell 20
# Zure kodea hemen:
arr6[arr6 < 5] = 0

# Balioztapena:
assert np.array_equal(arr6[:4], np.zeros(4, dtype=int)), "Lehen lau balioak zero izan behar dira!"
assert np.array_equal(arr6[4:], np.arange(5, 21)), "Gainerako balioak ez dira aldatu behar!"
print('✅ Zuzena!')


# %% [markdown] Cell 21
# **Ariketa 2.4:** `arr6`-tik (aldatu ondoren), atera 10 eta 15 bitarteko balioak (biak barne) `arr_tartea` izenarekin.


# %% [code] Cell 22
# Zure kodea hemen:
arr_tartea = arr6[(arr6 >= 10) & (arr6 <= 15)]

# Balioztapena:
assert len(arr_tartea) == 6, "10etik 15era 6 balio daude!"
assert np.min(arr_tartea) >= 10 and np.max(arr_tartea) <= 15, "10-15 tartean egon behar dute!"
print('✅ Zuzena!')


# %% [markdown] Cell 23
# **Ariketa 2.5:** Zenbatu zenbat elementu diren 3ren multiploak `arr6`-n. Gorde kopurua `kop_multiplo_3` aldagaian.


# %% [code] Cell 24
# Zure kodea hemen:
kop_multiplo_3 = int(np.sum(arr6 % 3 == 0))

# Balioztapena:
assert kop_multiplo_3 == np.sum(arr6 % 3 == 0), "Zuzen kalkulatu behar duzu 3ren multiplo kopurua!"
print('✅ Zuzena!')


# %% [markdown] Cell 25
# ## 3. Pandas Karga


# %% [markdown] Cell 26
# **Ariketa 3.1:** Inportatu `pandas` eta kargatu `data/cnc_mock.csv` fitxategia `df` izeneko DataFrame batean.


# %% [code] Cell 27
import pandas as pd
# Zure kodea hemen:
df = pd.read_csv('data/cnc_mock.csv')

# Balioztapena:
assert type(df) == pd.DataFrame, "df DataFrame bat izan behar da!"
assert df.shape == (100, 4), "100 errenkada eta 4 zutabe izan behar ditu!"
print('✅ Zuzena!')


# %% [markdown] Cell 28
# **Ariketa 3.2:** Gorde `df`-ren lehen 5 errenkadak `df_head` aldagaian.


# %% [code] Cell 29
# Zure kodea hemen:
df_head = df.head(5)

# Balioztapena:
assert df_head.shape[0] == 5, "5 errenkada izan behar ditu!"
print('✅ Zuzena!')


# %% [markdown] Cell 30
# **Ariketa 3.3:** Gorde `df`-ren zutabeen izenak list edo array batean `zutabeak` izenarekin.


# %% [code] Cell 31
# Zure kodea hemen:
zutabeak = df.columns.tolist()

# Balioztapena:
assert 'makina_id' in zutabeak and 'tenperatura' in zutabeak, "Zutabeen izenak ondo lortu behar dira!"
print('✅ Zuzena!')


# %% [markdown] Cell 32
# **Ariketa 3.4:** Lortu `makina_id` zutabeko balio unikoak eta gorde `makinak_unikoak` aldagaian.


# %% [code] Cell 33
# Zure kodea hemen:
makinak_unikoak = df['makina_id'].unique()

# Balioztapena:
assert len(makinak_unikoak) == 3, "3 makina id uniko egon behar dira (M1, M2, M3)!"
assert 'M1' in makinak_unikoak, "M1 egon behar da zerrendan!"
print('✅ Zuzena!')


# %% [markdown] Cell 34
# **Ariketa 3.5:** Zenbatu zenbat errenkada diren `errorea == 1` baldintza betetzen dutenak eta gorde `errore_kop` aldagaian.


# %% [code] Cell 35
# Zure kodea hemen:
errore_kop = (df['errorea'] == 1).sum()

# Balioztapena:
assert errore_kop == (df['errorea'] == 1).sum(), "Errore kopurua zuzen kalkulatu behar da!"
print('✅ Zuzena!')


# %% [markdown] Cell 36
# ## 4. Pandas Garbiketa


# %% [markdown] Cell 37
# **Ariketa 4.1:** Zenbatu zenbat NaN balio dauden zutabe bakoitzean eta gorde `nan_kopuruak` aldagaian.


# %% [code] Cell 38
# Zure kodea hemen:
nan_kopuruak = df.isna().sum()

# Balioztapena:
assert nan_kopuruak['tenperatura'] == 1, "Tenperaturan 1 NaN egon behar da!"
assert nan_kopuruak['bibrazioa'] == 1, "Bibrazioan 1 NaN egon behar da!"
print('✅ Zuzena!')


# %% [markdown] Cell 39
# **Ariketa 4.2:** Ezabatu NaN dituzten errenkadak (`.dropna()`) eta gorde bertsio garbia `df_clean` aldagaian.


# %% [code] Cell 40
# Zure kodea hemen:
df_clean = df.dropna().copy()

# Balioztapena:
assert df_clean.isnull().sum().sum() == 0, "Ez da NaN baliorik geratu behar df_clean-en!"
assert df_clean.shape[0] == 98, "2 errenkada ezabatu behar ziren!"
print('✅ Zuzena!')


# %% [markdown] Cell 41
# **Ariketa 4.3:** `df_clean`-en, `tenperatura` > 150 den kasuetan, ordezkatu balio hori `df_clean['tenperatura'].median()`-rekin (mediana).


# %% [code] Cell 42
# Zure kodea hemen:
mediana = df_clean['tenperatura'].median()
df_clean.loc[df_clean['tenperatura'] > 150, 'tenperatura'] = mediana

# Balioztapena:
assert df_clean['tenperatura'].max() < 150, "Outlier-a kendu egin behar da!"
print('✅ Zuzena!')


# %% [markdown] Cell 43
# **Ariketa 4.4:** `df_clean`-en, `bibrazioa` < 0 den kasuetan, ordezkatu balio hori 0-rekin.


# %% [code] Cell 44
# Zure kodea hemen:
df_clean.loc[df_clean['bibrazioa'] < 0, 'bibrazioa'] = 0

# Balioztapena:
assert df_clean['bibrazioa'].min() >= 0, "Ez da balio negatiborik egon behar bibrazioan!"
print('✅ Zuzena!')


# %% [markdown] Cell 45
# **Ariketa 4.5:** Bihurtu `errorea` zutabea boolean motara (True 1 bada, False 0 bada) astype erabiliz. Gorde aldaketa `df_clean`-en bertan.


# %% [code] Cell 46
# Zure kodea hemen:
df_clean['errorea'] = df_clean['errorea'].astype(bool)

# Balioztapena:
assert df_clean['errorea'].dtype == bool, "Datu mota boolean izan behar da!"
print('✅ Zuzena!')


# %% [markdown] Cell 47
# ## 5. Seaborn


# %% [markdown] Cell 48
# Seaborn eta Matplotlib irudiak sortzeko erabiltzen dira. Ariketa hauetan, funtzioa egokia erabili irudiak ikusteko, eta gorde ardatzak aldagaian asertatzeko.


# %% [markdown] Cell 49
# **Ariketa 5.1:** Inportatu `seaborn` (`sns` bezala) eta `matplotlib.pyplot` (`plt` bezala).


# %% [code] Cell 50
# Zure kodea hemen:
import seaborn as sns
import matplotlib.pyplot as plt

# Balioztapena:
assert 'sns' in locals(), "seaborn inportatu behar da sns izenarekin!"
assert 'plt' in locals(), "matplotlib.pyplot inportatu behar da plt izenarekin!"
print('✅ Zuzena!')


# %% [markdown] Cell 51
# **Ariketa 5.2:** Egin `df_clean`-en `tenperatura` zutabearen histograma bat `sns.histplot` erabiliz. Gorde emaitza `ax` aldagaian.


# %% [code] Cell 52
# Zure kodea hemen:
fig, ax = plt.subplots(figsize=(6, 4))
sns.histplot(data=df_clean, x='tenperatura', ax=ax)
plt.show()

# Balioztapena:
assert ax is not None, "Irudiaren ardatza ax aldagaian gorde behar da!"
print('✅ Zuzena!')


# %% [markdown] Cell 53
# **Ariketa 5.3:** Egin scatter plot bat `sns.scatterplot` erabiliz, x-ardatzean `tenperatura` eta y-ardatzean `bibrazioa` jarriz. Datuak `df_clean` izan behar dira. Gorde emaitza `ax_scatter` aldagaian.


# %% [code] Cell 54
# Zure kodea hemen:
fig, ax_scatter = plt.subplots(figsize=(6, 4))
sns.scatterplot(data=df_clean, x='tenperatura', y='bibrazioa', ax=ax_scatter)
plt.show()

# Balioztapena:
assert ax_scatter is not None, "Gorde plot-a ax_scatter aldagaian!"
print('✅ Zuzena!')


# %% [markdown] Cell 55
# **Ariketa 5.4:** Egin boxplot bat `sns.boxplot` erabiliz. x-ardatzean `makina_id` jarri eta y-ardatzean `tenperatura`. Gorde `ax_box` aldagaian.


# %% [code] Cell 56
# Zure kodea hemen:
fig, ax_box = plt.subplots(figsize=(6, 4))
sns.boxplot(data=df_clean, x='makina_id', y='tenperatura', ax=ax_box)
plt.show()

# Balioztapena:
assert ax_box is not None, "Gorde plot-a ax_box aldagaian!"
print('✅ Zuzena!')


# %% [markdown] Cell 57
# **Ariketa 5.5:** Sortu korrelazio matrize bat `df_clean`-en zutabe numerikoekin, eta egin heatmap bat `sns.heatmap` erabiliz. Gorde heatmap-a `ax_heat` aldagaian.


# %% [code] Cell 58
# Zure kodea hemen:
corr_matrix = df_clean.select_dtypes(include=[np.number]).corr()
fig, ax_heat = plt.subplots(figsize=(6, 4))
sns.heatmap(corr_matrix, annot=True, ax=ax_heat)
plt.show()

# Balioztapena:
assert ax_heat is not None, "Gorde plot-a ax_heat aldagaian!"
print('✅ Zuzena!')
