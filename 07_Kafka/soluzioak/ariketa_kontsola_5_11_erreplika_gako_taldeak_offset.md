# Kafka kontsolako ariketak 5–11: erreplika-faktorea, gakoak, consumer group-ak eta offset-ak

Iturria: [Apache Kafka PDFa](../materialak/01_03_ApacheKafka.pdf), 34., 39. eta 50–54. orrialdeak
(5–11 ariketak). 1–5 ariketak
[hemen](../soluzioak/ariketa_kontsola_topic_partizio_offset.md) daude;
fitxategi honek serie berria estaltzen du. Aginduak **broker isolatu
baterako txantiloiak** dira; 2026-09-28an beste container efimero batean
benetan egindako exekuzioaren emaitzak
[hemen](kafka_exekuzio_isolatua_2026-09-28_5_11.md) daude. Repoaren broker
partekatua (`infra/`ko `iabd-kafka`) ez da ukitu.

## Segurtasunez nola erabili

Beheko agindu guztiek labeko Kafka 3.7.0 container **isolatu** baten izena
(`KAFKA_CONTAINER`) eta haren broker helbidea (`KAFKA_BOOTSTRAP`) eskatzen
dituzte; ez zuzendu `iabd-kafka`-ra. `RUN_ID` berria izan behar da
arriketa-sorta bakoitzerako.

```bash
export KAFKA_CONTAINER='LAB_ISOLATUKO_KAFKA_CONTAINERA'
export KAFKA_BOOTSTRAP='brokerra-containerretik-iristeko:9092'
export RUN_ID='RUN_BAKOITZERAKO_BERRIA'
export KEYS="codex-aabd-${RUN_ID}-erosketak-key"
export ORDERS="codex-aabd-${RUN_ID}-eskaerak"
```

## 5. ariketa — erreplika-faktorea broker bakarrean

```bash
docker exec "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-topics.sh --create --topic "codex-aabd-${RUN_ID}-erreplikak" --partitions 2 --replication-factor 2 --bootstrap-server "$KAFKA_BOOTSTRAP"
```

**Erantzuna:** broker bakarrarekin komandoak huts egiten du:
`InvalidReplicationFactorException: Unable to replicate the partition 2
time(s): The target replication factor of 2 cannot be reached because only
1 broker(s) are registered.` Erreplika bakoitzak broker DESBERDIN batean
egon behar du; broker bakarra badago, faktore zuzena `--replication-factor
1` da. Exekuzio-erregistroa: [5. atala](kafka_exekuzio_isolatua_2026-09-28_5_11.md#5-erreplika-faktorea).

## 6. ariketa — mezuak KEY batekin bidali

```bash
docker exec "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-topics.sh --create --topic "$KEYS" --partitions 3 --bootstrap-server "$KAFKA_BOOTSTRAP"
docker exec -it "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-console-producer.sh --topic "$KEYS" --bootstrap-server "$KAFKA_BOOTSTRAP" --property parse.key=true --property key.separator=:
```

Producer-ean idatzi (`gakoa:balioa`):

```text
Bezero1:Erosketa egin tu
Bezero2:Saioa hasi du
Bezero1:ordainketa egin du
Bezero3:produktua ikusi du
Bezero2:erosketa egin du
```

Consumer-a key-a eta partizioa erakusteko:

```bash
docker exec -it "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-console-consumer.sh --topic "$KEYS" --group "codex-aabd-${RUN_ID}-key-read" --from-beginning --property print.key=true --property print.partition=true --bootstrap-server "$KAFKA_BOOTSTRAP"
```

**Erantzuna:** gako bera → partizio bera (entitate-mailako ordena). Behatutako
banaketa: `Bezero1` (bi mezuak P0), `Bezero2` (bi mezuak P0), `Bezero3` (P1).
Transkripzioa: [6. atala](kafka_exekuzio_isolatua_2026-09-28_5_11.md#6-gakoak).

## 7. ariketa — consumer group bat sortu

```bash
docker exec "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-topics.sh --create --topic "$ORDERS" --partitions 3 --bootstrap-server "$KAFKA_BOOTSTRAP"
# Bi terminaletan, TALDE BEREAN, mezuak bidali AURRETIK abiarazi:
docker exec -it "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-console-consumer.sh --topic "$ORDERS" --group "codex-aabd-${RUN_ID}-denda" --property print.partition=true --bootstrap-server "$KAFKA_BOOTSTRAP"
```

**Erantzuna:** ez, bi consumer-ek ez dituzte mezu guztiak jasotzen; lana
partizioen arabera banatzen da eta mezu bakoitza behin kontsumitzen da
taldearen barruan. Behatuta (12 mezu gakodun, 3 partiziotan): Consumer A 9
(P0+P1), Consumer B 3 (P2), guztira 12/12 bikoizketarik gabe. Partizio
kopuruak mugatzen du paraleloan lan egin dezakeen consumer kopurua.
Transkripzioa: [7. atala](kafka_exekuzio_isolatua_2026-09-28_5_11.md#7-consumer-group).

## 8. ariketa — consumer bat erortzen bada

Aurreko taldearekin jarraituz: gelditu Consumer 1 (`Ctrl-C`), bidali mezu
gehiago, behatu.

**Erantzuna:** bai, mezuak kontsumitzen jarraitzen dira; taldeak rebalance
egiten du eta bizirik dagoen consumer-ak eroritakoaren partizioak hartzen
ditu. Frogak: erorketaren ONDOREN bidalitako `m8` mezua bizirik zegoen
consumer-ak jaso zuen; `--describe`-ek LAG 0 erakutsi zuen partizio
guztietan (mezu guztiak kontsumituta erorketa gorabehera). Oharra:
puntuz-puntuko log-lerroak galtzea saihesteko, `--max-messages` gabeko
consumer-en irteera ez da froga osoa (buffering); offset commit-ak dira
froga. Transkripzioa: [8. atala](kafka_exekuzio_isolatua_2026-09-28_5_11.md#8-erorketa).

## 9. ariketa — consumer gehiegi

```bash
docker exec "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-topics.sh --create --topic "codex-aabd-${RUN_ID}-eskaerak-2p" --partitions 2 --bootstrap-server "$KAFKA_BOOTSTRAP"
# Hiru consumer TALDE BEREAN abiarazi, gero 6 mezu bidali.
```

**Erantzuna:** 2 partizio + 3 consumer = consumer bat geldirik (inaktibo).
Behatuta: J1 3 mezu, J2 3 mezu, J3 0 mezu (guztira 6/6). Hirurek paraleloan
lan egiteko, topic-ak gutxienez 3 partizio izan behar ditu (`--alter
--partitions 3`; bestela consumer soberakina kendu). Transkripzioa:
[9. atala](kafka_exekuzio_isolatua_2026-09-28_5_11.md#9-consumer-soberakina).

## 10. ariketa — bi consumer group independente

```bash
docker exec -it "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-console-consumer.sh --topic "codex-aabd-${RUN_ID}-salmentak" --group "codex-aabd-${RUN_ID}-analitika" --from-beginning --bootstrap-server "$KAFKA_BOOTSTRAP"
docker exec -it "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-console-consumer.sh --topic "codex-aabd-${RUN_ID}-salmentak" --group "codex-aabd-${RUN_ID}-alertak" --from-beginning --bootstrap-server "$KAFKA_BOOTSTRAP"
```

Producer-etik: `salmenta-001` … `salmenta-004`.

**Erantzuna:** bi taldeek lau mezuak jasotzen dituzte (4/4 eta 4/4).
Talde BEREAN lana banatzen da (7. ariketa); talde DESBERDINEK offset
independenteak dituzte eta bakoitzak kopia osoa irakurtzen du — pub/sub
eredua. Transkripzioa: [10. atala](kafka_exekuzio_isolatua_2026-09-28_5_11.md#10-bi-talde).

## 11. ariketa — offset-a praktikan

```bash
docker exec -it "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-console-consumer.sh --topic "codex-aabd-${RUN_ID}-offset-proba" --group "codex-aabd-${RUN_ID}-offset-taldea" --property print.offset=true --bootstrap-server "$KAFKA_BOOTSTRAP"
```

**Erantzuna:** 10 mezu irakurri ondoren (offset 0–9) eta 5 berri bidalita,
talde BEREAN berrabiaraztean 11. mezutik hasten da (offset 10–14); lehenengo
10ak ez dira errepikatzen. Offset-ak talde bakoitzak partizio bakoitzean
kontsumitutako hurrengo posizioa gordetzen du. `--describe`: 
`CURRENT-OFFSET 15 = LOG-END-OFFSET 15, LAG 0`. Transkripzio osoa:
[11. atala](kafka_exekuzio_isolatua_2026-09-28_5_11.md#11-offset).

## Egiaztapen-erregistroa

| Egiaztapena | Egoera |
|---|---|
| PDFko 5–11 ariketen enuntziatuak (34., 39., 50–54. or.) | Testuarekin berrikusia |
| Erreplika-errorea broker bakarrean | Errore erreala transkribatuta |
| Gako→partizio determinismoa, talde-banaketa, erorketa+rebalance, consumer soberakina, bi talde, offset commit | Broker efimero isolatuan 2026-09-28an exekutatuta; ikus erregistroa |
| Kontsola-komandoak (`--property print.key/print.partition/print.offset`, `kafka-consumer-groups.sh --describe`) | Kafka 3.7.0 irudiarekin egiaztatuta |
| Oharra: 8. ariketako consumer-en log-lerroak | `--max-messages` gabe eta pipe bidez jasoak; buffering dela eta lerroak gal daitezke — offset commit-ak (LAG 0) dira froga, erregistroan dokumentatuta |
