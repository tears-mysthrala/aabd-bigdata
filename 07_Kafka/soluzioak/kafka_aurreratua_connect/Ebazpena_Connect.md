# Kafka Connect: MySQL → Kafka → MongoDB — ebazpena (4.1–4.3 + bide osoa)

> **5. kasu berria (56–69. or.):** ingurune eta agindu eguneratuak
> [caso5/README.md](caso5/README.md) fitxategian daude: Compose + broker
> Confluent 7.7.1 (KRaft), worker 7.8.0 aldaera dokumentatua, MySQL 8.4,
> MongoDB 8 eta `iabd.categories`. Dokumentu honetako 2026-09-29ko
> 6 erregistroak aurreko exekuzioaren froga dira; PDF berriak 3 hasierako
> errenkada eta `Streaming` laugarrena ditu.

Iturria: [`01_04_ApacheKafka_aurreratua.pdf`](../../materialak/01_04_ApacheKafka_aurreratua.pdf),
17–27. or. Fitxategiak: [`categories-schema.sql`](categories-schema.sql),
[`connect-standalone.properties`](connect-standalone.properties),
[`mysql-source.properties`](mysql-source.properties),
[`mongodb-sink.properties`](mongo-sink.properties).

> **Egoera 2026-09-29: EXEKUTATUTA eta egiaztatuta.** Worker standalone
> (`apache/kafka:3.7.0`), MySQL 8.4 + Mongo 7.0 efimeroak, guztiak `--rm`.
> Bide osoa: 6 errenkada MySQL → 6 mezu topic-ean → 6 dokumentu MongoDBn.
> Ohar teknikoak: (1) CLI bidez bigarren konektorea sortzea trabatu egiten da
> (`processExtraArgs` zain; 3.7 standalone) — sink-a REST POST bidez sortu zen
> (PDF 4.3 eredua); (2) ez poll-eatu RESTik task-trantsizioetan (deadlock
> ezaguna); (3) JDBC plugin-a Maven piezekin muntatu zen (Confluent Hub
> eskuraezin: `kafka-connect-jdbc` + `mysql-connector-j` + `guava` + `re2j`).

## 4.1 MySQL categories

`categories-schema.sql`: `category_id` PK auto_increment,
`category_department_id`, `category_name`; `mode=incrementing` zutabea
`category_id` da (Connect-ek horren arabera detektatzen ditu berriak).

## 4.2 Konfigurazioa

- Worker: bootstrap + `JsonConverter` (`schemas.enable=true` →
  `{schema, payload}`) + offset fitxategia + `plugin.path`.
- Source: `JdbcSourceConnector`, `tasks.max=1`, `retail_db`,
  `table.whitelist=categories`, `topic.prefix=iabd-retail_db-`
  (hori da `iabd-retail_db-categories` topic-izena).
- Pluginak: JDBC konektorea + MySQL driverra + guava, `plugin.path` azpiko
  `jdbc/` karpetan (Confluent Hub eskuraezin → Maven bidezko piezak).

## Exekuzioa (egiaztatuta 2026-09-29)

```bash
# Lehenik properties konkretuak sortu (${} ez da Connect-en hedatzen).
# Ezarri aldagaiak zure ingurunean (.env / pass-cli — baliorik ez repoan):
# BOOTSTRAP, PLUGIN_PATH, MYSQL_JDBC_URL, MYSQL_USER, MYSQL_PASSWORD, MONGO_URI
./sortu_connect_config.sh
connect-standalone.sh generated/connect-standalone.properties \
  generated/mysql-source.properties
kafka-console-consumer.sh --topic iabd-retail_db-categories --from-beginning \
  --bootstrap-server <broker>:9092   # {schema,payload} JSON (PDF 25. or.)
curl <worker>:8083/ ; curl <worker>:8083/connectors
curl <worker>:8083/connectors/mysql-source/status
# Sink-a REST bidez (PDF 4.3): POST /connectors {mongodb-sink...}
```

Behatuta: `GET /` → `{"version":"3.7.0",...}`;
`/connectors` → `["mysql-source"]` (+`"mongodb-sink"` POST ondoren);
`mysql-source/status` → connector + task `RUNNING`.
Topic-ean 5 mezu `{schema,payload}` (PDF 25. or. eredua) + 6. insert-aren
ondoren 6. mezua. MongoDB `retail_sink.categories`: 5 dokumentu, 6. insert
(`Kirolak`) automatikoki agertu — `countDocuments() = 6`.
```

## 4.3 bide osoa (source + sink)

```bash
connect-standalone.sh generated/connect-standalone.properties \
  generated/mysql-source.properties generated/mongo-sink.properties
# (CLI bidez bi konektore aldi berean trabatu daiteke; orduan sink-a REST
#  POST bidez — goian bezala.)
# MySQL-an insert → automatiko MongoDBan (retail_sink.categories)
```

## Egiaztapen-erregistroa

| Egiaztapena | Egoera |
|---|---|
| SQL + 3 properties + plugin-zerrenda | Transkribatuta PDFtik, kredentzialak `${}` bidez |
| Source → topic (5 errenkada, `{schema,payload}`) | Exekutatuta |
| REST API (`/`, `/connectors`, `/status`) | `RUNNING`/`RUNNING` |
| Sink → Mongo (5 dokumentu) + 6. insert automatikoa | `countDocuments() = 6` |
