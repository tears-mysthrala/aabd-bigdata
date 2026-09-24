# DF2.2 — MariaDB → MongoDB (bi aldaera)

Ariketak `retail_db`-ko `customers`, `orders` eta `order_items` taulak prozesatzea eskatzen du, bi NiFi fluxu-definizioetan, eta konplexutasunaren eta errendimenduaren arteko konparaketa. Iturria [Apache NiFi aurreratua PDFa](../../materialak/01_02_ApacheNifi_aurreratua.pdf), DF2.2 atala da.

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

Hau egituraren araberako konparaketa da, ez exekuzio edo benchmark baten emaitza. Ez da saio honetan MariaDB/MongoDB konektatu, fluxurik exekutatu edo daturik zenbatu; beraz, ez dago hemen live-insert edo abiadura-neurketarik baieztatuta. Biltegiko aurreko konparaketa-oharrean ageri diren neurketa enpirikoak ez dira lan honetan egiaztatu.
