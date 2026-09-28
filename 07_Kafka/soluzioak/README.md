# 07_Kafka — soluzioak ✅ (0. kasua + 1. kasua + DF3)

Teoria: `../materialak/01_03_ApacheKafka.pdf` (1150 lerro testu: pub/sub, partizioak, consumer groups, acks, LAG).

## Fitxategiak
- `kafka_producer.py` / `kafka_consumer.py` — PDF 10.2/10.3-ko kodea, `localhost`-era egokitua + `--keys` + `--mock` + `--csv`.
  Defaults desde entorno (`TOPIC`, `GROUP`, `BOOTSTRAP`; ver `.env.example`).
- `test_kafka_mock.py` — roundtrip broker gabe (10 mezu).
- `requirements.txt` — `kafka-python`, `pymongo`, `faker` (DF3.3);
  son rangos de versiones, no un entorno bloqueado reproducible.
- **Broker compartido**: `infra/` define `iabd-kafka` y el volumen persistente `iabd-kafka-data`. No usarlo para practicar, borrar/recrear topic-ak, ni ejecutar los ejemplos siguientes: topic aurrizkiak ez du broker/volume hori isolatzen. Erabili soilik container independente bat. 2026-09-25eko [exekuzio isolatua](kafka_exekuzio_isolatua_2026-09-25.md) container efimeroan egin da eta amaieran ezabatu da.

## 0. kasua (kontsola — broker isolatu batean bakarrik)

Ez erabili `infra/`ko Compose-a laborategi isolatu gisa eta ez abiarazi/gelditu zerbitzurik gida honengatik. Ezarri beheko balioak zure Kafka 3.7.0 labeko container eta broker-helbiderako; erabili `RUN_ID` berri bat 0. kasua berriz egiten duzun bakoitzean.

```bash
export KAFKA_CONTAINER='LAB_ISOLATUKO_KAFKA_CONTAINERA'
export KAFKA_BOOTSTRAP='brokerra-containerretik-iristeko:9092'
export RUN_ID='RUN_BAKOITZERAKO_BERRIA'
export TOPIC="codex-aabd-${RUN_ID}-hello"
export GROUP="codex-aabd-${RUN_ID}-hello-read"
docker exec "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-topics.sh --create --topic "$TOPIC" --bootstrap-server "$KAFKA_BOOTSTRAP"
docker exec -it "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-console-producer.sh --topic "$TOPIC" --bootstrap-server "$KAFKA_BOOTSTRAP"
docker exec -it "$KAFKA_CONTAINER" /opt/kafka/bin/kafka-console-consumer.sh --topic "$TOPIC" --group "$GROUP" --from-beginning --bootstrap-server "$KAFKA_BOOTSTRAP"
```

## PDFko 1–5 kontsola-ariketak

Erantzunak eta komandoen txantiloia: [ariketa_kontsola_topic_partizio_offset.md](ariketa_kontsola_topic_partizio_offset.md). Kafka 3.7.0 CLI sintaxiarekin eta broker efimeroko [exekuzio errealarekin](kafka_exekuzio_isolatua_2026-09-25.md) berrikusita dago. Txantiloiko komandoak ez zuzendu `iabd-kafka` partekatura; behatutako partizio/offset zenbakiak exekuzio hartakoak soilik dira.

## 1. kasua (Python)
```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
BOOTSTRAP=localhost:19092 .venv/bin/python kafka_producer.py --n 10
BOOTSTRAP=localhost:19092 .venv/bin/python kafka_consumer.py --max 10
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
# Resultado histórico no verificable solo con este repositorio.
```
## Throughput 2026-09-22 (topic `iabd-tput`, 3 particiones, CSV en streaming)

| Sentido | Volumen | Tiempo | Ritmo |
|---|---|---|---|
| produce (3 en paralelo, `--keys`, 333k cada uno) | 1M | 21 s | ~48k/s |
| consume (`--quiet`, 1 grupo) | 1M | 59 s | ~17k/s |

Estos tiempos son notas de una ejecución histórica; no se conservan logs,
configuración completa ni offsets que permitan certificarlos desde el repo.
El código actual espera ACK de cada envío por lotes acotados y usa `acks=all`,
por lo que **no hay benchmark actualizado comparable**. Una regla de tres a
10M sería solo una estimación, no un resultado medido. El CSV se lee en
streaming (`islice`) para no materializarlo entero; el consumer confirma
offsets al final de cada ejecución, tras procesar los mensajes impresos.

## DF3.1 / DF3.2 / DF3.3 (proposamena, PDF 09 atala + 10.1 oharrak)
- **DF3.1 — partizioak + gakoak**: topic 3 partiziorekin sortu, `kafka_producer.py --keys` erabili;
  gako bera → partizio bera (ordena entitate-mailan). Egiaztatu `--property print.key=true`-rekin kontsolan.
- **DF3.2 — consumer groups**: 2 consumer `iabd-app1` taldean + 1 `iabd-app2`-n;
  talde-barruan banaketa, talde-artean denek mezu berak (offset independenteak). `kafka-consumer-groups.sh --describe`.
- **DF3.3 — MongoDB sink**: consumer batetik `pymongo`-rekin txertatu (`faker` datuekin);
  patroia `06_NiFi/.../06_MariaDB_MongoDB_Laborategia_DF2.2`-ko Record API bulk-aren bera.
