# 2. kasua: Kafka Klusterra + Python + NiFi — ebazpena (1–6)

Iturria: [`01_04_ApacheKafka_aurreratua.pdf`](../../materialak/01_04_ApacheKafka_aurreratua.pdf),
15–16. or. Exekuzio erreala 2026-09-29an: 3 broker (ZK modua,
`apache/kafka:3.7.0`), container efimeroak, gero ezabatuak.
Fitxategiak: [`compose.yaml`](compose.yaml),
[`broker.properties.txantiloia`](broker.properties.txantiloia),
[`personas_producer.py`](personas_producer.py),
[`personas_consumer.py`](personas_consumer.py),
[`nifi_consumer_2_kasua.py`](nifi_consumer_2_kasua.py).

> Oharra: PDFak KRaft aipatzen du kluster-topologian, baina 3.7.0 irudiarekin
> eta RAM mugatuarekin ZK modua erabili da (RF=2rako baliokidea). Compose
> barruan zerbitzu-izenek DNS bidez ebazten dute; `--network connect`
> gurutzatuarekin IPak erabili behar dira (ikus 5. atala).

## 1. Kafka klusterra — compose 3 broker + NiFi

```bash
./sortu_broker_config.sh   # txantiloitik broker-1/2/3.properties
docker compose up -d
```

`compose.yaml`: `zoo1` + `kafka1..3` (heap 512m, `127.0.0.1:1909x:1909x`).
NiFi DF2.2 stack-a bereiz martxan (`iabd-nifi`); 5. ataserako brokerrak
`iabd-nifi-lab-net` sarera konektatu ziren.

## 2. Topic-a: 4 partizio + RF=2, describe

```bash
kafka-topics.sh --create --topic codex-personas --partitions 4 \
  --replication-factor 2 --bootstrap-server <broker>:9092
kafka-topics.sh --describe --topic codex-personas --bootstrap-server <broker>:9092
```

Behatuta:

```text
Topic: codex-personas  PartitionCount: 4  ReplicationFactor: 2
Partition: 0  Leader: 3  Replicas: 2,3  Isr: 2,3
Partition: 1  Leader: 1  Replicas: 3,1  Isr: 1,3
Partition: 2  Leader: 1  Replicas: 1,2  Isr: 1,2
Partition: 3  Leader: 1  Replicas: 2,1  Isr: 1,2
```

Leaderrak 3 brokerretan banatuta; ISR osoa (RF=2 beteta).

## 3. Python Producer — Faker, 10 pertsona

```bash
BOOTSTRAP=127.0.0.1:19092 TOPIC=codex-personas \
  python personas_producer.py --n 10 --seed 42
```

`Faker("es_ES")`, seed finkoa (errepikagarria); key=emaila, value JSON
`{izena, adina, hiria, emaila}`. Behatuta: 10/10 bidalita, P0/P1/P2/P3
guztietan (gako-hash bidez).

## 4. Python Consumer — Partition | Offset | Key | Value

```bash
BOOTSTRAP=127.0.0.1:19092 TOPIC=codex-personas GROUP=codex-personas-py \
  python personas_consumer.py --max 10 --from-beginning
```

Behatuta: 10/10, `P:<p> O:<o> K:<email> V:<json>` formatuan.

## 5. NiFi Consumer — talde desberdina

`nifi_consumer_2_kasua.py --brokers <ip>:9092` (API bidez, canvasa zikindu gabe;
amaieran `--cleanup`):
`ConsumeKafka (group codex-personas-nifi, earliest)` → `UpdateAttribute
(filename=${kafka.key})` → `PutFile /tmp/nifi-personas`.
NiFi 2.0 ohartxoak: processor mota `...kafka.processors.ConsumeKafka` da
(record motakoa: `Kafka3ConnectionService` + `JsonTreeReader` +
`JsonRecordSetWriter` behar ditu, `Output Strategy=USE_VALUE`,
`Key Format=string`); konexioetan `groupId` bidali behar da; controller
service-ak `run-status` endpointetik desgaitzen dira.
Sare-oharra: brokerrak NiFi-ren sarean egon behar dira ETA
`advertised.listeners`eko PLAINTEXT helbidea NiFi-tik iristekoa izan behar da
(bestela metadata zaharrak timeoutak eragiten ditu — consumerra STOP/RUNNING
birpasatu behar izan zen).

## 6. Egiaztatu: mezu berdinak

```text
MEZU BERDINAK: 10/10
```

Bi consumer-ek (`codex-personas-py2` eta `codex-personas-nifi`, group
desberdinak) email multzo bera jaso zuten. Konparaketa ez zen fitxategi-izenen
gainekoa bakarrik: NiFi-ko emailak fitxategien edukitik (JSON payload,
`emaila` eremua) atera ziren eta Python consumer-eko key-ekin alderatu
(`exekuzioa_2026-09-29_2_kasua.md`-n).

## Egiaztapen-erregistroa

| Egiaztapena | Egoera |
|---|---|
| 3 broker + ZK, topic 4P/RF2 + describe (Leader/Replicas/ISR) | Exekutatuta 2026-09-29 |
| Faker producer 10 pertsona (seed 42) | 10/10, P0–P3 |
| Python consumer P\|O\|K\|V | 10/10 |
| NiFi ConsumeKafka (beste group) → PutFile | 10 fitxategi |
| Bi consumer-etan mezu berdinak | diff 10/10 |
| Amaieran: NiFi PG-ak ezabatuta, /tmp/nifi-personas garbituta | Canvasa ukitu gabe |
