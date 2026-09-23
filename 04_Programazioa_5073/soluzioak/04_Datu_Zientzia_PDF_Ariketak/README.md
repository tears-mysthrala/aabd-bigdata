# 04_Datu_Zientzia_PDF_Ariketak (5073 Modulua - 2. Gaia)

Karpeta honek `5073_2_Datu_Zientzia.pdf` apunte-dokumentuko ariketa praktiko guztiak biltzen ditu, datu-zientzialari baten 5 zutabe metodologikoak landuz (NumPy, Pandas, Matplotlib/Seaborn, DVC eta Plataforma Komertzialak).

## Edukia eta Fitxategiak
- **`5073_2_Datu_Zientzia_PDF_Ariketak.ipynb`**: Ariketa guztien ebazpena biltzen duen Jupyter koadernoa, taula, estatistika eta grafiko guztiak gelaxketan bertan exekutatuta eta gordeta.
- **`5073_2_Datu_Zientzia_PDF_Ariketak.py`**: Koadernoaren baliokide zuzena den Python fitxategi egituratua, `# %%` gelaxka interaktiboekin (VS Code / Spyder).
- **`data/`**: Ariketetan erabilitako datu-multzoak:
  - `urtarrila.csv`, `otsaila.csv`, `martxoa.csv`: Q1eko hileroko salmentak (`pd.concat` ariketarako).
  - `bezeroak_zikinak.csv`: Datu-garbiketa probarako fitxategia (balio galduak, bikoiztuak, espazioak).
  - `notak.csv`: Ikasleen notak DVC bertsio-kontrolerako.
  - `tips.csv`: Jatetxeko propina eta fakturen datu-multzoa.
  - `emaitzak_benchmark.csv`: NumPy vs Python zerrendak abiadura-konparaketaren datu errealak.
- **`grafikoak/`**: Sortutako eta esportatutako grafiko guztiak:
  - `grafikoa_3_1.png` (300 DPI) & `grafikoa_3_1.pdf`: 2x2 azpigrafikoak (barrak, sakabanaketa, histograma, kaxa).
  - `grafikoa_3_3.png`, `grafikoa_3_3.pdf`, `grafikoa_3_3.svg`: Gai pertsonalizatua eta bektore-formatuen esportazioa.
- **`.venv/`**: `uv`-rekin sortutako ingurune birtual isolatua (`numpy`, `pandas`, `matplotlib`, `seaborn`, `dvc`).
- **`requirements.txt`**: Proiektuko liburutegien bertsioak.

## Nola Exekutatu
```bash
# Ingurune birtuala aktibatu
source .venv/bin/activate

# Jupyter bidez ireki
jupyter lab 5073_2_Datu_Zientzia_PDF_Ariketak.ipynb

# Edo Python fitxategi interaktiboa exekutatu
python 5073_2_Datu_Zientzia_PDF_Ariketak.py
```

## Azterketarako gogortua (`laguntzaileak.py`, menpekotasun berririk gabe)

`laguntzaileak.py` (stdlib + pandas) CSV tranpak jasaten ditu: encoding okerrak,
lerro malformituak, zutabe okerrak/hutsak, fitxategi hutsak, ehunka fitxategi,
koma-dezimalak (`1.234,56 €` → 1234.56; komarik gabe puntua dezimala da).
Kopiatu fitxategi hori + `pilatu_csvak("data/*.csv", ...)` 3 lerro.
```bash
python test_laguntzaileak.py   # 200 fixture zikin: 265 errenkada + 10 txar ✅
```
