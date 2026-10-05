# DF2.2 — MariaDB → MongoDB (bi aldaera)

## Ejecución verificada y evidencia

2026-10-02: ambas variantes se ejecutaron contra el SQL original completo,
sin LIMIT ni muestreo. Cada colección Mongo contiene **253.516 documentos**:
12.435 customers, 68.883 orders y 172.198 order_items. Se cotejaron **todas las
filas y todos sus campos** contra SQL, ordenando por la clave original:
cero diferencias. La normalización excluye `_id`, expresa fechas ISO con
segundos y redondea los importes float a dos decimales; el resto se compara
exactamente. Los hashes normalizados coinciden por tabla en ambos destinos.

Defecto corregido: las seis consultas estaban bajo la propiedad `SQL Query`;
NiFi 2.0.0 utiliza `SQL select query`. Aunque el processor aparecía VALID,
fallaba al arrancar sin consulta. El log conserva ese error previo y la
configuración corregida se ejecutó mediante RUN_ONCE. Classic crea 253.516
FlowFiles de registros a partir de tres resultados SQL; Record entrega tres
FlowFiles a PutMongoRecord. El muestreo provenance del sink clásico no es un
registro exhaustivo de sus 253.516 eventos; la verificación completa está en
los conteos y la comparación de contenido.

[Resultado](evidencias/resultado_2026-10-02.json),
[comparación completa](evidencias/comparacion_contenido_completo.json),
[log del diagnóstico](evidencias/nifi_app_extracto.log),
[estado clásico final](evidencias/flow_06_mariadb_mongodb_classic_final_status.json) y
[estado Record final](evidencias/flow_06_mariadb_mongodb_record_final_status.json).

**Motor probado: MySQL 8.4**, que es el definido en el Compose existente.
El título académico pide MariaDB: no se ha probado ese motor. No se ha medido
un benchmark controlado de tiempo, CPU o memoria; la comparación cualitativa
no establece una mejora cuantitativa de velocidad.


Ariketak `retail_db`-ko `customers`, `orders` eta `order_items` taulak prozesatzea eskatzen du, bi NiFi fluxu-definizioetan, eta konplexutasunaren eta errendimenduaren arteko konparaketa. Iturria [Apache NiFi aurreratua PDFa](../../materialak/01_02_ApacheNifi_aurreratua.pdf), DF2.2 atala da.

Konparaketa kualitatiboaren xehetasunak [DF2.2 konparaketa-oharrean](DF2.2_konparaketa_oharra.md) daude.

## Fluxu-definizioak

- [Classic: ExecuteSQLRecord → SplitText (Line Split Count = 1) → PutMongo](flow_06_mariadb_mongodb_classic.json). Hiru SQL adarrak `6kasua-classic` bilduma berera doaz; dokumentu bakoitzak `source_table` eremua darama jatorrizko taula bereizteko.
- [Record API: ExecuteSQLRecord → PutMongoRecord](flow_06_mariadb_mongodb_record.json). Hiru SQL adarrak `6kasua-record` bilduma berera doaz, `JsonTreeReader` erabiliz; dokumentu bakoitzak `source_table` eremua darama.

Adar bakoitzak taula osoa hautatzen du eta ez du lagin-mugarik (`LIMIT`) ezartzen. Fluxuetan DBCP/MongoDB/record controller-service IDak kanpoan erreferentziatzen dira, inportatutako NiFi inguruneak eman ditzan.

## Diseinu-konparaketa

| Gaia | Classic (`SplitText` + `PutMongo`) | Record API (`PutMongoRecord`) |
| --- | --- | --- |
| Fluxuaren egitura | Erregistroak banan-banan FlowFile bihurtzen dira; ilara eta FlowFile kopurua handitzen dira. | Record multzoa Record API bidez pasatzen da; ez du banakako FlowFile bihurketarik behar. |
| Diseinu/operazio konplexutasuna | Split eta downstream konexio gehigarria konfiguratu eta behatu behar dira. | Prozesadore-etapa gutxiago; reader/writer eta batch portaera egiaztatu behar dira. |
| Errendimendu-itxaropena | Erregistro bakoitzeko FlowFile/insert eredua gainkarga handiagokoa izan daiteke, bereziki multzo handietan. | Batch portaerak FlowFile/txertaketa gainkarga txikiagoa eman dezake; benetako emaitza konfigurazioaren, tamainaren eta ingurunearen araberakoa da. |
| Aukeratzeko irizpidea | Erregistro bakoitza banaka prozesatu edo bideratu behar denean erabilgarria izan daiteke. | Erregistro multzoa zuzenean prozesatzea nahi denean egokiagoa izan daiteke. |

La tabla compara la estructura. La ejecución y los conteos se acreditan arriba; no constituye un benchmark controlado. MariaDB sigue sin probarse.

## Preparación del laboratorio y lectura de la comparación

[Compose](docker-compose.yml) y [guía operativa](Ebazpena_Kasu_6.md) describen
red, puertos, SQL inicial y servicios. Lee la configuración local y `.env.example`
antes de arrancar; las credenciales reales se suministran fuera de Git. Las
rutas del contenedor no son las rutas del host. Usa las guías generales de
[infra](../../../infra/README.md) y [NiFi](../README.md) para resolver montajes y
servicios antes de importar los dos JSON parados.

Classic crea un FlowFile por línea y Record conserva conjuntos de registros.
Para comprobar equivalencia compara conteos por `source_table` y una muestra de
campos de `customers`, `orders` y `order_items`. No compares solo el conteo total.
Las consultas leen tablas completas; repetir processors puede insertar de nuevo
los mismos registros: cuenta por ejecución y revisa la estrategia de IDs/modo
antes de concluir que un aumento significa datos nuevos. Una comparación de
velocidad necesita el mismo dato, entorno y límites de lote, con tiempos
medidos; el menor número de processors no basta para certificarla.


## Laboratorio aislado y reproducción

Los comandos siguientes se ejecutan desde la raíz y prueban los casos 1-6 en
una única instancia dedicada. No usan `infra/`, bases de datos personales ni
el canvas de otra instancia. Requieren Docker, Python 3 y las imágenes
`iabd-nifi:2.0.0-local`, `mongo:7.0` y `mysql:8.4`. Si falta la imagen local:

```bash
docker build -t iabd-nifi:2.0.0-local \
  06_NiFi/soluzioak/06_MariaDB_MongoDB_Laborategia_DF2.2
```

```bash
python 06_NiFi/soluzioak/scripts/nifi_lab_stack.py up
python 06_NiFi/soluzioak/scripts/nifi_lab_verificar.py prepare
python 06_NiFi/soluzioak/scripts/nifi_lab_ejecutar.py
python 06_NiFi/soluzioak/scripts/nifi_lab_evidencias.py
python 06_NiFi/soluzioak/scripts/nifi_lab_comparar.py
python 06_NiFi/soluzioak/scripts/nifi_lab_resultados.py
python 06_NiFi/soluzioak/scripts/nifi_lab_validar_evidencias.py
python 06_NiFi/soluzioak/scripts/nifi_lab_stack.py down
```

[Preparador](../scripts/nifi_lab_stack.py): Compose sanitizado embebido,
proyecto `bigdata-nifi-lab-20261002`, red dedicada y endpoint
`https://localhost:18443` publicado solo en loopback. Genera credenciales
aleatorias en `/tmp/bigdata-nifi-lab-20261002/credentials.json` y `.env`, con
modo 600 dentro de un directorio 700; exporta el certificado de NiFi y verifica
TLS y el hostname `localhost`. Ningún secreto entra en Git. No muestra tokens.
MySQL/MongoDB no publican puertos. No se sobreescribe un laboratorio existente.

[Importador](../scripts/nifi_lab_verificar.py) crea un PG propio y remapea
servicios/rutas solo dentro del laboratorio. [Ejecutor](../scripts/nifi_lab_ejecutar.py)
ejecuta SQL y GenerateFlowFile mediante `RUN_ONCE`; GetFile sondea entradas
con `Keep Source File=false` y se detiene al cerrar la prueba. Espera como
máximo diez minutos para
la carga SQL completa (puede necesitar ajuste en otra máquina), evita duplicar la carga SQL si las
colecciones ya tienen documentos y detiene su PG al terminar. Es una prueba
local: modifica solo directorios temporales, grupos y bases de datos del lab.
[Exportador](../scripts/nifi_lab_evidencias.py) guarda estados y provenance
acotado a 100 eventos por procesador; las listas largas de linaje conservan
20 UUID y el conteo total. Liberar resultados de consulta no borra eventos.
[Comparador](../scripts/nifi_lab_comparar.py) coteja todas las filas SQL/Mongo.
[Verificador de resultados](../scripts/nifi_lab_resultados.py) compara y archiva
los archivos reales y los documentos de muestra, sin guardar las filas de clientes.

La receta reúne los pasos ejecutados en esta sesión; no se ha repetido un
segundo arranque completo desde cero con el script conjunto. `down` retira
solo los contenedores y volúmenes del proyecto dedicado y conserva los
archivos temporales del host. Si se comparte con el caso 7, detener primero
su sidecar MinIO y coordinar el cierre. La evidencia versionada permite
[validación sin Docker](../scripts/nifi_lab_validar_evidencias.py).

**Límites:** ejecución real de NiFi por REST, contenido, logs y provenance;
no hay captura GUI. T3 abrió el HTTPS del lab pero no pudo cargar su
certificado en el navegador. La validación REST sí usa certificado verificado.
No se han accedido APIs con claves reales ni AWS.
