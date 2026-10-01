# 04_Datu_Zientzia_PDF_Ariketak (5073 Modulua - 2. Gaia)

Karpeta honek `5073_2_Datu_Zientzia.pdf` apunte-dokumentuko ariketa praktiko guztiak biltzen ditu, datu-zientzialari baten 5 zutabe metodologikoak landuz (NumPy, Pandas, Matplotlib/Seaborn, DVC eta Plataforma Komertzialak).

## Edukia eta Fitxategiak
- **`5073_2_Datu_Zientzia_PDF_Ariketak.ipynb`**: Ebazpenak eta aurreko irteerak dituen koadernoa; gordetako emaitzek ez dute egungo bertsioaren exekuzio osoa frogatzen.
- **`5073_2_Datu_Zientzia_PDF_Ariketak.py`**: Koadernoaren baliokide zuzena den Python fitxategi egituratua, `# %%` gelaxka interaktiboekin (VS Code / Spyder).
- **`data/`**: Ariketetan erabilitako datu-multzoak:
  - `urtarrila.csv`, `otsaila.csv`, `martxoa.csv`: Q1eko hileroko salmentak (`pd.concat` ariketarako).
  - `bezeroak_zikinak.csv`: Datu-garbiketa probarako fitxategia (balio galduak, bikoiztuak, espazioak).
  - `notak.csv.dvc`: DVCko punteroa; datu-fitxategia ez dago Git-en. 4.1 ariketak bere lagin txikia sortzen du laborategi isolatuan.
  - [tips.csv](../../data/tips.csv): 244 errenkadako kopia lokala; scriptak ez du dataset hau saretik deskargatzen.
  - `emaitzak_benchmark.csv`: NumPy vs Python zerrendak abiadura-konparaketaren datu errealak.
- **`grafikoak/`**: Sortutako eta esportatutako grafiko guztiak:
  - `grafikoa_3_1.png` (300 DPI) & `grafikoa_3_1.pdf`: 2x2 azpigrafikoak (barrak, sakabanaketa, histograma, kaxa).
  - `grafikoa_3_3.png`, `grafikoa_3_3.pdf`, `grafikoa_3_3.svg`: Gai pertsonalizatua eta bektore-formatuen esportazioa.
- **`.venv/`**: `uv`-rekin sortutako ingurune birtual isolatua (`numpy`, `pandas`, `matplotlib`, `seaborn`, `dvc`).
- **`requirements.txt`**: Proiektuko liburutegien gutxieneko bertsioak (ez lock zehatza).

## Preparación, ejecución y lectura

Desde la raíz del repositorio, con Python 3, Git y `uv` disponibles:

```bash
cd 04_Programazioa_5073/soluzioak/04_Datu_Zientzia_PDF_Ariketak
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python 5073_2_Datu_Zientzia_PDF_Ariketak.py
```

Se crean entorno y paquetes locales; no se distribuye una `.venv` en Git.
En Jupyter usa ese intérprete, esta carpeta y orden de arriba abajo. El script
contiene llamadas junto a las definiciones: importarlo también ejecuta ejercicios;
llamar después a `main()` los repite. Para conservar CSV/gráficos propios,
ejecuta una copia de esta carpeta. El benchmark llega a 50 millones de enteros
(~400 MB solo para el array NumPy); sus tiempos dependen del equipo y excluyen
la creación de ese array. La frase de speedup del programa no es un resultado
universal. `tips` se lee de `../../data/tips.csv`, sin descarga. El script construye
esa ruta con `__file__`; en Jupyter adapta esa variable/ruta al directorio
del kernel o utiliza el `.py`.

| Bloque | Qué debes entender y comprobar |
|---|---|
| 1.1–1.5 | Igualdad de las sumas; formas de arrays, broadcasting y máscaras. `axis=0` agrega filas; `axis=1`, columnas. Las variantes de precios/stock del PDF están en el script auxiliar, no sustituyen este ejemplo. |
| 2.1–2.5 | Filtros, origen de cada CSV, tratamiento de ausencias/duplicados y diferencia entre `concat` (apilar) y `merge` (unir por clave). Revisa filas antes/después y valores excluidos. |
| 3.1–3.3 | Comprueba variables, etiquetas y diferencias entre distribución, relación y comparación de grupos. PNG es raster; PDF/SVG permiten gráficos vectoriales. |
| 4.1 | El ejercicio crea un repositorio Git/DVC y remoto local en un directorio temporal independiente; el puntero referencia datos, no contiene el CSV. No escribe en un remoto cloud. |
| 5.1 | La selección de herramientas es una propuesta razonada según recursos y necesidades, no una medición del mercado. |

El [registro histórico](../egiaztapena_2026-09-28.md) acota lo que se ejecutó.
Las comprobaciones documentales actuales no recalculan los resultados.

## Azterketarako gogortua (`laguntzaileak.py`, menpekotasun berririk gabe)

`laguntzaileak.py` (stdlib + pandas) CSV tranpak jasaten ditu: encoding okerrak,
lerro malformituak, zutabe okerrak/hutsak, fitxategi hutsak, ehunka fitxategi,
koma-dezimalak (`1.234,56 €` → 1234.56; komarik gabe puntua dezimala da).
Kopiatu fitxategi hori + `pilatu_csvak("data/*.csv", ...)` 3 lerro.
```bash
python test_laguntzaileak.py   # 200 fixture zikin: 265 errenkada + 10 txar ✅
```


## Ariketa 2.3 — CSV berria (2026)

`data/bezeroak_zikinak.csv` aurreko adibideak komaz bereizita erabiltzen du. Enuntziatu honetako sarrera berria [datu_zikinak.csv](../../data/mock_datuak/Ariketa%202.3/datu_zikinak.csv) da: puntu eta komaz bereizita dago, eta ez da lehendik dagoen fitxategia ordezten.

- [Python ebazpena](ariketa_2_3_datu_berria.py) eta [koaderno sinkronizatua](ariketa_2_3_datu_berria.ipynb)
- [Garbiketa-emaitza](data/datu_zikinak_garbia.csv)
- [Hasierako balio galduen eta prozesuaren laburpena](data/datu_zikinak_laburpena.json)

Emaitzak berreraikitzeko, exekutatu `python ariketa_2_3_datu_berria.py` direktorio honetatik. Soldata hutsik mantentzen da, eta JSONak izen-bikoiztuak kentzeko eta adina betetzeko aukerak azaltzen ditu.

## PDFko datu-ariketen aldaera osagarriak

PDFko ariketa zehatzen beste berrikuspen bat dago [ariketa_pdf_aldaerak.py](ariketa_pdf_aldaerak.py)
fitxategian eta [koaderno sinkronizatuan](ariketa_pdf_aldaerak.ipynb): seed=42 matrizea,
PDFko prezio/stock balioak, eta Pandas concat. Hura exekutatzeko, erabili
`python ariketa_pdf_aldaerak.py` direktorio honetatik. Z-score adibideko 5x4 datuak eta
`data/pdf_ariketa_2_2_fixtures/`-eko sei salmenta-errenkadak sintetikoak dira; fixture horiek ez dira tutorearen CSV zehatzak, eta ez dituzte lehendik dauden datasetak ordezten.

## Variantes: elige la entrada correcta

- **3.1, datos del curso:** [script](ariketa_3_1_ikasleak.py) y
  [notebook](ariketa_3_1_ikasleak.ipynb) leen
  [ikasleak_notak_100.csv](data/ikasleak_notak_100.csv), con `;` y decimal `,`.
  `python ariketa_3_1_ikasleak.py` genera
  `grafikoak/grafikoa_3_1_ofiziala.png` y `.pdf`. El scatter usa horas y nota;
  su correlación no demuestra que aumentar horas cause cierta mejora de nota.
- **2.3, CSV nuevo:** el script enlazado arriba produce un CSV limpio y JSON
  de decisiones. Compara `rows_before/rows_after` y la política de deduplicación;
  elegir por nombre no es un identificador fiable de personas en datos reales.
- **Variantes del PDF:** `ariketa_pdf_aldaerak.py` explica matriz, IVA/descuento,
  z-score, stock y concat. Usa fixtures de seis filas. También contiene un
  **fallback absoluto** a `/home/tears/bigdata/.../Ariketa 2.2`: en otra máquina
  ese bloque opcional no se ejecuta. Los CSV del curso existen en
  [Ariketa 2.2](<../../data/mock_datuak/Ariketa 2.2/>); su existencia no convierte
  automáticamente los fixtures en esos datos. Adapta la ruta si quieres comparar
  ambas entradas. Esta revisión documenta esa limitación de portabilidad.
