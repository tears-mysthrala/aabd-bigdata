#!/usr/bin/env python3
# Auto-converted from 5073_1_Lengoaiak_Ariketak.ipynb
# Executable in VS Code (supports # %% interactive cells) or terminal via `python3`.


# %% [markdown] Cell 1
# # 01 Lengoaiak Ariketak
# 
# Helburua: Python oinarriak, JSON, Terminala/Git, List Comprehensions, eta Funtzio Funtzionalak lantzea.


# %% [markdown] Cell 2
# ## Setup (Datuen sorkuntza)
# Lehenik, exekutatu hurrengo gelaxka datuak prestatzeko.


# %% [code] Cell 3
# @title
import os
import json
import pickle

os.makedirs('data', exist_ok=True)
with open('data/test.json', 'w') as f:
    json.dump({"erabiltzailea": "ikasle1", "puntuazioa": 95}, f)
with open('data/test.txt', 'w') as f:
    f.write("Kaixo mundua!\nPython ikasten ari gara.")

print("✅ Ingurunea prest! data/ karpeta eta fitxategiak sortu dira.")


# %% [markdown] Cell 4
# ## 1. Atala: JSON


# %% [markdown] Cell 5
# ### Ariketa 1.1
# Bihurtu hurrengo JSON katea Python hiztegi batean `json.loads` erabiliz.


# %% [code] Cell 6
import json
json_katea = '{"izena": "Mikel", "adina": 30}'

# Zure kodea hemen:
hiztegia = json.loads(json_katea)

# Egiaztapena
assert type(hiztegia) == dict, "Ez da hiztegia"
assert hiztegia["izena"] == "Mikel", "Balioa ez da zuzena"
print("✅ Zuzena!")


# %% [markdown] Cell 7
# ### Ariketa 1.2
# Hiztegi batetik JSON kate bat sortu `json.dumps` erabiliz.


# %% [code] Cell 8
hiztegi_berria = {"hiria": "Bilbo", "biztanleak": 346000}

# Zure kodea hemen:
json_emaitza = json.dumps(hiztegi_berria)

# Egiaztapena
assert type(json_emaitza) == str, "Ez da katea"
assert "Bilbo" in json_emaitza, "Balioa falta da"
print("✅ Zuzena!")


# %% [markdown] Cell 9
# ### Ariketa 1.3
# Irakurri `data/test.json` fitxategia eta gorde edukia `datuak_json` aldagaian.


# %% [code] Cell 10
# Zure kodea hemen:
with open('data/test.json', 'r', encoding='utf-8') as f:
    datuak_json = json.load(f)

# Egiaztapena
assert datuak_json["erabiltzailea"] == "ikasle1", "Eduki okerra"
print("✅ Zuzena!")


# %% [markdown] Cell 11
# ### Ariketa 1.4
# Gehitu 'aktiboa': True gako-balioa `datuak_json` hiztegian eta gorde `data/berria.json` fitxategian.


# %% [code] Cell 12
# Zure kodea hemen:
datuak_json['aktiboa'] = True
with open('data/berria.json', 'w', encoding='utf-8') as f:
    json.dump(datuak_json, f)

# Egiaztapena
import os
assert os.path.exists('data/berria.json'), "Fitxategia ez da sortu"
with open('data/berria.json', 'r', encoding='utf-8') as f:
    assert json.load(f).get("aktiboa") == True, "Balioa ez da gorde"
print("✅ Zuzena!")


# %% [markdown] Cell 13
# ### Ariketa 1.5
# Sortu JSON kate bat, formatu polita emanez (indent=4 erabiliz).


# %% [code] Cell 14
hiztegia = {"a": 1, "b": [2, 3]}

# Zure kodea hemen:
json_formatuduna = json.dumps(hiztegia, indent=4)

# Egiaztapena
assert "\n" in json_formatuduna and "    " in json_formatuduna, "Ez dirudi formatu polita duenik"
print("✅ Zuzena!")


# %% [markdown] Cell 15
# ## 2. Atala: Terminala, Venv eta Git
# Python Notebook batean komandoak `!` erabiliz exekutatu daitezke.


# %% [markdown] Cell 16
# ### Ariketa 2.1
# Erabili terminaleko komando bat uneko karpeta zein den ikusteko eta gorde irteera `uneko_karpeta` aldagaian (Adib: `uneko_karpeta = !pwd` edo `!cd` windows-en). Oharra: OS bidez egiaztatuko dugu.


# %% [code] Cell 17
import os
# Zure kodea hemen:
uneko_karpeta = os.getcwd()

# Egiaztapena
assert uneko_karpeta is not ..., "Aldagaia esleitu gabe"
print("✅ Zuzena!")


# %% [markdown] Cell 18
# ### Ariketa 2.2
# Sortu `data/karpeta_berria` direktorioa Python edo `!mkdir` erabiliz.


# %% [code] Cell 19
# Zure kodea hemen:
os.makedirs('data/karpeta_berria', exist_ok=True)

# Egiaztapena
assert os.path.exists('data/karpeta_berria'), "Karpeta ez da sortu"
print("✅ Zuzena!")


# %% [markdown] Cell 20
# ### Ariketa 2.3
# Sortu ingurune birtual bat `data/test_env` izenarekin. (Oharra: `!python -m venv data/test_env` erabili dezakezu)


# %% [code] Cell 21
# Zure kodea hemen:
import subprocess
subprocess.run(['uv', 'venv', '--clear', 'data/test_env'], check=True)

# Egiaztapena
assert os.path.exists('data/test_env') or os.path.exists('data/test_env/Scripts') or os.path.exists('data/test_env/bin'), "Ingurunea ez da ondo sortu"
print("✅ Zuzena!")


# %% [markdown] Cell 22
# ### Ariketa 2.4
# Hasieratu Git biltegi bat `data/karpeta_berria` karpetan. (`!git init data/karpeta_berria`)


# %% [code] Cell 23
# Zure kodea hemen:
subprocess.run(['git', 'init', 'data/karpeta_berria'], check=True)

# Egiaztapena
assert os.path.exists('data/karpeta_berria/.git'), "Git biltegia ez da hasieratu"
print("✅ Zuzena!")


# %% [markdown] Cell 24
# ### Ariketa 2.5
# Idatzi 'Erantzuna' testua `data/karpeta_berria/readme.md` fitxategian, gero gehitu Git-era (add). `!git -C data/karpeta_berria add readme.md`


# %% [code] Cell 25
# Zure kodea hemen:
with open('data/karpeta_berria/readme.md', 'w', encoding='utf-8') as f:
    f.write('Erantzuna\n')
subprocess.run(['git', '-C', 'data/karpeta_berria', 'add', 'readme.md'], check=True)

# Egiaztapena
assert os.path.exists('data/karpeta_berria/readme.md'), "Fitxategia falta da"
res = subprocess.run(['git', '-C', 'data/karpeta_berria', 'status', '--porcelain'], capture_output=True, text=True)
assert 'readme.md' in res.stdout, "Ez dago git add eginda"
print("✅ Zuzena!")


# %% [markdown] Cell 26
# ## 3. Atala: List Comprehensions


# %% [markdown] Cell 27
# ### Ariketa 3.1
# Sortu 1-etik 10-era bitarteko zenbakien karratuen zerrenda `karratuak` aldagaian.


# %% [code] Cell 28
# Zure kodea hemen:
karratuak = [x**2 for x in range(1, 11)]

# Egiaztapena
assert karratuak == [1, 4, 9, 16, 25, 36, 49, 64, 81, 100], "Erantzuna okerra da"
print("✅ Zuzena!")


# %% [markdown] Cell 29
# ### Ariketa 3.2
# Eman zerrenda honetako zenbaki bikoitiak bakarrik: `zenbakiak = [1,2,3,4,5,6,7,8]`


# %% [code] Cell 30
zenbakiak = [1, 2, 3, 4, 5, 6, 7, 8]

# Zure kodea hemen:
bikoitiak = [x for x in zenbakiak if x % 2 == 0]

# Egiaztapena
assert bikoitiak == [2, 4, 6, 8], "Bikoitiak oker"
print("✅ Zuzena!")


# %% [markdown] Cell 31
# ### Ariketa 3.3
# Bihurtu hitz guztiak maiuskulara: `hitzak = ['kaixo', 'mundua', 'python']`


# %% [code] Cell 32
hitzak = ['kaixo', 'mundua', 'python']

# Zure kodea hemen:
maiuskulak = [h.upper() for h in hitzak]

# Egiaztapena
assert maiuskulak == ['KAIXO', 'MUNDUA', 'PYTHON'], "Oker"
print("✅ Zuzena!")


# %% [markdown] Cell 33
# ### Ariketa 3.4
# Atera hitz bakoitzaren lehenengo letra: `hitzak = ['sagarra', 'madaria', 'laranja']`


# %% [code] Cell 34
hitzak = ['sagarra', 'madaria', 'laranja']

# Zure kodea hemen:
lehen_letrak = [h[0] for h in hitzak]

# Egiaztapena
assert lehen_letrak == ['s', 'm', 'l'], "Oker"
print("✅ Zuzena!")


# %% [markdown] Cell 35
# ### Ariketa 3.5
# Bihurtu matrize hau 1D zerrenda batean (flatten): `matrizea = [[1,2], [3,4], [5,6]]`


# %% [code] Cell 36
matrizea = [[1,2], [3,4], [5,6]]

# Zure kodea hemen:
laua = [elem for lerro in matrizea for elem in lerro]

# Egiaztapena
assert laua == [1, 2, 3, 4, 5, 6], "Oker"
print("✅ Zuzena!")


# %% [markdown] Cell 37
# ## 4. Atala: Lambda, Map, Filter


# %% [markdown] Cell 38
# ### Ariketa 4.1
# Sortu `biderkatu` izeneko lambda funtzio bat bi zenbaki jasotzen dituena eta haien biderkadura itzultzen duena.


# %% [code] Cell 39
# Zure kodea hemen:
biderkatu = lambda a, b: a * b

# Egiaztapena
assert biderkatu(3, 4) == 12, "Oker"
assert biderkatu(5, -2) == -10, "Oker"
print("✅ Zuzena!")


# %% [markdown] Cell 40
# ### Ariketa 4.2
# Erabili `map` zerrendako zenbaki bakoitza bikoizteko. `zenbakiak = [1, 2, 3, 4]`


# %% [code] Cell 41
zenbakiak = [1, 2, 3, 4]

# Zure kodea hemen:
bikoiztuak = list(map(lambda x: x * 2, zenbakiak))

# Egiaztapena
assert list(bikoiztuak) == [2, 4, 6, 8], "Oker"
print("✅ Zuzena!")


# %% [markdown] Cell 42
# ### Ariketa 4.3
# Erabili `filter` zerrendatik bokalekin hasten diren hitzak uzteko. `hitzak = ['ana', 'peru', 'iker', 'jon', 'elene']`


# %% [code] Cell 43
hitzak = ['ana', 'peru', 'iker', 'jon', 'elene']

# Zure kodea hemen:
bokal_hitzak = list(filter(lambda h: h[0].lower() in 'aeiou', hitzak))

# Egiaztapena
assert list(bokal_hitzak) == ['ana', 'iker', 'elene'], "Oker"
print("✅ Zuzena!")


# %% [markdown] Cell 44
# ### Ariketa 4.4
# Ordenatu ikasleen zerrenda (tuplak) haien notaren arabera (bigarren elementua) lambda erabiliz txikienetik handienera. `ikasleak = [('Ane', 8), ('Jon', 5), ('Mikel', 9)]`


# %% [code] Cell 45
ikasleak = [('Ane', 8), ('Jon', 5), ('Mikel', 9)]

# Zure kodea hemen:
ordenatuak = sorted(ikasleak, key=lambda x: x[1])

# Egiaztapena
assert ordenatuak == [('Jon', 5), ('Ane', 8), ('Mikel', 9)], "Oker"
print("✅ Zuzena!")


# %% [markdown] Cell 46
# ### Ariketa 4.5
# Konbinatu `map` eta `filter`: Lehenik iragazi 5 baino handiagoak diren zenbakiak, eta gero bikoiztu. `zenbakiak = [2, 8, 4, 7, 1]`


# %% [code] Cell 47
zenbakiak = [2, 8, 4, 7, 1]

# Zure kodea hemen:
emaitza = list(map(lambda x: x * 2, filter(lambda x: x > 5, zenbakiak)))

# Egiaztapena
assert list(emaitza) == [16, 14], "Oker"
print("✅ Zuzena!")


# %% [markdown] Cell 48
# ## 5. Atala: Fitxategiak (Pickle eta JSON)


# %% [markdown] Cell 49
# ### Ariketa 5.1
# Idatzi 'Epa!' testua `data/agurra.txt` fitxategian.


# %% [code] Cell 50
# Zure kodea hemen:
with open('data/agurra.txt', 'w', encoding='utf-8') as f:
    f.write('Epa!\n')

# Egiaztapena
assert os.path.exists('data/agurra.txt'), "Falta da"
with open('data/agurra.txt', 'r', encoding='utf-8') as f:
    assert 'Epa!' in f.read(), "Testua ez da zuzena"
print("✅ Zuzena!")


# %% [markdown] Cell 51
# ### Ariketa 5.2
# Irakurri `data/test.txt` fitxategiaren lerro guztiak zerrenda batean `lerroak` izeneko aldagaian.


# %% [code] Cell 52
# Zure kodea hemen:
with open('data/test.txt', 'r', encoding='utf-8') as f:
    lerroak = f.readlines()

# Egiaztapena
assert type(lerroak) == list, "Ez da zerrenda"
assert 'Kaixo mundua!\n' in lerroak or 'Kaixo mundua!' in lerroak[0], "Edukia okerra da"
print("✅ Zuzena!")


# %% [markdown] Cell 53
# ### Ariketa 5.3
# Gorde `nire_hiztegia` pickle erabiliz `data/datuak.pkl` fitxategian.


# %% [code] Cell 54
import pickle
nire_hiztegia = {"zenbakiak": [1,2,3], "testua": "adibidea"}

# Zure kodea hemen:
with open('data/datuak.pkl', 'wb') as f:
    pickle.dump(nire_hiztegia, f)

# Egiaztapena
assert os.path.exists('data/datuak.pkl'), "Falta da"
print("✅ Zuzena!")


# %% [markdown] Cell 55
# ### Ariketa 5.4
# Irakurri `data/datuak.pkl` pickle fitxategitik eta gorde `kargatutakoa` aldagaian.


# %% [code] Cell 56
# Zure kodea hemen:
with open('data/datuak.pkl', 'rb') as f:
    kargatutakoa = pickle.load(f)

# Egiaztapena
assert kargatutakoa == {"zenbakiak": [1,2,3], "testua": "adibidea"}, "Oker kargatua"
print("✅ Zuzena!")


# %% [markdown] Cell 57
# ### Ariketa 5.5
# Irakurri `data/test.json`, aldatu 'puntuazioa' 100-era, eta gorde berriz izen berarekin (`data/test.json`).


# %% [code] Cell 58
# Zure kodea hemen:
with open('data/test.json', 'r', encoding='utf-8') as f:
    d = json.load(f)
d['puntuazioa'] = 100
with open('data/test.json', 'w', encoding='utf-8') as f:
    json.dump(d, f)

# Egiaztapena
with open('data/test.json', 'r', encoding='utf-8') as f:
    berria = json.load(f)
assert berria.get("puntuazioa") == 100, "Ez da eguneratu"
print("✅ Zuzena!")
