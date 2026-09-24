# 07_Kafka — soluzioak ✅ (0. kasua + 1. kasua + DF3)

Teoria: `../materialak/01_03_ApacheKafka.pdf` (1150 lerro testu: pub/sub, partizioak, consumer groups, acks, LAG).

## Fitxategiak
- `kafka_producer.py` / `kafka_consumer.py` — PDF 10.2/10.3-ko kodea, `localhost`-era egokitua + `--keys` + `--mock` + `--csv`.
  Defaults desde entorno (`TOPIC`, `GROUP`, `BOOTSTRAP`; ver `.env.example`).
- `test_kafka_mock.py` — roundtrip broker gabe (10 mezu).
- `requirements.txt` — `kafka-python`, `pymongo`, `faker` (DF3.3).
- **Broker**: vive en `infra/` (`docker compose up -d kafka` allí). Este lab es solo código.

## 0. kasua (kontsola, broker martxan: antes `cd ../../infra && docker compose up -d kafka`)
```bash
docker exec -it iabd-kafka /opt/kafka/bin/kafka-topics.sh --create --topic iabd-topic --bootstrap-server localhost:9092
docker exec -it iabd-kafka bash
/opt/kafka/bin/kafka-console-producer.sh --topic iabd-topic --bootstrap-server localhost:9092
/opt/kafka/bin/kafka-console-consumer.sh --topic iabd-topic --from-beginning --bootstrap-server localhost:9092
```

## PDFko 1–5 kontsola-ariketak

Erantzunak, komandoak eta 4. ariketako partizio/offset taula betetzeko txantiloia: [ariketa_kontsola_topic_partizio_offset.md](ariketa_kontsola_topic_partizio_offset.md). `infra/docker-compose.yml`-ko Kafka 3.7.0 (`iabd-kafka`) zerbitzura egokituta dago. Komandoak berrikusi dira, baina ez dira brokerrean exekutatu: dokumentuak topic izen prefijatuak erabiltzen ditu zuzeneko proba baterako, eta ez ditu container, topic edo bolumen partekatuak aldatu. Partizio/offset zenbakiek brokerreko egoera erreal bat behar dute.

## 1. kasua (Python)
```bash
pip install -r requirements.txt
python kafka_producer.py --n 10   # beste terminalean:
python kafka_consumer.py --max 10
```

## Mock (broker gabe, CI)
```bash
python kafka_producer.py --mock --n 10
python kafka_consumer.py --mock --max 10
pytest test_kafka_mock.py -v
```

## Test real 2026-09-22 (broker KRaft local, `cnc_10M.csv`)
```bash
# Funcional: 100k con clave makina_id
python kafka_producer.py --topic iabd-cnc --csv ../../04_Programazioa_5073/data/cnc_10M.csv --n 100000 --keys
python kafka_consumer.py --topic iabd-cnc --group iabd-verifica --max 100000 --quiet
# -> 100000 producidos → 100000 consumidos ✅
```
## Throughput 2026-09-22 (topic `iabd-tput`, 3 particiones, CSV en streaming)

| Sentido | Volumen | Tiempo | Ritmo |
|---|---|---|---|
| produce (3 en paralelo, `--keys`, 333k cada uno) | 1M | 21 s | ~48k/s |
| consume (`--quiet`, 1 grupo) | 1M | 59 s | ~17k/s |

Extrapolación honesta a 10M (≈1.2 GB en broker): **~3.5 min produciendo, ~10 min
consumiendo** (mismo nodo, sin réplicas). Los 10M enteros por Kafka **no** se han
movido (coste ~15 min + 1.2 GB): el benchmark de 1M es representativo y repetible.
Lección: el producer inicial tardaba 171 s/100k porque materializaba todo el CSV
en memoria (`list(reader)`); en streaming (`islice`) ×30 más rápido.

## DF3.1 / DF3.2 / DF3.3 (proposamena, PDF 09 atala + 10.1 oharrak)
- **DF3.1 — partizioak + gakoak**: topic 3 partiziorekin sortu, `kafka_producer.py --keys` erabili;
  gako bera → partizio bera (ordena entitate-mailan). Egiaztatu `--property print.key=true`-rekin kontsolan.
- **DF3.2 — consumer groups**: 2 consumer `iabd-app1` taldean + 1 `iabd-app2`-n;
  talde-barruan banaketa, talde-artean denek mezu berak (offset independenteak). `kafka-consumer-groups.sh --describe`.
- **DF3.3 — MongoDB sink**: consumer batetik `pymongo`-rekin txertatu (`faker` datuekin);
  patroia `06_NiFi/.../06_MariaDB_MongoDB_Laborategia_DF2.2`-ko Record API bulk-aren bera.
