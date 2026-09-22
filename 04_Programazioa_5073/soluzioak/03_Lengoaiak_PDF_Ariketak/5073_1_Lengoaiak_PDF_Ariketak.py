# -*- coding: utf-8 -*-
"""5073_1_Lengoaiak_PDF_Ariketak - Soluzio Exekutagarria VS Code / Spyder-entzat."""

# %%
# """
# # 5073 - Lengoaiak eta Datu Zientzia
# ## 1. Gaia: Programazio-Lengoaiak (PDF-ko Ariketa Guztien Ebazpena)
# 
# Dokumentu honek `5073_1_Lengoaiak.pdf` apunteetan proposatutako **ariketa praktiko guztiak** ebazten ditu urratsez urrats, azalpen teoriko zehatzekin, kode exekutagarriarekin eta egiaztapen automatikoekin:
# - **Ariketa 1.1**: Python script-aren anatomia (NIF balioztatzaile profesionala).
# - **Ariketa 1.2**: Lengoaien aukeraketa 4 enpresa errealetan (Glovo, BBVA, Roche, Vodafone).
# - **Ariketa 1.3**: Datu-formatuen transformazioa (JSON $\rightarrow$ YAML & XML konparaketa).
# - **Ariketa 2.1 - 2.5**: Garapen ingurunea, `venv`, `pip` dependentziak, `requirements.txt`, `AGENTS.md` eta Prompt Ingeniaritza.
# - **Ariketa 3.1 - 3.3**: Hiztegiak, List Comprehensions, Lambda/Map/Filter eta JSON/YAML fitxategien kudeaketa.
# - **Ariketa 4.1 - 4.4**: Git bertsio-kontrola, Conventional Commits, Branching, `.gitignore` eta PR txantiloiak.
# """

# %%
# """
# ---
# ## 🧩 Ariketa 1.1 · Python script-aren anatomia (NIF Balioztatzailea)
# **Egoera:** Eskolako programatze-laguntzailea zara.  
# **Eginkizuna:** Sortu NIF (NAN/IFZ) balioztatzaile oso bat Python script estandar baten 6 osagai nagusiak erabiliz:
# 1. Modulu-mailako docstring deskribatzailea
# 2. Inportazio estandarrak eta tipo-oharpenak (`typing`)
# 3. Konstante globalak (`HITZ_LARRIAK`)
# 4. Funtzio modularrak docstring eta salbuespenekin (`modulo 23` kalkulua)
# 5. Datuen sarrera eta balioztatzea
# 6. `if __name__ == "__main__":` blokea eta irteera-kodeak.
# """

# %%
from __future__ import annotations
import re
import sys
from typing import Final

# 1. Konstante globalak
NIF_LETRAK: Final[str] = "TRWAGMYFPDXBNJZSQVHLCKE"
NIF_PATROIA: Final[re.Pattern[str]] = re.compile(r"^(\d{8})([A-Z])$")

def kontrol_letra_kalkulatu(zenbakiak: int) -> str:
    """NIF zenbakiei dagokien kontrol-letra kalkulatzen du modulo 23 bidez."""
    if zenbakiak < 0 or zenbakiak > 99_999_999:
        raise ValueError(f"Zenbakiak 0 eta 99999999 artean egon behar du: {zenbakiak}")
    return NIF_LETRAK[zenbakiak % 23]

def nif_balioztatu(nif: str) -> tuple[bool, str]:
    """NIF katea balioztatzen du."""
    garbia = nif.strip().upper().replace("-", "").replace(" ", "")
    bat_dator = NIF_PATROIA.match(garbia)
    if not bat_dator:
        return False, f"Formatu baliogabea ('{nif}'). 8 digitu eta letra bat behar dira."
    
    zenbaki_str, emandako_letra = bat_dator.groups()
    zenbakiak = int(zenbaki_str)
    espero_letra = kontrol_letra_kalkulatu(zenbakiak)
    
    if emandako_letra != espero_letra:
        return False, f"Kontrol-letra okerra: emandakoa '{emandako_letra}', espero zena '{espero_letra}'."
    
    return True, f"NIF zuzena eta baliozkoa da: {zenbaki_str}{emandako_letra}."

# Proba kasuak
test_kasuak = [
    ("12345678Z", True),   # 12345678 % 23 = 14 -> Z
    ("00000000T", True),   # 0 % 23 = 0 -> T
    ("44332211X", True),   # 44332211 % 23 = 10 -> X
    ("12345678A", False),  # Letra okerra (Z behar luke)
    ("12345-X", False),    # Digitu gutxiegi
    ("123456789Z", False)  # Digitu gehiegi
]

print("=== NIF BALIOZTATZAILEAREN PROBAK ===")
for nif_test, espero_balioa in test_kasuak:
    baliozkoa, mezua = nif_balioztatu(nif_test)
    assert baliozkoa == espero_balioa, f"Errorea {nif_test}-rekin!"
    ikurra = "✅" if baliozkoa else "❌"
    print(f"{ikurra} {nif_test:12} -> {mezua}")

# %%
# """
# ---
# ## 🧩 Ariketa 1.2 · Lengoaien Aukeraketa (Enpresen Ebaluazioa)
# **Egoera:** 4 enpresatan praktikak egiteko aukera duzu:
# 1. **Glovo (Bartzelona)** — *Python + Go*
# 2. **BBVA (Madril)** — *Java + Python*
# 3. **Roche (Basilea)** — *R + Python*
# 4. **Vodafone (Madril)** — *Java + NodeJS*
# 
# **Eginkizuna:** Hautatu enpresa bat (edo guztiak aztertu), arrazoitu zergatik, zein lengoaiak ikasi beharko liratekeen aurretik, eta zein liburutegi nagusi.
# """

# %%
import pandas as pd

enpresak_datuak = [
    {
        "Enpresa": "Glovo (Bartzelona)",
        "Lengoaiak": "Python + Go",
        "Arkitektura & Xedea": "Eskaerak denbora errealean kudeatu, entrega-ibilbideak optimizatu eta mezularitza arina.",
        "Zergatik konbinazio hau?": "Go: konkurrentzia itzela (goroutines), latenzia minimoa mikrozerbitzuetan. Python: ML ereduak ibilbideen kalkulurako eta datu-analisia.",
        "Ikasi beharreko liburutegiak": "Python (FastAPI, Scikit-learn, Celery) | Go (Gin/Fiber, Goroutines, gRPC)"
    },
    {
        "Enpresa": "BBVA (Madril)",
        "Lengoaiak": "Java + Python",
        "Arkitektura & Xedea": "Banku-transakzio kritikoak, iruzur-detekzioa (fraud detection) eta arriskuen kalkulua.",
        "Zergatik konbinazio hau?": "Java: transakzio segurtasuna, sendotasuna eta Spring Boot ekosistema. Python: FinTech arrisku ereduak, PySpark eta Big Data.",
        "Ikasi beharreko liburutegiak": "Java (Spring Boot, Hibernate, Kafka) | Python (pandas, PySpark, scikit-learn, XGBoost)"
    },
    {
        "Enpresa": "Roche (Basilea)",
        "Lengoaiak": "R + Python",
        "Arkitektura & Xedea": "Entsegu klinikoak, genomika, ikerketa biomedikoa eta medikuntza pertsonalizatua.",
        "Zergatik konbinazio hau?": "R: ikerketa estatistiko zorrotza eta bioinformatika. Python: Deep Learning (irudi medikoak) eta datu-ingeniaritza orokorra.",
        "Ikasi beharreko liburutegiak": "R (ggplot2, Bioconductor, tidyverse) | Python (PyTorch, Biopython, pandas, NumPy)"
    },
    {
        "Enpresa": "Vodafone (Madril)",
        "Lengoaiak": "Java + NodeJS",
        "Arkitektura & Xedea": "Telekomunikazio sareen kudeaketa, bezeroen atari digitalak eta gertaeretara bideratutako APIak.",
        "Zergatik konbinazio hau?": "NodeJS: asinkronotasuna (event loop) eta I/O azkarra API atarietan. Java: backend sakona, fakturazio sistemak eta egonkortasuna.",
        "Ikasi beharreko liburutegiak": "NodeJS (Express, NestJS, Socket.io) | Java (Spring Cloud, Quarkus, Apache Camel)"
    }
]

df_enpresak = pd.DataFrame(enpresak_datuak)
print("=== ENPRESEN TEKNOLOGIA-STACKEN EBALUAZIOA ===")
for _, r in df_enpresak.iterrows():
    print(f"\n🏢 {r['Enpresa']} -> {r['Lengoaiak']}")
    print(f"   🎯 Arkitektura: {r['Arkitektura & Xedea']}")
    print(f"   💡 Arrazoia:    {r['Zergatik konbinazio hau?']}")
    print(f"   📦 Liburutegiak:{r['Ikasi beharreko liburutegiak']}")

# %%
# """
# ---
# ## 🧩 Ariketa 1.3 · Datu-Formatuak (JSON $\rightarrow$ YAML & XML)
# **Egoera:** Gemini API-tik 5 bezeroren erosketa-erregistroa jaso duzu JSON formatuan.  
# **Eginkizuna:**
# 1. Bihurtu erregistro hori YAML formatura.
# 2. Bihurtu XML formatura.
# 3. Erantzun: *Zer egingo zenuke datuak XML formatuan jaso bazenitu? Zergatik du JSON-ek abantaila web APIetan?*
# """

# %%
import json
import yaml
import xml.etree.ElementTree as ET

json_testua = """{
  "bezeroak": [
    {"id": "001", "izena": "Ane", "erosketa": 89.50},
    {"id": "002", "izena": "Mikel", "erosketa": 23.10},
    {"id": "003", "izena": "Leire", "erosketa": 145.00},
    {"id": "004", "izena": "Jon", "erosketa": 12.75},
    {"id": "005", "izena": "Maite", "erosketa": 67.90}
  ]
}"""

# 1. JSON kargatu
datuak = json.loads(json_testua)

# 2. YAML bihurtu
yaml_irteera = yaml.dump(datuak, sort_keys=False, allow_unicode=True)
print("=== 1. YAML FORMATUA ===")
print(yaml_irteera)

# 3. XML bihurtu
root = ET.Element("datuak")
bezeroak_elem = ET.SubElement(root, "bezeroak")
for b in datuak["bezeroak"]:
    b_elem = ET.SubElement(bezeroak_elem, "bezeroa", id=b["id"])
    izena_elem = ET.SubElement(b_elem, "izena")
    izena_elem.text = b["izena"]
    erosketa_elem = ET.SubElement(b_elem, "erosketa")
    erosketa_elem.text = str(b["erosketa"])

xml_irteera = ET.tostring(root, encoding="utf-8").decode("utf-8")
print("=== 2. XML FORMATUA ===")
print(xml_irteera)

# 4. Fitxategi-tamainen konparaketa (byte-kopurua)
print("=== 3. FORMATUEN TAMAINA-KONPARAKETA ===")
print(f"JSON tamaina: {len(json_testua.encode('utf-8'))} bytes")
print(f"YAML tamaina: {len(yaml_irteera.encode('utf-8'))} bytes")
print(f"XML tamaina:  {len(xml_irteera.encode('utf-8'))} bytes")

# %%
# """
# ### 💡 Galderaren Erantzuna: Zergatik du JSON-ek abantaila XML-ren aldean?
# 1. **Lerrorik eta etiketa bikoitzik gabea**: XML-k etiketa ireki eta itxiak behar ditu (`<izena>Ane</izena>`), datuen tamaina artifizialki handituz (%30-%50 gehiago sarean).
# 2. **Serializazio naturala**: JSON zuzenean mapatzen da programazio-lengoaia modernoen funtsezko datu-egituretara (Python `dict`/`list`, JavaScript `Object`/`Array`). XML-k ordea parseatzaile bereziak behar ditu (DOM/SAX) eta zuhaitz-egitura konplexuak sortzen ditu.
# 3. **Erabilera eremua**:
#    - **JSON**: Web APIak, mikrotraferak, REST zerbitzuak.
#    - **YAML**: Giza irakurlearentzako konfigurazio fitxategiak (Docker compose, Kubernetes, GitHub Actions).
#    - **XML**: Datu konplexu eta balioztapen zorrotza (XSD eskema bidez) behar duten industria/finantza protokolo zaharrak (SOAP, ISO 20022).
# """

# %%
# """
# ---
# ## 🧩 Ariketa 2.1 - 2.4 · Garapen Ingurunea, venv eta pip Pakete Kudeaketa
# - **Ariketa 2.1**: Antigravity IDE konfigurazioa eta lehen funtzio laguntzailea.
# - **Ariketa 2.2**: Ingurune birtualen isolamendua (`venv`). Zergatik ematen du `ModuleNotFoundError` ingurunea desaktibatzean?
# - **Ariketa 2.3**: `pip install` eta dependentzia trantsitiboak (`requests`, `pandas`, `scikit-learn`).
# - **Ariketa 2.4**: `requirements.txt` eta erreproduzigarritasuna.
# """

# %%
# Ariketa 2.1: Agur funtzioa (3 parametro: izena, adina, herria)
def sortu_agur_osoa(izena: str, adina: int, herria: str) -> str:
    """3 parametro hartu eta agur egituratu eta pertsonalizatua itzultzen du."""
    return f"Kaixo {izena}! {herria}(e)tik zatoz eta {adina} urte dituzu. Ongi etorri Antigravity laborategira!"

print("Ariketa 2.1 emaitza:")
print(sortu_agur_osoa("Ane", 24, "Donostia"))

# Ariketa 2.2 & 2.3: Dependentzien analisia
dependentzia_analisia = {
    "requests": ["urllib3", "certifi", "charset-normalizer", "idna"],
    "pandas": ["numpy", "python-dateutil", "pytz", "tzdata"],
    "scikit-learn": ["numpy", "scipy", "joblib", "threadpoolctl"]
}

print("\nAriketa 2.3: Zergatik gehitzen dira hainbeste pakete 'pip install' egitean?")
print("Trantsitibotasunaren printzipioa: pakete nagusi bakoitzak bere lanerako behar dituen azpi-liburutegiak ekartzen ditu:")
for paketea, azpipaketeak in dependentzia_analisia.items():
    print(f"📦 {paketea:12} -> gehitutako dependentziak: {', '.join(azpipaketeak)}")

# %%
# """
# ---
# ## 🧩 Ariketa 2.5 · Agenteak, AGENTS.md eta Prompt Ingeniaritza
# **Eginkizuna:**
# 1. Sortu `AGENTS.md` arau-fitxategi bat (xedea, Python bertsioa, hizkuntza arauak, debekatutako metodoak `eval()`, `pickle.load()`).
# 2. Prompt-konparaketa: Prompt orokorra vs Prompt egituratua (rol, testuinguru, murrizketa eta irteera argiarekin).
# """

# %%
prompt_konparaketa = {
    "Prompt_A (Lausoa)": {
        "Testua": "Egin funtzio bat CSV fitxategi bat irakurri eta estatistikak ateratzeko.",
        "Arazoak": "Ez ditu zehazten tipo-oharpenak, errore-kudeaketa (fitxategirik ez badago), zein estatistika mota nahi diren, ezta irteerako datu-formatua ere."
    },
    "Prompt_B (Egituratua & Zehatza)": {
        "Testua": (
            "Python 3.13 eta pandas erabiliz, idatzi `kargatu_eta_aztertu_salmentak(bidea: Path) -> dict[str, float]` funtzioa. "
            "Baldintzak: 1) FileNotFoundError kudeatu mezua emanez. 2) Batezbestekoa, mediana eta batura kalkulatu. "
            "3) PEP 8 eta tipo-oharpen zorrotzak erabili. 4) Debekatuta dago eval() edo kanpoko mendekotasun arraroak erabiltzea."
        ),
        "Abantailak": "Emaitza determinista, segurua, ekoizpenerako prest dagoena eta proiektuaren AGENTS.md arauekin %100 bat datorrena lortzen da."
    }
}

print("=== PROMPT-INGENIARITZA KONPARAKETA ===")
for izena, datua in prompt_konparaketa.items():
    print(f"\n[{izena}]")
    print(f"📝 Testua: {datua['Testua']}")
    print(f"🔍 Analisia: {datua.get('Arazoak') or datua.get('Abantailak')}")

# %%
# """
# ---
# ## 🧩 Ariketa 3.1 & 3.2 · List Comprehensions vs Funtzionala (Lambda, Map, Filter)
# - **Ariketa 3.1**: Ikasleen zerrenda hiztegiekin. Gaindituak lortu, hiztegi bihurtu eta batezbestekoa kalkulatu.
# - **Ariketa 3.2**: Zenbaki bikoitien karratuak: `map` + `filter` vs `list comprehension`.
# """

# %%
# Ariketa 3.1
ikasleak = [
    {"izena": "Ane", "nota": 7.5},
    {"izena": "Mikel", "nota": 4.0},
    {"izena": "Leire", "nota": 9.2},
    {"izena": "Jon", "nota": 3.8},
    {"izena": "Maite", "nota": 8.0}
]

# 1. Gainditu duten ikasleak (nota >= 5)
gaindituak = [i["izena"] for i in ikasleak if i["nota"] >= 5.0]

# 2. Hiztegi berria: izena -> nota
ikasle_hiztegia = {i["izena"]: i["nota"] for i in ikasleak}

# 3. Batez besteko nota
batez_bestekoa = sum(i["nota"] for i in ikasleak) / len(ikasleak)

print("=== ARIKETA 3.1 EMAITZAK ===")
print(f"Gaindituak ({len(gaindituak)}): {gaindituak}")
print(f"Ikasle hiztegia: {ikasle_hiztegia}")
print(f"Klasearen batez besteko nota: {batez_bestekoa:.2f}")

# Ariketa 3.2
zenbakiak = [1, 2, 3, 4, 5, 6]

# Modu funtzionala (lambda + map + filter)
emaitza_funtzionala = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, zenbakiak)))

# List comprehension bidez
emaitza_comprehension = [x**2 for x in zenbakiak if x % 2 == 0]

assert emaitza_funtzionala == emaitza_comprehension == [4, 16, 36]
print("\n=== ARIKETA 3.2 EMAITZAK ===")
print(f"Hasierako zerrenda:     {zenbakiak}")
print(f"Funtzionala (map/filter): {emaitza_funtzionala}")
print(f"List comprehension:      {emaitza_comprehension}")
print("Irakurgarritasuna: Python komunitatean (PEP 20) 'List Comprehension' askoz hobetsiagoa da, irakurtzeko argiagoa eta zuzenagoa delako.")

# %%
# """
# ---
# ## 🧩 Ariketa 3.3 · Fitxategien Kudeaketa: JSON eta YAML
# **Egoera:** Hipermerkatu batek produktu-katalogo bat dauka (izena, prezioa, kategoria, stock).  
# **Eginkizuna:**
# 1. Sortu 5 produkturen datuak.
# 2. Gorde `katalogoa.json` gisa.
# 3. Gorde `katalogoa.yaml` gisa.
# 4. Berrirakurri biak eta egiaztatu datuen osotasuna berdina dela (`assert`).
# """

# %%
import json
import yaml
from pathlib import Path

katalogoa = [
    {"id": 101, "izena": "Esne Osoa 1L", "kategoria": "Elikadura", "prezioa": 1.15, "stock": 250},
    {"id": 102, "izena": "Oliba Olio Birjina 1L", "kategoria": "Elikadura", "prezioa": 8.90, "stock": 80},
    {"id": 103, "izena": "Garbigarri Ekologikoa", "kategoria": "Garbiketa", "prezioa": 3.45, "stock": 45},
    {"id": 104, "izena": "Hortzetako Pasta", "kategoria": "Higienea", "prezioa": 2.20, "stock": 120},
    {"id": 105, "izena": "Sagar Gorriak 1kg", "kategoria": "Frutak", "prezioa": 2.10, "stock": 190}
]

fitx_json = Path("katalogoa.json")
fitx_yaml = Path("katalogoa.yaml")

# 1. Gorde JSON
with open(fitx_json, "w", encoding="utf-8") as f:
    json.dump(katalogoa, f, indent=2, ensure_ascii=False)

# 2. Gorde YAML
with open(fitx_yaml, "w", encoding="utf-8") as f:
    yaml.dump(katalogoa, f, sort_keys=False, allow_unicode=True)

# 3. Irakurri eta egiaztatu
with open(fitx_json, "r", encoding="utf-8") as f:
    json_kargatua = json.load(f)

with open(fitx_yaml, "r", encoding="utf-8") as f:
    yaml_kargatua = yaml.safe_load(f)

assert json_kargatua == yaml_kargatua == katalogoa, "Errorea: Datuak ez datoz bat!"
print("✅ JSON eta YAML fitxategiak zuzen sortu, gorde eta berrirakurri dira bat etorriz.")
print(f"Produktuak guztira: {len(json_kargatua)}")

# %%
# """
# ---
# ## 🧩 Ariketa 4.1 - 4.4 · Git Bertsio Kontrola, Lan-fluxuak eta Praktika Onak
# - **Ariketa 4.1**: Git ezartzeko 3 arrazoi nagusi enpresa batean.
# - **Ariketa 4.2**: Git hasieratzea, `agur.py` eta Conventional Commits (`feat:`, `refactor:`).
# - **Ariketa 4.3**: Branching (`feature/agur-hobetua`), Pull Requests eta kode-berrikuspenaren garrantzia.
# - **Ariketa 4.4**: `.gitignore`, `.env` fitxategi sentikorren babesa eta `PULL_REQUEST_TEMPLATE.md`.
# """

# %%
import subprocess

git_arrazoiak = [
    ("1. Historia eta Itzulgarritasuna (Time Travel)", "Kodearen lerro bakoitza nork, noiz eta zergatik aldatu zuen erregistratzen du. Akats bat ekoizpenera iristean, berehala itzul daiteke aurreko bertsio egonkorrera."),
    ("2. Talde-lankidetza adarren bidez (Branching)", "Hainbat garatzailek aldi berean egin dezakete lan elkarren kodea gainidatzi gabe, adar isolatuetan garatuz eta gatazkak modu kontrolatuan ebatziz."),
    ("3. Kalitate-kontrola eta CI/CD integrazioa", "Pull Request bidez kode-berrikuspenak (Code Review) eta proba automatizatuak derrigortu daitezke kodea adar nagusira batu aurretik.")
]

print("=== ARIKETA 4.1: GIT ERABILTZEKO 3 ARRAZOI SENDO ===")
for izena, azalpena in git_arrazoiak:
    print(f"\n📌 {izena}")
    print(f"   {azalpena}")

print("\n=== ARIKETA 4.4: SEGURTASUNA ETA .gitignore EGIAZTAPENA ===")
# Egiaztatu .env eta .gitignore fitxategiak existitzen direla
gitignore_path = Path(".gitignore")
env_path = Path(".env.example")
pr_path = Path("PULL_REQUEST_TEMPLATE.md")

print(f".gitignore existitzen da:            {gitignore_path.exists()} ({gitignore_path.stat().st_size} bytes)")
print(f".env.example existitzen da:          {env_path.exists()} ({env_path.stat().st_size} bytes)")
print(f"PULL_REQUEST_TEMPLATE existitzen da: {pr_path.exists()} ({pr_path.stat().st_size} bytes)")
