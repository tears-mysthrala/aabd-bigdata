# CNC Guard | plan reproducible Kafka -> NiFi -> scoring -> Elastic

Estado: productor CSV, API, contratos Avro y templates de Elasticsearch
disponibles. Todavía NO existe evidencia de que el recorrido completo
funcione entre servicios. No reutilizar las evidencias MySQL/Mongo del
laboratorio Kafka anterior como prueba de NiFi/Elasticsearch.

## Wire contract

El CSV original tiene ts,makina_id,tenperatura,bibrazioa,presioa,errorea.
scripts/produce_telemetry.py lo valida y emite en Kafka una fila CSV SIN
cabecera con las columnas ordenadas:

    event_id,machine_id,timestamp,temperature,vibration,pressure

El ID es el SHA-256 del contenido normalizado. La etiqueta errorea no se
envía para inferencia. topic: cnc-telemetry-csv, key: machine_id.
Avro schema: integration/telemetry.avsc.

Prueba inicial SIN Kafka:

    uv run --locked python scripts/produce_telemetry.py \
      --csv ../../04_Programazioa_5073/data/cnc_10M.csv --limit 500 \
      --errors reports/rechazos-primera-prueba.json

Para publicar tras levantar broker local:

    uv run --locked --with kafka-python python scripts/produce_telemetry.py \
      --csv ../../04_Programazioa_5073/data/cnc_10M.csv --limit 500 \
      --bootstrap 127.0.0.1:19095 --publish \
      --errors reports/rechazos-publicacion.json

## Implementación NiFi a realizar en el laboratorio

1. ConsumeKafka_2_6 (o equivalente en versión instalada): topic
   cnc-telemetry-csv, consumer group cnc-nifi-v1, bootstrap kafka:29092;
   consumir UNA línea por FlowFile y conservar cabeceras/offset.
2. ConvertRecord: CSVReader con cabecera ausente y esquema explícito
   telemetry.avsc; JsonRecordSetWriter con un OBJETO JSON por FlowFile.
   Comprobar que no produce array; /predict espera objeto único.
3. ValidateRecord: campos, tipos y rangos; malos registros van a
   relación failure y cuarentena duradera con razón. Dedupe persistente
   por event_id; NO confiar en dedupe local del productor tras un reinicio.
4. Rama telemetría: mapear timestamp a @timestamp, añadir ingested_at,
   PutElasticsearchJson en cnc-telemetry-YYYY.MM.DD, ID = event_id;
   aplicar previamente integration/telemetry-template.json.
5. Rama scoring: construir history con máximo tres lecturas anteriores
   de la misma máquina y InvokeHTTP POST a /predict con JSON sin campos
   ajenos al contrato de API. El modelo necesita historia causal para
   reproducir las features históricas; registrar cold start si no hay.
6. EvaluateJsonPath/RouteOnAttribute: clasificar por alert_level OK,
   AVISO, CRITICA. **No indexar directamente el JSON de /predict**:
   preservar `event_id` del FlowFile original, transformar el campo de
   respuesta `timestamp` en `@timestamp` y conservar solo los campos del
   mapping estricto `integration/alerts-template.json`; indexar usando
   `event_id` como `_id` en `cnc-alerts-YYYY.MM.DD`.
   El contrato se valida también mediante `cnc_guard.events.alert_document`.
7. Retry HTTP 5xx y timeouts de forma acotada, 422 a DLQ para investigar;
   backpressure y expiración de reintentos. Guardar counters y provenance.

## Pruebas necesarias para certificar integración

- Nominal: input = indexados válidos + rechazados + duplicados.
- Cabeceras incorrectas, timestamp roto, campos vacíos, NaN, duplicados
  y cambios de esquema; comprobar DLQ con causa legible.
- NiFi parado y reanudado: offsets, retrasos y reconciliación de IDs.
- API detenida: bounded retry y DLQ, no pérdida silenciosa.
- 500/5000/50000 mensajes: tasas medidas, backlog y CPU/RAM reales;
  sin inferir capacidad industrial por la carga de laboratorio.
- Replay at-least-once: escritura idempotente en Elasticsearch.
- Exportar proceso NiFi, versiones, saved objects Kibana y hashes.
  Capturas reales y registros sin secretos.

Los índices de ejemplo son mononodo con una shard y cero réplicas;
NO constituyen alta disponibilidad. Para producción, separar red OT,
autenticar endpoints, configurar TLS y autorización por rol.
