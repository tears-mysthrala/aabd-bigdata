# DF2.2 — MariaDB → MongoDB (bi aldaera)

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

Hau egituraren araberako konparaketa da, ez exekuzio edo benchmark baten emaitza. Ez da saio honetan NiFi, MariaDB edo MongoDB konektatu edo exekutatu; ez dago hemen live-insert, datu-zenbaketa edo abiadura-neurketarik baieztatuta.

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
