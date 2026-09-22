# 07_Kafka — soluzioak ✅ (0. kasua + 1. kasua + DF3)

Teoria: `../materialak/01_03_ApacheKafka.pdf` (1150 lerro testu: pub/sub, partizioak, consumer groups, acks, LAG).

## Fitxategiak
- `docker-compose.yml` — `apache/kafka:3.7.0` KRaft (Zookeeper gabe), `localhost:9092`, topic auto-create.
- `kafka_producer.py` / `kafka_consumer.py` — PDF 10.2/10.3-ko kodea, `localhost`-era egokitua + `--keys` + `--mock`.
- `test_kafka_mock.py` — roundtrip broker gabe (10 mezu).
- `requirements.txt` — `kafka-python`, `pymongo`, `faker` (DF3.3).

## 0. kasua (kontsola, broker martxan)
```bash
docker compose up -d && docker ps
docker exec -it iabd-kafka /opt/kafka/bin/kafka-topics.sh --create --topic iabd-topic --bootstrap-server localhost:9092
docker exec -it iabd-kafka bash
/opt/kafka/bin/kafka-console-producer.sh --topic iabd-topic --bootstrap-server localhost:9092
/opt/kafka/bin/kafka-console-consumer.sh --topic iabd-topic --from-beginning --bootstrap-server localhost:9092
```

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

## DF3.1 / DF3.2 / DF3.3 (proposamena, PDF 09 atala + 10.1 oharrak)
- **DF3.1 — partizioak + gakoak**: topic 3 partiziorekin sortu, `kafka_producer.py --keys` erabili;
  gako bera → partizio bera (ordena entitate-mailan). Egiaztatu `--property print.key=true`-rekin kontsolan.
- **DF3.2 — consumer groups**: 2 consumer `iabd-app1` taldean + 1 `iabd-app2`-n;
  talde-barruan banaketa, talde-artean denek mezu berak (offset independenteak). `kafka-consumer-groups.sh --describe`.
- **DF3.3 — MongoDB sink**: consumer batetik `pymongo`-rekin txertatu (`faker` datuekin);
  patroia `06_NiFi/.../06_MariaDB_MongoDB_Laborategia_DF2.2`-ko Record API bulk-aren bera.
