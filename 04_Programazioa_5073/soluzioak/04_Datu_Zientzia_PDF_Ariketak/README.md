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

## Ampliación docente 2.4 / 2.5 — ejecutada el 05/10/2026

El bloque extra del [notebook docente](../../materialak/2_SOLUZIOAK_URLa.ipynb)
(celdas 93–97, índices desde cero) amplía estas dos actividades. La solución
actual está en [ariketa_2_4_2_5_docente.py](ariketa_2_4_2_5_docente.py) y su
[notebook ejecutado](ariketa_2_4_2_5_docente.ipynb). Las funciones existentes
`ariketa_2_4()` y `ariketa_2_5()` del script/notebook principal llaman a esta
misma implementación.

**2.4, objetivo:** sumar ventas por ciudad, calcular `mean/max/count` por
categoría, construir un pivot de sumas y elegir la combinación ciudad/categoría
con mayor suma. Lee las **30 filas** de
[salmentak.csv](../../data/mock_datuak/Ariketa2.4/salmentak.csv).
El pivot incluye `GUZTIRA` para comprobar los totales; estos márgenes no
compiten como ciudades/categorías en la selección del máximo.

| Comprobación | Resultado |
|---|---:|
| Ventas Gasteiz / Bilbo / Donostia | 3.132 € / 2.820 € / 1.921 € |
| Total de las 30 ventas | 7.873 € |
| Máximo agregado ciudad/categoría | **Gasteiz / Janaria: 1.417 €** |
| Máxima fila individual | Donostia / Arropa: 456 € |

El máximo individual responde otra pregunta. La selección anterior con
`idxmax()` sobre las filas originales estaba equivocada para este enunciado.
Ahora se busca sobre las sumas del pivot. Si hay empate, `idxmax()` devuelve
la primera combinación en el orden del pivot; el enunciado pide una combinación.

**2.5, objetivo y origen:** añadir ciudades a los clientes mediante `merge`
inner/left y apilar dos meses con `concat`. Los CSV recibidos
[bezeroak.csv](../../data/mock_datuak/Ariketa2.5/bezeroak.csv) y
[hiriak.csv](../../data/mock_datuak/Ariketa2.5/hiriak.csv) tienen el mismo
SHA-256 que el CSV de ventas: 30 filas con
`hiria,kategoria,produktua,salmenta`. **No son tablas válidas de clientes/ciudades.**
Se conservan intactos y se documenta el esquema incompatible en el JSON.
La solución usa las tablas exactas **embebidas en la celda 97 docente**:
Ane, Mikel, Leire, Jon y Amaia; cuatro ciudades, incluida Iruñea. Amaia tiene
`hiri_id` nulo. No se presentan estas tablas como si procedieran de los CSV.

- `inner`: cuatro clientes y seis columnas; Amaia queda fuera porque no tiene
  coincidencia en ciudades.
- `left`: cinco clientes y seis columnas; Amaia permanece con ciudad/provincia
  ausentes. La ciudad Iruñea no tiene cliente y no añade una fila a estos JOIN.
- `concat`: seis ventas, con columna `hila` para preservar el mes. Enero suma
  295 €, febrero 410 € y el conjunto **705 €**. Apilar no añade ciudad a cada cliente.

Las tablas anteriores se conservan para comparar variantes:
`ariketa_2_4(SALMENTA_TAULA)` usa el ejemplo de ocho ventas;
`ariketa_2_5(BEZEROAK, HIRIAK)` usa Kepa con clave 99 sin correspondencia.
Estas variantes no sustituyen los datos docentes actuales.

### Repetir y comprobar

Desde esta carpeta, con la `.venv` indicada en preparación. Para un entorno
nuevo dedicado a esta ampliación, instala
[requirements-docente-notebook.txt](requirements-docente-notebook.txt) en un
venv Python 3.13 con `uv pip install --python .venv/bin/python -r
requirements-docente-notebook.txt`; estos pins principales no son un lock
transitivo:

```bash
.venv/bin/python ariketa_2_4_2_5_docente.py
.venv/bin/python test_agregazio_docente.py
```

El primer comando escribe en [data/docente_2_4_2_5/](data/docente_2_4_2_5/):
pivot con totales, resumen por categorías, resultados inner/left/concat y
[emaitzak.json](data/docente_2_4_2_5/emaitzak.json), con hashes, esquemas y
máximos. Funciona desde cualquier carpeta usando `__file__`. Para el notebook
nuevo, usa esta carpeta como directorio del kernel y ejecuta todo en orden.
No hace falta ejecutar el benchmark ni el laboratorio DVC para estas actividades.

El 05/10/2026 se ejecutaron el script, **todas las celdas del notebook nuevo**
y **solo las celdas 20/22 modificadas del notebook principal**, con sus salidas
actualizadas. No se afirma una nueva ejecución completa de todos los demás
bloques del principal. Se verificaron tres regresiones: un grupo de dos ventas
60+60 supera a otra fila de 100; el máximo docente agregado difiere del
individual; y Amaia/concat mantienen las filas esperadas y detectan el esquema
CSV incompatible. La primera prueba fallaba antes de la corrección y ahora pasa.

Entorno observado: Python 3.13, NumPy 2.5.3, pandas 3.0.6, scikit-learn 1.9.1,
nbclient 0.11.0 e ipykernel 7.3.0. Esta evidencia es local; no corrige la
incidencia de descarga docente, ni acredita publicación o entrega en Moodle.
