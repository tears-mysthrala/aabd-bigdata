# Connect: exekuzio-erregistroa (2026-09-29)

**Ingurunea:** `apache/kafka:3.7.0` (broker 1 + ZK + worker), `mysql:8.4`,
`mongo:7.0` — denak container efimeroak (`--rm`), amaieran ezabatuak.
Worker: heap 768m, `plugin.path` JDBC (`kafka-connect-jdbc` 10.8.9 +
`mysql-connector-j` 9.0.0 + `guava` + `re2j`) + Mongo sink
(`mongo-kafka-connect` 1.13.0 `-all`).

## REST (4.3)

```text
GET / → {"version":"3.7.0","commit":"2ae524ed625438c5","kafka_cluster_id":"yEOxBVA9QEeYw96330e1PQ"}
GET /connectors → ["mysql-source"]  (+ ["mysql-source","mongodb-sink"] POST ondoren)
GET /connectors/mysql-source/status → connector RUNNING + task 0 RUNNING
```

## Topic (4.1/4.2): iabd-retail_db-categories

5 mezu `{schema,payload}` (PDF 25. or. eredua), adib.:

```json
{"schema":{"type":"struct","fields":[
  {"type":"int32","optional":false,"field":"category_id"},
  {"type":"int32","optional":false,"field":"category_department_id"},
  {"type":"string","optional":false,"field":"category_name"}],
  "optional":false,"name":"categories"},
 "payload":{"category_id":1,"category_department_id":1,"category_name":"Futbola"}}
```

## Mongo (bide osoa): retail_sink.categories

6 dokumentu (5 + `Kirolak` automatikoa MySQL insert-aren ondoren):

```text
1 Futbola | 2 Saskibaloia | 3 Ordenagailuak
4 Telefonoak | 5 Liburuak | 6 Kirolak
```

Topic-kontsumoa: 6/6 mezu (`category_id` 1–6).

## Gorabeherak

- CLI bidez bigarren konektorea sortzea trabatu (`processExtraArgs` zain);
  sink-a REST POST bidez (PDF 4.3).
- REST vs task-update aldi berean = deadlock (3.7 standalone): ez poll-eatu
  trantsizioetan.
- Confluent Hub eskuraezin (cloudfront): pluginak Maven piezekin;
  `re2j` falta zen (`NoClassDefFoundError`) — gehituta.
