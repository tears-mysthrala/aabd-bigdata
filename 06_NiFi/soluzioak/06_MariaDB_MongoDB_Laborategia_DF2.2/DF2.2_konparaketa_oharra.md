# DF2.2 Ariketa: 6. Kasua — MariaDB → MongoDB Konparaketa-Oharra

## 1. Testuingurua eta helburua

DF2.2 ariketak `retail_db`-ko hiru taulak —`customers`, `orders` eta `order_items`— MariaDBtik MongoDBra eramateko bi NiFi aldaera eskatzen ditu. Fluxu bakoitzak hiru `ExecuteSQLRecord` adar ditu. SELECT bakoitzak `source_table` eremua eransten du, taula bereko dokumentuak bereizteko bilduma bateratuan. Ez da taula-laginketarik aplikatzen.

- **Classic:** hiru SQL adarrak `SplitText`-era lotzen dira (`Line Split Count = 1`), eta ondoren `PutMongo`-ra; xedea `iabd.6kasua-classic` bilduma da.
- **Record API:** hiru SQL adarrak `PutMongoRecord`-era lotzen dira, `JsonTreeReader` erabiliz; xedea `iabd.6kasua-record` bilduma da.

Fluxu-definizioak: [Classic JSON](flow_06_mariadb_mongodb_classic.json), [Record API JSON](flow_06_mariadb_mongodb_record.json). Zerbitzuen IDak kanpoko controller-service erreferentziak dira eta inportatutako NiFi inguruneak ebatzi behar ditu.

## 2. Arkitektura eta diseinuaren konparaketa

| Ezaugarria | Classic (`SplitText` + `PutMongo`) | Record API (`PutMongoRecord`) |
| --- | --- | --- |
| Prozesadoreak | 3 `ExecuteSQLRecord` adar, `SplitText` partekatua eta `PutMongo` partekatua | 3 `ExecuteSQLRecord` adar eta `PutMongoRecord` partekatua |
| Erregistroen banaketa | `SplitText`-ek JSON lerro bakoitzeko FlowFile bereizia sortzen du | Record irakurleak erregistroak prozesadoreari record multzo gisa ematen dizkio; ez dago `SplitText`-en urratsik |
| Konplexutasuna | Banaketa- eta ilara-etapa gehigarria konfiguratu eta zaindu behar da | Prozesadore gutxiago, baina Record reader-aren eskema/formatua eta batch konfigurazioa egiaztatu behar dira |
| Errendimendu-itxaropena | Erregistro bakoitzeko FlowFile gehiagok I/O eta ilara-kudeaketa gainkarga sor dezakete | Record multzoak batch portaera erabil dezake; abantaila zehatza konfigurazioaren eta datu-bolumenaren araberakoa da |
| Erabilera-irizpidea | Erregistroak banaka bideratu edo eraldatu behar direnean izan daiteke egokia | Multzoa record gisa zuzenean idaztea nahi denean izan daiteke egokia |

Taulak egituran oinarritutako konparazio kualitatiboa egiten du; ez du abiadura, memoria edo txertaketa-ratioen neurketa adierazten.

## 3. Errendimenduaren eta baliabideen inguruko oharrak

Classic aldaeran `SplitText`-ek SQL irteerako lerro bakoitzerako FlowFile bana sortzen du. Horrek FlowFile kopurua eta ilarako erregistroak handitzen ditu; datu-bolumen handietan biltegi- eta kudeaketa-gainkarga gehigarria izan dezake. Banakako dokumentuen txertatze-ereduak sareko eragiketa gehiago ere sor ditzake, konfigurazioaren arabera.

Record API aldaerak ez du erregistro bakoitzerako FlowFile banaketarik egiten. `PutMongoRecord`-ek batch bidezko idazketa erabil dezake eta horrek eskaera/FlowFile gainkarga murrizteko aukera ematen du. Emaitza batch tamainak, datu-bolumenak, zerbitzuen konfigurazioak, MongoDBren egoerak eta inguruneko baliabideek baldintzatzen dute; ezin da abiadura-ratio jakin bat ondorioztatu egitura hutsetik.

**Egiaztapen-egoera:** ohar hau eta bi JSONak estatikoan berrikusi dira. Lan honetan ez dira NiFi, MariaDB edo MongoDB exekutatu edo konektatu, eta ez dira `find()`/zenbaketa egiaztapenak, insertak edo benchmarkak egin. Dokumentu honen aurreko bertsioan agertzen ziren 2.508 eta 160.600 dokumentuko kopuruak kendu dira, ez baitago hemen haiek berresteko exekuzio-ebidentziarik. Beraz, ez da zuzeneko kargarik edo errendimendu-emaitzarik baieztatzen.

## 4. Ondorioa

Bi diseinuek hiru iturburu-taulak jomuga-bilduma berean gordetzea ahalbidetzen dute, eta `source_table`-ek dokumentuen jatorria mantentzen du. Classic aldaerak FlowFile banaketa esplizitua eskaintzen du, konfigurazio eta ilara-operazio gehigarrien truke. Record API-k zuzeneko record bidea eskaintzen du, reader eta batch konfigurazioa behar bezala egiaztatzearen truke. Aukera ingurunean egindako proba neurgarriek gidatu behar dute; ohar honetako konparaketa kualitatiboa da.
