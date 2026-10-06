# Caso 5: ejecución local del 2026-10-05

**Resultado:** recorrido completo verificado en el proyecto fresco
`aabd-kafka-connect-20261005-v78`: **3 → 4 → 4** registros en MySQL, Kafka y
MongoDB, con ambas tareas `RUNNING`. El último 4 corresponde a un reinicio normal
del worker, sin republicar filas. Es una **variante con worker Confluent 7.8.0**;
el worker 7.7.1 del PDF reprodujo un deadlock y no se declara válido.

Enunciado revisado: [Kafka avanzado, pp. 56–69](../../../materialak/01_04_ApacheKafka_aurreratua.pdf).
Se extrajo su texto con `pdftotext -layout -f 56 -l 69` y se inspeccionaron las
capturas incrustadas de Compose, Dockerfile y SQL en las pp. 58–60 con `pdftoppm`.
La [receta reproducible y las nueve respuestas](README.md) reúnen las consignas.

## Entorno final y evidencia

- Broker: `confluentinc/cp-kafka:7.7.1`, KRaft, una partición.
- Worker: base `confluentinc/cp-kafka-connect:7.8.0`; REST declara `7.8.0-ccs`.
- Plugins: JDBC **10.8.9**, MongoDB **1.13.0**, driver MySQL **8.4.0**.
- Bases: MySQL **8.4.11** (`mysql:8.4`) y MongoDB **8.3.11** (`mongo:8`).
- Puertos exclusivamente en `127.0.0.1`: **19094 / 13307 / 12718 / 18083**.
- Límites: broker/worker/MySQL 512 MiB cada uno; MongoDB 384 MiB. Heaps Java
  256 MiB. Se coordinó el arranque después de parar el laboratorio de Elastic.
- Antes del proyecto final: RAM disponible **2,6 GiB**, swap libre **10 GiB**,
  disco libre **34 GiB**. Son instantáneas del host, no medidas de carga sostenida.

Los [hashes de configuraciones y límites](evidencias/preparacion_v78_2026-10-05.json)
y los [IDs/digests de imágenes y versiones](evidencias/versiones_v78_2026-10-05.json)
identifican el entorno ejecutado. Las contraseñas locales están en `.env` y
`private/`, ignorados por Git y Docker; sus valores no aparecen en estos JSON.

| Etapa, hora UTC | MySQL | Topic Kafka | MongoDB | Comprobaciones |
|---|---:|---:|---:|---|
| [Inicial, 09:00:45](evidencias/inicial_v78_2026-10-05.json) | 3 | 3 | 3 | 11/11, PASS |
| [Streaming, 09:01:32](evidencias/streaming_v78_2026-10-05.json) | 4 | 4 | 4 | 11/11, PASS |
| [Reinicio, 09:04:51](evidencias/reinicio_v78_2026-10-05.json) | 4 | 4 | 4 | 11/11, PASS |

El [resumen contrastado](evidencias/resumen_v78_2026-10-05.json) comprueba que las
tres etapas usan `7.8.0-ccs`. El SHA-256 del archivo de offsets es idéntico antes
y después del reinicio. Un `jstack` posterior terminó con código 0 y sin el
marcador de deadlock. Las filas/documentos son exactamente:

```text
1 | 1 | Football
2 | 2 | Basketball
3 | 3 | Running
4 | 2 | Streaming
```

Cada JSON contiene estados REST de conector **y task**, versiones de plugins,
filas MySQL, offsets y todos los mensajes Kafka con su esquema, documentos
MongoDB con `_id` estable, presencia/hash del archivo de offsets y estado/puertos
de los cuatro contenedores. Ninguno aparece terminado por OOM durante esas tomas.

## Comandos y resultados observados

Desde este directorio, usando la configuración final:

```bash
python preparar_lab.py
docker compose config --quiet
docker compose build connect
docker compose up -d --wait --wait-timeout 240
docker compose exec -T -w /opt/kafka-connect/config connect \
  connect-standalone connect-standalone.properties
```

Construcción y configuración: código 0. Contenedores base saludables y contenedor
Connect activo; el worker se inicia manualmente. Tras el mensaje de REST listo,
en otra terminal se registraron, secuencialmente:

```bash
python registrar_conector.py mysql-source --aplicar
python registrar_conector.py mongodb-sink --aplicar
python verificar_lab.py --etapa inicial --salida evidencias/inicial_v78_2026-10-05.json
```

Ambos registros devolvieron `{"registered":"<nombre>","http_status":201}`
y el verificador terminó con código 0. El topic fue `iabd-retail_db-categories`
y MongoDB el destino `iabd.categories`, con tres registros coincidentes.

La inserción fue la literal del PDF, una sola vez en este proyecto:

```bash
docker compose exec -T mysql sh -c \
  'MYSQL_PWD="$MYSQL_PASSWORD" mysql -uiabd retail_db' <<'SQL'
INSERT INTO categories (category_department_id,category_name) VALUES (2, 'Streaming');
SQL
python verificar_lab.py --etapa streaming --salida evidencias/streaming_v78_2026-10-05.json
```

INSERT: código 0. La segunda verificación terminó con código 0, cuatro registros
completos y el ID 4 para Streaming. No se generó el mensaje con Python: lo produjo
el JDBC source al consultar la nueva fila.

Para el reinicio se envió SIGTERM al proceso Java del worker, se esperó su cierre,
se paró/arrancó el contenedor Connect y se repitieron el arranque manual y ambos
registros REST. Las configuraciones standalone residen en memoria; los offsets
se conservan en el volumen. Los dos registros volvieron a devolver HTTP 201.

```bash
docker compose exec -T connect pkill -TERM -f '[o]rg.apache.kafka.connect.cli.ConnectStandalone'
# Esperar el cierre del worker en su terminal antes de continuar.
docker compose stop -t 30 connect
docker compose up -d --wait --wait-timeout 120 connect
# Repetir arranque manual y registro REST de los dos conectores.
python verificar_lab.py --etapa reinicio --salida evidencias/reinicio_v78_2026-10-05.json
```

La última verificación terminó con código 0. Se conservaron cuatro mensajes,
sin replay del source en este ciclo. El [cierre previo al reinicio](evidencias/cierre_worker_v78_2026-10-05.txt)
y el [cierre final](evidencias/cierre_final_worker_v78_2026-10-05.txt) muestran
`Stopped FileOffsetBackingStore`, `Worker stopped`, `Herder stopped` y
`Kafka Connect stopped`. La salida 143 del `docker exec` es la terminación por
SIGTERM, acompañada de esas señales de cierre normal.

## Diagnóstico del entorno literal 7.7.1

Estas evidencias pertenecen al proyecto anterior `aabd-kafka-connect-20261005`
y se conservan separadas del resultado final:

1. El healthcheck REST heredado de la imagen no encajaba con `sleep infinity`
   y el arranque posterior del worker. `up --wait` terminó con
   `application not healthy after 4m0s`. Compose desactiva esa comprobación en
   el contenedor Connect y verifica su readiness por REST en el paso manual.
2. El comando con los dos properties en CLI y otra prueba con solo el source
   se bloquearon. El [jstack del comando del PDF](evidencias/deadlock_cli_2026-10-05.txt)
   muestra inversión de locks entre `StandaloneHerder` y `MemoryConfigBackingStore`
   desde `TableMonitorThread`, con `Found 1 deadlock`.
3. El primer registro REST permitió [3 filas iniciales](evidencias/inicial_2026-10-05.json)
   y la inserción Streaming, pero la API del POST source agotó 30 segundos
   y finalmente registró HTTP 500 a los 90 segundos. El
   [reinicio con registro REST](evidencias/deadlock_rest_reinicio_2026-10-05.txt)
   volvió a bloquearse. Una captura Streaming interrumpida al parar el worker
   antes de su último GET falló con conexión cerrada; no produjo un JSON PASS.
4. La prueba `table.monitoring.startup.polling.limit.ms=0` produjo
   [connector FAILED aunque task RUNNING](evidencias/startup_polling_cero_2026-10-05.json),
   con `Task already exists in this worker: mysql-source-0`. Se descartó y no
   forma parte de la configuración final.

El patrón observado coincide con la incidencia oficial
[KAFKA-16051](https://issues.apache.org/jira/browse/KAFKA-16051), corregida upstream
en Kafka 3.8.0. La coincidencia respalda la elección de Connect 7.8.0; no se
presenta como una prueba de identidad entre builds Confluent y upstream.

## Estado final y alcance

Los dos proyectos se paran conservando sus cuatro volúmenes de datos por
proyecto. No se ejecuta `down -v`, `prune` ni borrado, y no se alteran otros labs.
La receta, las tres comprobaciones v78, las nueve respuestas y el diagnóstico
del entorno del PDF quedan disponibles para revisión.

La evidencia cubre estas filas sintéticas, esta inserción y este reinicio;
no prueba exactly-once ante cualquier fallo, carga sostenida, cambios/borrados
SQL ni entrega en Moodle. `incrementing` solo detecta IDs nuevos crecientes.
Los tags MySQL/MongoDB son mutables; los digests guardados identifican esta ejecución.
