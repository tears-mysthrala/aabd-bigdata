#!/usr/bin/env python3
# Auto-converted from 5073_1_Lengoaiak.ipynb
# Executable in VS Code (supports # %% interactive cells) or terminal via `python3`.


# %% [markdown] Cell 1
# # 1. Gaia · Lengoaiak eta Ingeniaritza — Python adibideak
# 
# 
# ---
# 
# Koaderno hau material didaktikoaren **osagarri exekutagarria** da. Apunteetan agertzen diren Python adibide guztiak hemen daude gelaxka exekutagarri gisa antolatuta, gai-egituraren arabera (§1 - §4).
# 
# Gelaxka bakoitza autonomoa izaten saiatu da: behar dituen inportazioak bertan daude, edo aurreko gelaxka batean argi adierazita.
# 
# **Oharra:** shell/bash komandoak (venv aktibatu, git, etab.) markdown gelaxketan agertzen dira erreferentziatzat. `pip install` komandoak `!pip install ...` magic moduan exekuta daitezke notebook-etik zuzenean.


# %% [markdown] Cell 2
# ## 1. Programa informatiko baten egitura eta AArako lengoaiak
# 
# Atal honetan programa baten oinarrizko anatomia ikusiko dugu: inportazioak, konstanteak, funtzioak, programa nagusia eta sarrera-puntua.
# 
# BOEko Errege Dekretuak (RD 279/2021) lehen ikaskuntza-emaitzaren oinarria da: lengoaiak karakterizatu eta haien egokitasuna baloratu.


# %% [markdown] Cell 3
# ### 1.1 Programa baten anatomia
# 
# Edozein Python programak bost zati nagusi izan ohi ditu: inportazioak, konstanteak, funtzioak, programa nagusia eta sarrera-puntua (`if __name__ == "__main__"`).
# 
# > **Oharra:** Beheko adibideak `input()` darabil, beraz notebook-ean exekutatzean zelda bat azalduko da idazteko. Nahi izanez gero `main()` funtzioaren `input(...)` deia kommentatu eta proba ezazu zatika.


# %% [code] Cell 4
# Programa baten egiturazko adibidea (Python)

# 1. Inportazioak — kanpoko paketeen kargaketa
import json
from pathlib import Path

# 2. Konstanteak eta konfigurazioa
MAX_AHALEGINAK = 3
KONFIG_PATH = Path("config.json")

# 3. Funtzioak — logika berreraikigarria
def kargatu_konfigurazioa(path: Path) -> dict:
    """Konfigurazio-fitxategia kargatu eta itzuli."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"lehenetsia": True}

# 4. Programa nagusia
def main():
    config = kargatu_konfigurazioa(KONFIG_PATH)

    for i in range(MAX_AHALEGINAK):
        izena = input("Sartu zure izena: ")
        if izena.strip():
            print(f"Kaixo, {izena}!")
            break
    else:
        print("Errorea: izen baliodun bat behar duzu.")

# 5. Sarrera-puntua — script gisa exekutatzean
if __name__ == "__main__":
    main()


# %% [markdown] Cell 5
# Ariketa 1.1 (soluzioa):


# %% [code] Cell 6
# @title
# 1. Shebang eta docstring (dokumentazio-burua)
#!/usr/bin/env python3
"""NIF baliozkotzaile soila.

Erabiltzaileari NIF bat eskatzen dio eta formatu zuzena duen
baieztatzen du (8 zenbaki + letra maiuskula bat).
"""

# 2. Inportazioak
import sys

# 3. Konstanteak
LETRAK = "TRWAGMYFPDXBNJZSQVHLCKE"
NIF_LUZERA = 9

# 4. Funtzioak
def nif_baliozkoa_da(nif: str) -> bool:
    """Egiaztatu NIF-aren formatua eta kontrol-letra."""
    nif = nif.strip().upper()
    if len(nif) != NIF_LUZERA:
        return False
    zenbaki_zatia, letra = nif[:8], nif[8]
    if not zenbaki_zatia.isdigit() or not letra.isalpha():
        return False
    espero_dena = LETRAK[int(zenbaki_zatia) % 23]
    return letra == espero_dena

# 5. main() funtzioa
def main() -> int:
    nif = input("Sartu zure NIF-a (8 zenbaki + letra): ")
    if nif_baliozkoa_da(nif):
        print("NIF zuzena da.")
        return 0
    print("NIF okerra.")
    return 1

# 6. Sarrera-puntua
if __name__ == "__main__":
    sys.exit(main())


# %% [markdown] Cell 7
# Zer gertatuko litzateke `if __name__ == "__main__"` lerroa ez bagenu
# sartuko? Noiz exekutatuko litzateke main() funtzioa?
# 
# ---
# 
# Baldintza jartzen ez baduzu eta `main()` zuzenean deitzen baduzu (adibidez, kodearen amaieran `main()` jarrita), `main()` funtzioa exekutatuko da fitxategia importatzen den bakoitzean (hau da: beti).
# 
# 
# 
# ```
# # fitxategia: adibidea.py
# 
# def main():
#     print("Programa nagusia martxan dago!")
# 
# if __name__ == "__main__":
#     main()
# ```
# 
# 
# 
# `adibidea.py` fitxategia zuzenean exekutatzen baduzu, Python-ek `__name__` aldagaiari "__main__" balioa ematen dionez `main()` exekutatzen da. Fitxategia importatzen baduzu (`import` tresnak), `__name__` aldagaiak "tresnak" balioa hartzen duenez baldintza ez da betetzen eta `main()` EZ da exekutatzen. Horri esker, Adibidea.py barruko funtzioak erabili ahal izango dituzu programa nagusia alferrik martxan jarri gabe.


# %% [markdown] Cell 8
# ## 2. Ingurune Profesionala
# 
# Atal honetan benetako lan-fluxua osatzen duten lau elementu nagusiak landuko ditugu: editorea (Antigravity), ingurune birtualak, pakete-kudeaketa (`pip`) eta dependentzien dokumentazioa (`requirements.txt`).


# %% [markdown] Cell 9
# ### 2.1 Antigravity (eta VS Code-ren oinordetza)
# 
# Antigravity Google-k 2025eko azaroan kaleratu zuen IDE-a da, Gemini 3 ereduarekin batera. VS Code-ren kode-oinarrian eraikita dago eta IA-agenteen koordinazioan zentratzen da (**Antigravity 2.0** eta **Antigravity IDE**).
# 
# Atal honek IDE-aren konfigurazioa lantzen du nagusiki (`settings.json`, luzapenak, lasterbideak); ez du Python kode exekutagarririk ekartzen, beraz koaderno honetan ez dago code cell-ik. Ikus MD dokumentuko 2.1 atala xehetasunetarako.


# %% [markdown] Cell 10
# ### 2.2 Ingurune Birtualak (venv eta conda)
# 
# Ingurune birtualek proiektu bakoitzari bere Python interprete eta paketeak isolatzeko aukera ematen diote. Komandoak shell-ekoak dira (ez Python), beraz hemen markdown gelaxka gisa daude.
# 
# **venv (Python estandarra):**
# ```bash
# # 1. Karpetan ingurune birtuala sortu
# python -m venv .venv
# 
# # 2. Aktibatu
# # Windows (PowerShell)
# .venv\Scripts\Activate.ps1
# # Linux / macOS
# source .venv/bin/activate
# 
# # 3. Aktibatuta dagoela egiaztatu — terminal-ean (.venv) agertuko da:
# # (.venv) C:\proiektua>
# 
# # 4. Paketeak instalatu (ingurune birtualean bakarrik)
# pip install numpy pandas
# 
# # 5. Desaktibatu
# deactivate
# ```
# 
# **conda:**
# ```bash
# # Ingurune berria sortu Python bertsio zehatzarekin
# conda create -n proiektua python=3.11
# 
# # Aktibatu
# conda activate proiektua
# 
# # Pakete bat instalatu
# conda install numpy
# ```


# %% [markdown] Cell 11
# ### 2.3 pip eta Pakete Kudeaketa
# 
# `pip` Python-en pakete-kudeatzaile ofiziala da, **PyPI** biltegi zentraletik paketeak deskargatzeko erabiltzen dena. Hauek dira komando arruntenak (shell-ean exekutatzen dira; notebook-ean `!` aurrizkiarekin):


# %% [code] Cell 12
# pip komandoak notebook-ean ! magic-arekin exekutatu daitezke.
# Adibide gisa, instalatutako paketeak zerrendatu:
# IPython magic: !pip list


# %% [markdown] Cell 13
# **Komando-erreferentzia osoa** (shell-ean edo `!` aurrizkiarekin notebook-ean):


# %% [code] Cell 14
# Pakete bat instalatu
# IPython magic: !pip install numpy

# Bertsio zehatz bat instalatu
# IPython magic: !pip install numpy==1.26.4

# Bertsio-tarte bat instalatu
#!pip install "numpy>=1.24,<2.0"

# Pakete bat eguneratu
#!pip install --upgrade numpy

# Pakete bat desinstalatu
# IPython magic: !pip uninstall numpy

# Instalatutako paketeak ikusi
# IPython magic: !pip list

# Pakete baten informazioa ikusi
# IPython magic: !pip show numpy


# %% [markdown] Cell 15
# ### 2.4 requirements.txt
# 
# `requirements.txt` proiektuaren dependentzia zehatzen "errezeta-fitxa" da — erreproduzigarritasunaren oinarria.
# 
# **Sortu eta erabili:**
# ```bash
# # Ingurune birtualean instalatutako guztia esportatu
# pip freeze > requirements.txt
# 
# # Ingurune berri batean dena instalatu
# pip install -r requirements.txt
# ```
# 
# **Adibide-eduki bat:**
# ```
# certifi==2024.2.2
# numpy==1.26.4
# pandas==2.2.1
# python-dateutil==2.9.0
# pytz==2024.1
# requests==2.31.0
# scikit-learn==1.4.0
# ```
# 
# **Egitura aurreratua (fitxategi anitz):**
# ```
# requirements/
# ├── base.txt       # Oinarrizko dependentziak
# ├── dev.txt        # Garapen tresnak (pytest, black)
# └── prod.txt       # Produkzio-bakarrak (gunicorn)
# ```


# %% [markdown] Cell 16
# ## 3. Python Aurreratua Datuetarako
# 
# Atal honek Python modu **pythonikoan** idazteko hiru teknika-multzo nagusi ekartzen ditu: list comprehensions, funtzio anonimoak (lambda/map/filter) eta datuen iraupena (JSON, YAML, Pickle).


# %% [markdown] Cell 17
# ### 3.1 List Comprehensions
# 
# List comprehensions Python-en zerrenda berriak modu labur eta adierazkorrean sortzeko bide nagusia dira. Matematikako multzoen notazioan inspiratuta daude.
# 
# Sintaxi orokorra:
# ```python
# emaitza = [espresioa for elementua in iterable if baldintza]
# #           ^^^^^^^^^  ^^^^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^
# #           zer egin   zertatik hartu           filtroa (aukerazkoa)
# ```


# %% [markdown] Cell 18
# **For loop tradizionala vs list comprehension** — biek emaitza bera ematen dute:


# %% [code] Cell 19
# Forma klasikoa: for loop
karratuak = []
for n in range(10):
    karratuak.append(n ** 2)
print(karratuak)

# Baliokidea list comprehension bidez
karratuak = [n ** 2 for n in range(10)]

print(karratuak)
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]


# %% [markdown] Cell 20
# **Baldintzekin** — `if` klausula erabiliz filtratu daitezke elementuak:


# %% [code] Cell 21
# Bikoitiak soilik
bikoitiak = [n for n in range(20) if n % 2 == 0]
print(bikoitiak)
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Zerrendako datu-garbiketa
datuak_gordinak = ["  Ane ", "MIKEL", " leire  ", "JON"]
datuak_garbi = [d.strip().capitalize() for d in datuak_gordinak]
print(datuak_garbi)
# ['Ane', 'Mikel', 'Leire', 'Jon']


# %% [markdown] Cell 22
# **Dictionary eta Set comprehensions** — patroi bera, baina `{}` artean:


# %% [code] Cell 23
# Dictionary comprehension
ikasleak = ["Ane", "Mikel", "Leire"]
notak = {ikaslea: 0 for ikaslea in ikasleak}
notak['Ane']=5
print(notak)
# {'Ane': 0, 'Mikel': 0, 'Leire': 0}

# Set comprehension (bikoiztuak kendu)
hitzak = ["kaixo", "mundua", "kaixo", "python", "mundua"]
bakanak = {h.capitalize() for h in hitzak}
print(bakanak)
# {'kaixo', 'mundua', 'python'}


# %% [markdown] Cell 24
# ### 3.2 Lambda, Map eta Filter
# 
# Pythonek paradigma funtzionaleko tresnak eskaintzen ditu: `lambda` (funtzio anonimoak), `map` (funtzioa aplikatu denei) eta `filter` (elementuak iragazi).


# %% [markdown] Cell 25
# **Lambda — funtzio anonimoak:** lerro bakarreko funtzio txikiak adierazteko.


# %% [code] Cell 26
# Funtzio arrunta
#def bikoiztu(x: int) -> int:
#    return x * 2

# Lambda baliokidea
bikoiztu = lambda x: x * 2

print(bikoiztu(5))   # 10


# %% [markdown] Cell 27
# **Lambda ordenatzeko gako gisa** — `sorted()`-ek `key` parametroan funtzio bat espero du, eta lambda perfektua da hortarako:


# %% [code] Cell 28
# Ordenatzeko gako gisa
produktuak = [
    {"izena": "sagarra", "prezioa": 1.2},
    {"izena": "platanoa", "prezioa": 0.8},
]
ordenatua = sorted(produktuak, key=lambda p: p["prezioa"])
print(ordenatua)


# %% [markdown] Cell 29
# **Map eta Filter** — datu-fluxu funtzionalak:


# %% [code] Cell 30
# map: funtzioa aplikatu elementu bakoitzari
zenbakiak = [1, 2, 3, 4, 5]
hirukoak = []
hirukoak = list(map(lambda x: x * 3, zenbakiak))
print(hirukoak)
# [3, 6, 9, 12, 15]

# filter: elementuak iragazi baldintza batekin
bikoitiak = list(filter(lambda x: x % 2 == 0, range(10)))
print(bikoitiak)
# [0, 2, 4, 6, 8]

# datu-pipeline funtzionala
bikoitien_karratuak = list(
    map(lambda x: x ** 2,
        filter(lambda x: x % 2 == 0, range(10))
        )
    )
print (bikoitien_karratuak)


# %% [markdown] Cell 31
# ### 3.3 Fitxategien Kudeaketa: JSON, YAML eta Pickle
# 
# Python-en datuak fitxategietatik irakurri eta idazteko hiru formatu nagusi erabiltzen ditugu, bakoitza bere kasu-erabilerarekin:
# 
# | Formatua | Mota | Erabilera tipikoa |
# |---|---|---|
# | **JSON** | Testua | API, web, datu-trukea |
# | **YAML** | Testua | Konfigurazioak (ML-parametroak, Docker, CI) |
# | **Pickle** | Bitarra | Python objektu osoak (ereduak, datu-egiturak) |


# %% [markdown] Cell 32
# #### JSON
# 
# JSON estandar zabalena da APIetan eta datu-trukean. Python-en `json` modulu estandarrak idatzi (`dump`) eta irakurri (`load`) ahalbidetzen du. Lehenik **idatzi** egingo dugu fitxategia, eta gero **irakurri**, gelaxkak modu independentean exekutatu ahal izateko.


# %% [code] Cell 33
import json

# IDATZI: Python dict → JSON fitxategia
datuak = {
    "bezeroak": ["Ane", "Mikel"],
    "kopurua": 2
}
with open("datuak.json", "w") as f:
    json.dump(datuak, f, indent=2, ensure_ascii=False)

print("datuak.json idatzita.")


# %% [code] Cell 34
import json

# IRAKURRI: JSON fitxategia → Python dict
with open("datuak.json", "r") as f:
    datuak = json.load(f)

print(datuak["bezeroak"])  # ['Ane', 'Mikel']


# %% [markdown] Cell 35
# #### YAML
# 
# YAML konfigurazio-fitxategi irakurterrazentzat erabiltzen da (ML hiperparametroak, Docker Compose, GitHub Actions...). Python-en `pyyaml` pakete kanpokoa behar du.
# 
# Beheko gelaxkan `pyyaml` instalatuko dugu notebook-etik bertatik (jada instalatuta badago, `pip`-ek aurreratu egingo du):


# %% [code] Cell 36
# pyyaml liburutegia instalatu (kanpokoa)
# IPython magic: !pip install pyyaml


# %% [code] Cell 37
import yaml

# Konfigurazio-fitxategia
yaml_testua = """
proiektua: AI-AA
parametroak:
  learning_rate: 0.001
  batch_size: 32
"""
konfig = yaml.safe_load(yaml_testua)
print(konfig["parametroak"]["learning_rate"]) # 0.001
print(konfig["proiektua"])  #AI-AA


# %% [markdown] Cell 38
# #### Pickle
# 
# Pickle Python-en barneko serializazio-formatu bitarra da. Edozein Python objektu byte-segidatara bihurtzen du eta itzulera berreraikitzen. ML ereduak (scikit-learn, etab.) gordetzeko oso erabilia.
# 
# > **Segurtasun-oharra**: ez kargatu inoiz fitxategi pickle ezezagunik — kode arbitrarioa exekutatzeko gai baita.


# %% [code] Cell 39
import pickle

# IDATZI: Python objektu konplexua serializatu eta gorde
eredua = {"pisuak": [0.5, -0.3, 0.8], "alborapena": 0.1} #weights and bias
with open("eredua.pkl", "wb") as f:
    pickle.dump(eredua, f)

print("eredua.pkl idatzita.")


# %% [code] Cell 40
import pickle

# IRAKURRI: berreskuratu Python objektua fitxategitik
with open("eredua.pkl", "rb") as f:
    eredu_berreskuratua = pickle.load(f)

print(eredu_berreskuratua)
# {"pisuak": [0.5, -0.3, 0.8], "alborapena": 0.1}


# %% [markdown] Cell 41
# ## 4. Bertsio Kontrola (Git)
# 
# Atal hau ia osorik shell-komandoetan oinarritzen da (`git ...`), beraz code cell Python exekutagarririk ez du. Hala ere, fluxu osoa hemen biltzen da erreferentziatzat.
# 
# Git-ek hiru egoera nagusi ditu: **Working directory** (zure ordenagailuko fitxategiak), **Staging area** (`git add`) eta **Repository** (`git commit`).


# %% [markdown] Cell 42
# ### 4.2 Oinarrizko Komandoak
# 
# **Konfigurazio hasierako (behin bakarrik):**
# ```bash
# git config --global user.name "Zure Izena"
# git config --global user.email "izena.abizena@uni.eus"
# ```
# 
# **Proiektua hasteko:**
# ```bash
# # Aukera 1: Biltegia hasieratu (proiektu berria)
# git init
# 
# # Aukera 2: Biltegia klonatu (dagoen proiektua)
# git clone https://github.com/erabiltzailea/proiektua.git
# ```
# 
# **Oinarrizko fluxua:**
# ```bash
# # 1. Egoera ikusi
# git status
# 
# # 2. Fitxategiak Staging area-ra gehitu
# git add fitxategia.py     # Fitxategi bakar bat
# git add .                 # Dena
# 
# # 3. Commit sortu
# git commit -m "feat: bezeroaren login funtzioa gehitu"
# 
# # 4. Historia ikusi
# git log
# git log --oneline --graph --all
# ```
# 
# **Commit-mezuen praktika ona (Conventional Commits):**
# ```bash
# # TXARRA
# git commit -m "aldaketak"
# git commit -m "gauza asko"
# 
# # ONA
# git commit -m "feat: bezero-modeloa sortu"
# git commit -m "fix: login API errore-kode okerra konpondu"
# git commit -m "docs: README eguneratu"
# git commit -m "test: bezero CRUD testak gehitu"
# ```


# %% [markdown] Cell 43
# ### 4.3 Branching eta Merging
# 
# ```bash
# # Branch berria sortu eta bertara aldatu
# git checkout -b ezaugarri-berria
# 
# # Branch-ak kudeatu
# git branch                    # Lokalak ikusi
# git branch -a                 # Lokalak + urrunekoak
# git checkout main             # Beste branch batera aldatu
# 
# # Branch ezabatu
# git branch -d ezaugarri-zaharra
# 
# # Merging: main-era itzuli eta branch-a batu
# git checkout main
# git merge ezaugarri-berria
# ```
# 
# **Merge conflict-aren itxura kodean:**
# 
# ```python
# <<<<<<< HEAD
# # Zure aldaketa
# def kalkulatu(x, y):
#     return x + y
# =======
# # Beste branch-aren aldaketa
# def kalkulatu(x, y, z):
#     return x + y + z
# >>>>>>> ezaugarri-berria
# ```
# 
# Erabaki zein bertsio mantendu (edo nahaste bat), markatzaileak (`<<<<<<<`, `=======`, `>>>>>>>`) kendu, eta gero `git add` + `git commit`.


# %% [markdown] Cell 44
# ### 4.4 Remote, .gitignore eta praktika onak
# 
# **Remote kudeaketa:**
# ```bash
# # Remote bat gehitu
# git remote add origin https://github.com/erabiltzailea/proiektua.git
# 
# # Push eta pull
# git push -u origin main          # Lehen push-a
# git push                          # Ondorengo push-ak
# git pull                          # Aldaketak jaitsi
# ```
# 
# **`.gitignore` Python proiektu baterako (oinarrizkoak):**
# ```gitignore
# # Ingurune birtualak
# .venv/
# venv/
# 
# # Python cache
# __pycache__/
# *.py[cod]
# *.egg-info/
# 
# # Sekretuak
# .env
# *.env
# credentials.json
# 
# # ML / Data
# *.pkl
# *.h5
# data/raw/
# 
# # IDE / sistema
# .vscode/settings.json
# .idea/
# .DS_Store
# 
# # Testing
# .pytest_cache/
# .coverage
# ```
# 
# **Praktika onak:**
# 
# 1. Commit txikiak eta maizagoak, mezu argiekin (Conventional Commits).
# 2. Inoiz ez push egin zuzenean `main`-era — beti pull request baten bidez.
# 3. Branch estrategia argia (Gitflow): `main`, `develop`, `feature/*`, `bugfix/*`, `hotfix/*`.
# 4. Sekretuen segurtasuna: inoiz ez committatu `.env` edo API-gakoak. Igo bada, giltza aldatu berehala.


# %% [markdown] Cell 45
# ## Eguneroko lan-fluxua
# 1. [Inizializazioa]    ▶   `git checkout develop`
#                                           `git pull` `git checkout -b feature/zeregina`
# 
# 2. [Programatu]      ▶  Fitxategiak aldatu
#                     `git add .`
#                   `git commit -m "zeregina eginda"`
# 
# 3. [Igo eta Eskatu]  ▶  `git push origin feature/zeregina`
#                           (GitHub-en Pull Request/ Gitlab-en Merge Request ireki)
# 
# 4. [Amaiera]         ▶  Taldekideek/irakasleak PR-a onartzen dutenean, zure kodea
#                           'develop'-era igaroko da automatikoki eta
#                           'feature/zeregina' adarra ezabatu egingo da.


# %% [markdown] Cell 46
# ## Amaierako lan-fluxua
# 
# 1. Lehenik 'main' adarrera joan `git checkout main`
# 
# 
# 
# 2. 'main' adarra eguneratuta dagoela ziurtatu `git pull origin main`
# 
# 3. 'develop'-eko aldaketak 'main' barruan batu (Merge)
# `git merge develop`
# 
# 4. Azkenik, 'main' berria zerbitzarira igo
# `git push origin main`


# %% [markdown] Cell 47
# ### **Laburpena**
# 
# Koaderno honetan gai osoaren Python kode exekutagarriak bildu dira:
# 
# - **§1** — Programa baten anatomia (inportazioak, konstanteak, funtzioak, `main`, `if __name__ == "__main__"`).
# - **§2** — Ingurune profesionala (Antigravity, venv, `pip`, `requirements.txt`). Gehienak shell-komandoak dira; `pip install` notebook-ean `!pip install ...` magic-arekin exekuta daiteke.
# - **§3** — Python aurreratua: list/dict/set comprehensions, `lambda`/`map`/`filter`, eta serializazioa (JSON, YAML, Pickle).
# - **§4** — Git fluxua: `init/clone`, `add/commit/log`, branch eta merge, `.gitignore`. Komando guztiak shell-ekoak dira.
