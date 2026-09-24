# Kafka kontsolako ariketak: topic-ak, mezuak, partizioak eta offset-ak

Iturria: [Apache Kafka 3.7 PDFa](../materialak/01_03_ApacheKafka.pdf), 23–27. orrialdeak (ariketak 1–5). CLI sintaxia `infra/docker-compose.yml`-ko `apache/kafka:3.7.0` irudiaren `/opt/kafka/bin/` bidearekin alderatu da, baina adibideek **isolatutako labeko container eta broker baten ordezko-balioak** erabiltzen dituzte. Azalpen hau **komandoak berrikusiak** egoeran dago; ez dira brokerrean exekutatu. Ez da zerbitzurik abiarazi/gelditu, topic-ik sortu edo aldatu, ezta bolumena ukitu ere.

## Segurtasunez nola erabili

Ikasgelako enuntziatuek `sentsoreak` eta `erosketak` izenak eskatzen dituzte. Repositorio honetako `infra/`-k `iabd-kafka` broker/container partekatua eta `iabd-kafka-data` bolumen iraunkorra ditu. Topic izen prefijatuak ez dira isolamendua: container horri bidalitako komando batek broker eta bolumen partekatua aldatuko lituzke. Horregatik, beheko agindu guztiek erabiltzaileak esleitutako **labeko container isolatuaren eta haren broker helbidearen ordezko-aldagaiak** eskatzen dituzte; ez zuzendu `iabd-kafka`-ra, ezta repo honetako datuak dituen beste container batera ere. Aginduek topic-ak sortu edo aldatuko lituzkete exekutatuz gero; hemen **ez dira exekutatu**.

`KAFKA_CONTAINER`-ek labeko Kafka 3.7.0 container **isolatu** baten izena izan behar du; `KAFKA_BOOTSTRAP`-ek CLI container horren barrutik irits daitekeen broker helbidea adierazi behar du. Aldagaiak komandoak erabili aurretik ezarri. `RUN_ID` aukeratu berria izan behar da ariketa-sorta bakoitzerako, inoiz ez lehendik erabilitako bat. Erabili balio berak bi terminaletan sorta bereko ariketa jarraitzeko; hurrengo exekuzio-sortan sortu beste `RUN_ID` bat. Horrek topic izen eta group ID berriak sortzen ditu. Ordezko-balioak bere horretan utziz gero, adibideak ez dira erabil daitezkeen konexio-aginduak.

```bash
export KAFKA_CONTAINER='LAB_ISOLATUKO_KAFKA_CONTAINERA'
export KAFKA_BOOTSTRAP='brokerra-containerretik-iristeko:9092'
export RUN_ID='RUN_BAKOITZERAKO_BERRIA'
export SENSORS="codex-aabd-${RUN_ID}-sensors"
export PURCHASES="codex-aabd-${RUN_ID}-purchases"
```

Ez abiarazi Compose zerbitzurik gida hau erabiltzeko: ingurune isolatua dagoeneko prest egon behar da. Ez erabili erregistro partekatuetan baimenik gabe. Adibideek ezin dituzte aurreikusi broker horretako topic-zerrenda, leaderrak, mezuen banaketa edo benetako offset-ak.

## 1. ariketa — bi topic sortu eta partizioak deskribatu

Enuntziatuko topic-ak: `sentsoreak` (2 partizio) eta `erosketak` (4 partizio). Topic berriak sortzeko, ariketa broker isolatu batean egin edo goiko aurrizkidun izenak erabili:

```bash
docker exec "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-topics.sh --create --topic "$SENSORS" --partitions 2 --bootstrap-server "$KAFKA_BOOTSTRAP"
docker exec "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-topics.sh --create --topic "$PURCHASES" --partitions 4 --bootstrap-server "$KAFKA_BOOTSTRAP"
docker exec "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server "$KAFKA_BOOTSTRAP"
docker exec "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-topics.sh --describe --topic "$SENSORS" --bootstrap-server "$KAFKA_BOOTSTRAP"
docker exec "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-topics.sh --describe --topic "$PURCHASES" --bootstrap-server "$KAFKA_BOOTSTRAP"
```

`--describe`-ren goiburuko `PartitionCount` balioek 2 eta 4 izan behar dute. Lerro bakoitzeko `Partition:` eremuak IDak ematen ditu:

| Topic-a | Behar den kopurua | Espero diren partition IDak |
|---|---:|---|
| `$SENSORS` | 2 | `0`, `1` |
| `$PURCHASES` | 4 | `0`, `1`, `2`, `3` |

ID multzoa eta kopurua deterministikoak dira; `Leader`, `Replicas` eta `Isr` bezalako gainerako eremuak klusterraren uneko egoeraren araberakoak dira. `--list`-ek beste erabiltzaileek/ariketek sortutako topic-ak ere erakuts ditzake; ez ondorioztatu prefijorik gabeko topic-ak ariketa honetakoak direnik. Kafka 3.7 dokumentazioak `kafka-topics.sh --create`, `--list`, `--describe` erabilera deskribatzen du [topic eragiketen atalean](https://kafka.apache.org/37/operations/basic-kafka-operations/).

## 2. ariketa — sentsore-mezuak eta consumer-a deskonektatuta dagoenean

Producer terminalean, bidali gutxienez ondoko sei lerroak (lerro bakoitza mezu bat da):

```bash
docker exec -it "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-console-producer.sh --topic "$SENSORS" --bootstrap-server "$KAFKA_BOOTSTRAP"
```

Producer-ean idatzi banan-banan:

```text
Eibar;21.4
Ermua;20.8
Eibar;21.7
Markina;19.6
Ermua;21.0
Eibar;22.1
```

Sei mezu horiek argitaratu ondoren, abiarazi consumer-a beste terminal batean. Irakurri, gelditu consumer-a, bidali hiru neurketa gehigarriak producer-ean, eta berrabiarazi consumer-a. `--group` izen berezia emateak proba errepikagarri egiten du: bigarren abioan beste group ID bat aukeratuz, `--from-beginning`-ek talde berri horren lehen offset-etik irakurtzen du. Consumer talde berean berrabiarazten bada, aurretik commit egindako offset-ak jarraituko dira; `--from-beginning` ez da offset zaharrak ezabatzeko agindua.

```bash
# Lehen consumer-a
docker exec -it "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-console-consumer.sh --topic "$SENSORS" --group "codex-aabd-${RUN_ID}-sensor-read-1" --from-beginning --bootstrap-server "$KAFKA_BOOTSTRAP"
```

Consumer-a `Ctrl-C` bidez gelditu, eta producer-ean sartu, adibidez:

```text
Eibar;22.4
Ermua;20.9
Markina;20.1
```

Ondoren, berriro irakurri talde berri batekin:

```bash
docker exec -it "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-console-consumer.sh --topic "$SENSORS" --group "codex-aabd-${RUN_ID}-sensor-read-2" --from-beginning --bootstrap-server "$KAFKA_BOOTSTRAP"
```

**Erantzuna:** consumer-a itxita egon den bitartean argitaratutako hiru neurketak ez dira deskonexioagatik galtzen: retained geratzen diren bitartean topic-ean gordetzen dira. Group desberdin batek eta `--from-beginning` aukerak hiru neurketa horiek eta lehenagoko seiak erakutsi beharko lituzke. Talde bera berrabiaraztean aurretik commit egindako offset-etik jarraitzen da; `--from-beginning`-ek ez ditu offset zaharrak ezabatzen. `--from-beginning`-ek, Kafka 3.7ko [ConsoleConsumer iturburu ofizialak](https://github.com/apache/kafka/blob/3.7.0/core/src/main/scala/kafka/tools/ConsoleConsumer.scala) zehazten duen bezala, aurretik offset ezarria ez dagoenean hasieratik irakurtzeko `earliest` ezartzen du. Mezuak retention politikak ezaba ditzake; ikus [broker `log.retention.*` konfigurazioa](https://kafka.apache.org/37/configuration/broker-configs/). Benetako irteera eta retention konfigurazioa ez dira hemen egiaztatu.

Key-rik gabeko producer honekin mezuen arteko **topic osoko ordena ez dago bermatuta**; ordena partizio bakoitzaren barruan bakarrik bermatzen da. `--from-beginning` erabileraren adibidea dago Kafka 3.7 [quickstart-ean](https://kafka.apache.org/37/getting-started/quickstart/), eta `auto.offset.reset=earliest` ezarpena [consumer konfigurazioan](https://kafka.apache.org/37/configuration/consumer-configs/) dago dokumentatuta.

## 3. ariketa — bost erosketak birritan irakurri

Producer-ean argitaratu iturriak eskatutako bost mezuak:

```bash
docker exec -it "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-console-producer.sh --topic "$PURCHASES" --bootstrap-server "$KAFKA_BOOTSTRAP"
```

```text
E001;ordenagailua;899
E002;monitorea;249
E003;teklatua;59
E004;SSD;89
E005;routerra;119
```

Lehen consumer-a:

```bash
docker exec -it "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-console-consumer.sh --topic "$PURCHASES" --group "codex-aabd-${RUN_ID}-purchases-read-1" --from-beginning --bootstrap-server "$KAFKA_BOOTSTRAP"
```

Itxi consumer-a `Ctrl-C` bidez eta ireki beste bat, group ID berriarekin:

```bash
docker exec -it "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-console-consumer.sh --topic "$PURCHASES" --group "codex-aabd-${RUN_ID}-purchases-read-2" --from-beginning --bootstrap-server "$KAFKA_BOOTSTRAP"
```

**Erantzuna:** bai. Bi group independentek topic bereko retained mezuak irakur ditzakete. Irakurtzeak ez du mezua topic-etik ezabatzen; kontsumo-posizioa/offset-a da consumer group bakoitzaren egoera. Mezuak retention politikak edo topic ezabatzeak ezaba ditzake, ez irakurtze hutsak. Bost erosketak birritan agertzea espero da egoera garbi batean; topic-ak aurreko erregistroak baditu, hasieratik irakurtzean haiek ere agertuko dira. Hori dela eta, gida honek ez du irteera zehatzik fabrikatzen. Oinarriak: Kafka-ren [quickstart](https://kafka.apache.org/37/getting-started/quickstart/) eta [retention konfigurazioa](https://kafka.apache.org/37/configuration/broker-configs/).

## 4. ariketa — mezu, partizio eta offset-a ikusi

Erabili 3. ariketako topic-a. Consumer-en formatter-ak `print.partition` eta `print.offset` propietateak onartzen ditu:

```bash
docker exec -it "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-console-consumer.sh --topic "$PURCHASES" --group "codex-aabd-${RUN_ID}-purchases-offsets" --from-beginning --property print.partition=true --property print.offset=true --bootstrap-server "$KAFKA_BOOTSTRAP"
```

Lehenik sortu duzun topic prefijatu eta bost erosketa horiek soilik badaude, osatu taula irteera errealetik. Utzi `—` hutsik irteera neurtu arte; ezin dira balio horiek agindutik bakarrik ondorioztatu.

| Mezua | Partition | Offset |
|---|---:|---:|
| `E001;ordenagailua;899` | — | — |
| `E002;monitorea;249` | — | — |
| `E003;teklatua;59` | — | — |
| `E004;SSD;89` | — | — |
| `E005;routerra;119` | — | — |

**Galderen erantzunak:**

1. **Partizio guztiek offset-kontagailu bera al dute?** Ez. Offset-ak partizio bakoitzeko dira; partizio bakoitzak bere sekuentzia dauka.
2. **`Offset=0` behin baino gehiagotan ager daiteke?** Bai, partizio desberdinetan: adibidez, P0eko offset 0 eta P2ko offset 0 mezu desberdinak dira.
3. **Offset-a bakarrik nahikoa da mezu bat identifikatzeko?** Ez; topic berean ere offset bera partizio askotan egon daiteke.
4. **Zer datuk identifikatzen dute?** Topic izenak, partition IDak eta offset-ak.

Mezu bakoitza zein partiziotan amaitzen den **broker/producerren baldintzen araberakoa** da, batez ere key-rik gabeko producer-en banaketaren ondorioz. Offset zehatzak ere topic horretan aurretik idatzitako mezuen eta retention/compaction egoeraren araberakoak dira. Horregatik taula txantiloi hutsa da, ez emaitza asmatu bat. `print.partition` eta `print.offset` propietateak Kafka 3.7-ren [ConsoleConsumer iturburu ofizialean](https://github.com/apache/kafka/blob/3.7.0/core/src/main/scala/kafka/tools/ConsoleConsumer.scala) ageri dira; `print.offset` adibidea ere badago [tiered-storage operazioan](https://kafka.apache.org/37/operations/tiered-storage/). Offset-aren eta partizioen eragiketak azaltzen dira [Kafka operazio oinarrizkoen dokumentuan](https://kafka.apache.org/37/operations/basic-kafka-operations/).

## 5. ariketa — bi partiziotik lau handitu eta gutxitzea saiatu

1. eta 2. ariketetako topic prefijatu bera erabili; ez erabili `sentsoreak` izen partekatu/ikasgelakoa hemen. Egiaztatu hasierako egoera, handitu 4ra eta egiaztatu berriro:

```bash
docker exec "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-topics.sh --describe --topic "$SENSORS" --bootstrap-server "$KAFKA_BOOTSTRAP"
docker exec "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-topics.sh --alter --topic "$SENSORS" --partitions 4 --bootstrap-server "$KAFKA_BOOTSTRAP"
docker exec "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-topics.sh --describe --topic "$SENSORS" --bootstrap-server "$KAFKA_BOOTSTRAP"
```

Lehen deskribapenean `PartitionCount: 2` ikustea espero da baldin eta 1. ariketan sortu zen eta beste inork aldatu ez badu; bigarrenean `PartitionCount: 4` eta partition IDak 0–3 espero dira. Partizio gehiago gehitzea egoera-aldaketa da eta key bidezko banaketa-araua alda dezake hurrengo mezuentzat. Kafka-k ez ditu lehendik zeuden erregistroak partizio berrietara birbanatzen.

Ondoren, PDFak eskatutako jaitsiera saiatzeko komandoa hau da:

```bash
docker exec "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-topics.sh --alter --topic "$SENSORS" --partitions 2 --bootstrap-server "$KAFKA_BOOTSTRAP"
```

**Ez exekutatu gida honetako lanaren baitan**: topic egoera ez da aldatu behar. Kafka 3.7 dokumentazioaren arabera, partition kopurua gehitzea onartzen da, baina murriztea ez; beraz, komandoko eskaera baztertua izatea espero da. Ez dago hemen benetako stderr/error transkriptorik, komandoa ez baita exekutatu. Erreferentzia: [Kafka 3.7 — Modifying topics](https://kafka.apache.org/37/operations/basic-kafka-operations/).

## Egiaztapen-erregistroa

| Egiaztapena | Egoera |
|---|---|
| Iturriaren 5 ariketak eta eskatutako mezu-sekuentziak (23–27. orrialdeak) | PDFko testuarekin berrikusia |
| CLI sintaxia eta irudi ofizialaren CLI bidea | Kafka 3.7.0 Compose irudiari buruz irakurrita; ez da container abiarazi edo eskatu |
| Topic komandoak, `--from-beginning`, `--alter` eta partizio-jaitsieraren portaera | Kafka 3.7 dokumentazio ofizialarekin berrikusia |
| Consumer/producer edo brokerrarekin zuzeneko exekuzioa | **Ez da egin**; komandoak berrikusiak bakarrik |
| Partizio/offset taulako benetako balioak | Ez dira asmatu; ariketako exekuzioan bete |
