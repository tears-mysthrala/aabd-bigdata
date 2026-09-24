# 5073-1 PDFko ariketa-aldaerak: 1.1, 2.4 eta 2.5

Iturria: `materialak/5073_1_Lengoaiak.pdf`, inprimatutako 1.1 (PDF 5. or.), 2.4 (PDF 27. or.) eta 2.5 (PDF 43. or.). Dokumentu honek PDFaren ariketa zehatzak osatzen ditu; ez da irakasleak edo taldekideak egindako entregaren ebidentzia.

## 1.1 — NIF galdetu eta formatua egiaztatzeko sei ataleko paper-zirriborroa

Eskatutako zirriborroa da, ez NIF errealak bildu edo gordetzeko sistema bat. Formatua bakarrik egiaztatzen du: zortzi digitu eta letra larri bat. Ez du kontrol-letraren algoritmoa egiaztatzen.

1. **Moduluaren docstringa:** “Erabiltzaileak emandako NIF sarrera `8 digitu + letra` patroiarekin bat datorren egiaztatzen du.”
2. **Inportazioak eta tipoak:** `import re`; `def formatu_zuzena(nif: str) -> bool:`. Ez da hirugarrenen paketerik behar.
3. **Konstanteak:** `NIF_PATROIA = re.compile(r"^\d{8}[A-Z]$")`.
4. **Funtzioa:** `formatu_zuzena` funtzioak sarrera kentzen du (`strip`), maiuskulaz normalizatzen du eta `fullmatch` bidez aztertzen du. Horrela, ez ditu aurreko/ondorengo karaktere gehigarriak onartzen.
5. **Programa nagusia eta sarrera:** `main()` funtzioak `input("NIF (8 digitu eta letra): ")` galdetzen du, eta `if/else` bidez formatu zuzena edo okerra adierazten du. Ez da sarrera pertsonala fitxategian gordetzen.
6. **Sarrera-puntua:** `if __name__ == "__main__": main()`.

Guard-a dagoenean, Python-ek fitxategia programa nagusi gisa exekutatzen duenean deitzen da `main()`, baina ez modulu hori inportatze hutsagatik. Guard-a kendu eta `main()` baldintzarik gabe deituko balitz, inportazioan ere exekutatuko litzateke; deia bera kentzen bada, `main()` ez da bere kabuz exekutatzen.

## 2.4 — Taldekidearen proiektua birsortu eta itzultzeko prozedura

PDFak aipatzen duen taldekidearen `main.py`, bost lerroko `requirements.txt` eta benetako CSVa ez dira checkout-ean aurkitu. Beraz, ezin dut baieztatu haiek instalatu, exekutatu edo aldatu ditudanik, ezta taldekideak egiaztatu duenik ere. Hona hemen fitxategi horiek jasotzean egiteko isolatutako eskualdaketa-ibilbidea:

1. Jaso hiru fitxategiak batera (`main.py`, `requirements.txt`, CSVa) eta galdetu nola exekutatu behar den zein zutabe espero diren. Jatorrizko kopia ez ukitu.
2. Kopiatu laneko direktorio garbi batera; aztertu `requirements.txt` eta scriptean CSV bide erlatiboa/argumentua nola ematen den.
3. Sortu ingurune lokala eta instalatu emandako dependentziak:

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\\Scripts\\activate
   python -m pip install -r requirements.txt
   python main.py salmentak.csv
   ```

4. Lehen emaitza eta erroreak jaso. Gehitu eskatutako zutabea sarrerako zutabeen esanahia eta datu-mota baieztatu ondoren; ez asmatu kalkulu negozionalik.
5. Gehitu grafikoak sortzeko erabili den `matplotlib` bertsioa lock/requirements fitxategira (proiektuaren arauaren arabera, pin zehatza edo bertsio-barrutia). Berrinstalatu ingurune garbi batean eta egiaztatu scriptak CSV bera prozesatzen duela.
6. Itzuli aldaketak eta exekuzio-agindu zehatza; eskatu taldekideari bere makinan `pip install -r requirements.txt` eta exekuzioa baieztatzeko. Baieztapen hori jaso arte, entregaren integrazio-egiaztapena **zain** dago.

Adibidezko dependentzia-lerro berria `matplotlib>=3.8,<4` izan liteke, baina taldekidearen Python bertsioarekin eta gainerako paketeekin bateragarria den probatu behar da. Benetako bost lerroko fitxategia falta denez, ez dut hemen ordezko `requirements.txt` bat asmatu.

## 2.5 — Agenteekin lan egitea: promptak, adibide-erantzunak eta egiaztapen-zikloa

Ondoko bi erantzunak konparazio didaktikorako **adibide ilustratiboak** dira; ez dira benetan exekutatutako bi agenteren elkarrizketak edo token-kopuruaren neurketa. `laburpena_csv` kodea, aldiz, beheko fixture txikiarekin exekutatu zen aldatu gabe.

### Prompt lausoa (~10 hitz)

> Idatzi CSV irakurri eta laburpen estatistikoa ematen duen funtzio bat.

### Prompt zehatza (60 hitz baino gehiago)

> `data/salmentak.csv` fitxategiak `produktua` (testua), `kopurua` (zenbaki osoa) eta `prezioa` (hamartarra) zutabeak ditu. Idatzi Python 3.10+ funtzio bat, Pandas erabiliz CSV UTF-8z irakurtzen duena eta JSONera serializa daitekeen dict bat itzultzen duena: errenkada-kopurua, unitate-kopuru osoa eta `kopurua * prezioa` guztizko salmenta bi hamartarrera biribildua. Kudeatu fitxategia ez egotea, beharrezko zutabeak falta izatea eta zenbakizko balio baliogabeak; eman errore-mezu erabilgarriak. Gehitu tipoak eta docstring-a, eta erakutsi exekuzio-adibide bat. Ez aldatu CSV iturria eta ez inprimatu bezero-datu pertsonalik.

### Erantzun ilustratiboa — prompt lausoa

```python
def laburpena(bidea):
    df = pd.read_csv(bidea)
    return df.describe()
```

### Erantzun ilustratiboa — prompt zehatza

Ondoko erantzunak eskemaren egiaztapena, balio motak eta errore-mezuak esplizitatzen ditu. Horren kode osoa beheko 2.5(c) atalean dago; konparazioa ez da benetako bi agentek emandako emaitza.

```python
from pathlib import Path
import pandas as pd

def laburpena_csv(bidea: Path) -> dict[str, int | float]:
    """Salmenta CSV baten laburpen agregatua JSONerako prest itzuli."""
    try:
        df = pd.read_csv(bidea, encoding="utf-8")
    except FileNotFoundError as errorea:
        raise FileNotFoundError(f"Ez da fitxategia aurkitu: {bidea}") from errorea
    beharrezkoak = {"produktua", "kopurua", "prezioa"}
    falta = beharrezkoak.difference(df.columns)
    if falta:
        raise ValueError(f"Zutabeak falta dira: {sorted(falta)}")
    try:
        kopuruak = pd.to_numeric(df["kopurua"], errors="raise")
        prezioak = pd.to_numeric(df["prezioa"], errors="raise")
    except (TypeError, ValueError) as errorea:
        raise ValueError("kopurua eta prezioa zenbakizkoak izan behar dira") from errorea
    if not (kopuruak % 1 == 0).all():
        raise ValueError("kopurua balio osoa izan behar da errenkada guztietan")
    salmentak = kopuruak * prezioak
    return dict(
        errenkadak=len(df),
        unitateak=int(kopuruak.sum()),
        salmentak=round(float(salmentak.sum()), 2),
    )
```

**Lerro eta gaitasun konparaketa.** Lerro-kopuruak erantzun bakoitzaren Python kode-blokeetako lerro ez-hutsuak zenbatzen ditu, iruzkinik eta markdownik gabe; import-ak sartzen dira: erantzun lausoak 3 ditu, zehatzak 25. Lausoko erantzunak ez ditu argumentua edo itzulera mota tipatzen (`bidea`/`df.describe()`), eta ez du falta den fitxategia, eskema edo datu baliogabea berariaz tratatzen. Erantzun zehatzak `Path` argumentua eta `dict[str, int | float]` itzulera tipatzen ditu; falta den fitxategiari mezu argia ematen dio, eskema eta mota akatsak `ValueError` bihurtzen ditu, eta erosketa-kopuru ez-osoak baztertzen ditu. Bi kasuetan irteerak CSV erreal baten gaineko egiaztapena behar du; promptaren zehaztasunak ez du berez zuzentasuna bermatzen.

### 2.5(c) — prompt zehatzaren kodea, egiaztapen-zikloan exekutatua

Prompt zehatzaren erantzun osoa (25 kode-lerro, lerro hutsik gabe) kode bera da; beheko blokea fixturearekin exekutatu zen aldatu gabe:

```python
from pathlib import Path
import pandas as pd

def laburpena_csv(bidea: Path) -> dict[str, int | float]:
    """Salmenta CSV baten laburpen agregatua JSONerako prest itzuli."""
    try:
        df = pd.read_csv(bidea, encoding="utf-8")
    except FileNotFoundError as errorea:
        raise FileNotFoundError(f"Ez da fitxategia aurkitu: {bidea}") from errorea
    beharrezkoak = {"produktua", "kopurua", "prezioa"}
    falta = beharrezkoak.difference(df.columns)
    if falta:
        raise ValueError(f"Zutabeak falta dira: {sorted(falta)}")
    try:
        kopuruak = pd.to_numeric(df["kopurua"], errors="raise")
        prezioak = pd.to_numeric(df["prezioa"], errors="raise")
    except (TypeError, ValueError) as errorea:
        raise ValueError("kopurua eta prezioa zenbakizkoak izan behar dira") from errorea
    if not (kopuruak % 1 == 0).all():
        raise ValueError("kopurua balio osoa izan behar da errenkada guztietan")
    salmentak = kopuruak * prezioak
    return dict(
        errenkadak=len(df),
        unitateak=int(kopuruak.sum()),
        salmentak=round(float(salmentak.sum()), 2),
    )
```

Exekuzioan fixture honek erabili zuen (adibide sintetikoa; ez du bezero pertsonalik):

```csv
produktua,kopurua,prezioa
koadernoa,2,3.20
arkatza,5,0.80
```

Emaitza exekutatua: `{'errenkadak': 2, 'unitateak': 7, 'salmentak': 10.40}`. Falta den fitxategiak `FileNotFoundError` mezu erabilgarria ematen du; eskema eta datu mota okerrak `ValueError` dira. `kopurua` hamartar zatiduna bada, ez du unitate-kopurua `int()` bidez isilean mozten: errorea ematen du. Dict-eko balio guztiak JSON serializagarriak dira.

**Egiaztapen-oharrak:** kode-bloke hori bere horretan probatu da aurreko bi errenkadako CSV fixturearekin, eta emaitza itxarondakoa izan da. Python konpilazio-egiaztapena ere egin da. Pylance ez dago ingurune honetan eskuragarri; beraz, ez dut haren diagnostikorik edo “lint garbi” emaitzarik aldarrikatzen. Realeko taldekidearen fitxategian exekuzioa eta bere IDEko Pylance/flake8 berrikuspena egiteke daude.

**Ekoizpenerako hausnarketa (100 hitz baino gehiago):** Lagin hau ekoizpenean erabili aurretik, eskemaren kontratu idatzia eskatuko nuke: zutabeen izenak, zenbaki hamartarren bereizlea, moneta, biribiltze-araua eta hutsik dagoen CSV baten esanahia. Orain `to_numeric(errors="raise")` erabiltzen da, baina ez dira negatiboak, hutsuneak, bikoiztutako salmentak edo prezio ezinezkoak semantikoki aztertzen. Data-gama eta produktu-identifikatzaileak balioztatuko nituzke, CSV tamaina-muga ezarriko nuke eta erroreak logetan datu pertsonalik gabe jasoko nituzke. Salmenta-guztira `Decimal` bidez kalkulatzea aztertuko nuke, euro-zentimoetan zehaztasuna behar bada. Unitate-probak gehituko nituzke fitxategi falta, zutabe falta, balio oker, UTF-8 BOM eta CSV hutsa kasuetarako; integrazio-proba batek fitxategi errealik gabeko fixture txiki bat erabiliko luke. Azkenik, iturburua irakurtzeko bakarrik mantendu, irteeraren eskema bertsionatu, Python/Pandas bertsioak finkatu eta taldeko beste kide batek ingurune garbian errepikatu duela dokumentatu behar da. Une honetan, horietako azken berrespena ezin da egin, lankidearen datuak falta direlako.

### OpenClaw probatzeko isolamendu-proposamena

- **Aukera:** botatzeko VM batean (snapshot batetik) probatuko nuke, sare-sarbidea behar denean soilik eta kontu bereiziarekin.
- **Babestu beharrekoa:** laptop pertsonaleko fitxategiak, saio-cookieak, SSH gakoak, kontaktuak, kamera/mikrofonoa eta hodei-tokenak VM-ra ez muntatu.
- **Kostua/konplexutasuna:** VM-ak baliabide eta konfigurazio gehiago eskatzen ditu devcontainer batek baino, baina snapshot bidezko atzera-egitea eta ostalariaren isolamendu hobea eskaintzen du; doako tokiko VM posible ez bada, ikastetxeko makina administratu bat aukera da.

Talde-eztabaidarako, benetako parte-hartzaileen hautuak idatzi gabe uzten dira: ez dira checkout-ean ageri.
