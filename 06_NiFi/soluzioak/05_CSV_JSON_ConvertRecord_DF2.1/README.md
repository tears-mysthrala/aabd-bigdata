# DF2.1 · CSV → JSON ConvertRecord prozesu-taldean

Iturri kanonikoa [01_02 Apache NiFi Aurreratua](../../materialak/01_02_ApacheNifi_aurreratua.pdf), DF2.1 atala da. Eskaerak lau prozesadore, `sarrera`/`irteera` muga-portuak, `CSVReader` eta `JsonRecordSetWriter` Controller Service-ak, eta JSON irteeraren egiaztapena zehazten ditu.

- [DF2.1 flow definizio estatikoa](flow_05_csv_json_df2.1.json)
- [CSV lagina](sarrera/datuak.csv)

## Topologia

```mermaid
flowchart LR
  I[sarrera · Input Port] --> C[ConvertRecord]
  G[GetFile · tokiko CSV] --> C
  C --> U[UpdateAttribute · .csv → .json]
  U --> P[PutFile · irteera-karpeta]
  P --> O[irteera · Output Port]
```

Prozesu-taldeak `5kasua_iabd` izena mantentzen du. Tokiko bide nagusia `GetFile → ConvertRecord → UpdateAttribute → PutFile` da; Input Port-ak CSV FlowFile-a zuzenean `ConvertRecord`-era bidaltzeko sarrera alternatiboa eskaintzen du. NiFi-ren `GetFile` iturri-prozesadoreak ez du sarrerako FlowFile-harremanik, beraz Input Port-a GetFile-ren aurretik kateatzea ez litzateke baliozko konexioa. Bi sarrerek bihurketa eta ondorengo izen-aldaketa partekatzen dituzte. `PutFile`-ren `success` FlowFile-a `irteera` Output Port-era ere bideratzen da.

`ConvertRecord`-ek txertatutako `CSVReader` (`;` bereizlea) eta `JsonRecordSetWriter` (JSON array) erabiltzen ditu. `UpdateAttribute`-ek `filename` atributuko `.csv` luzapena `.json`-era aldatzen du; `PutFile`-ek JSON edukia tokiko irteera-direktorioan idazteko konfiguratuta dago. Direktorio absolutuak laborategiko NiFi edukiontzi-bideak dira, ez ordenagailu honetako bide-egiaztapenak.

## Egiaztapen-egoera

JSONa lokalean parsatu da eta lau prozesadoreak, bi Controller Service-en ID erreferentziak, bi muga-portuen izenak eta konexio-muturrak estatistikoki balioztatu dira. **Ez da NiFi abiarazi, flow-a inportatu edo exekutatu, CSVtik JSON fitxategirik sortu, ezta irteera-fitxategi zerrendarik egiaztatu ere.** JSON definizio estatikoa da; PDFko exekuzio-proba eta irteera-ebidentzia ez dira faltsuki baieztatzen.

## Cómo verificar la conversión

1. Importa el flow parado en el laboratorio de [caso 6](../06_MariaDB_MongoDB_Laborategia_DF2.2/README.md)
   y comprueba los paths de GetFile/PutFile en el contenedor.
2. Habilita CSVReader y JsonRecordSetWriter y verifica el separador `;` y cabecera.
3. Introduce la muestra por **una** de las dos entradas, para no duplicar el dato.
4. Compara CSV y JSON: misma cantidad de registros y mismos campos/valores según
   el esquema del Reader. El escritor produce un array, no JSONL.
5. Comprueba el archivo y la salida del puerto: cambiar `.csv` por `.json` solo
   cambia un atributo; es ConvertRecord quien transforma el contenido.

Si ves `invalid`, revisa servicios y propiedades; si el contenido no se parsea,
comprueba delimitador y esquema. No se ha realizado aquí esta prueba runtime.
