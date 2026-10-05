# Caso 5: MySQL → Kafka Connect → MongoDB

Enunciado: [Kafka avanzado, pp. 56–69](../../../materialak/01_04_ApacheKafka_aurreratua.pdf).
Esta receta amplía la [resolución anterior de Connect](../Ebazpena_Connect.md)
y conserva su [evidencia del 29/09](../exekuzioa_2026-09-29_connect.md) como
ejecución histórica. El PDF usa imágenes de **Confluent Platform 7.7.1** para
Kafka KRaft y Connect, MySQL **8.4**, MongoDB **8** y destino **`iabd.categories`**.
Esta receta mantiene el broker 7.7.1 y selecciona **Connect 7.8.0** como variante
por un deadlock reproducido con el worker 7.7.1. La diferencia queda explícita;
el tag de Confluent no es la versión upstream de Kafka.

El objetivo es trasladar las filas nuevas de `retail_db.categories` al topic
`iabd-retail_db-categories` y a MongoDB sin escribir un producer ni un consumer
propios. El SQL del PDF contiene **Football, Basketball y Running**; después
de insertar **Streaming**, deben verse cuatro filas, cuatro mensajes y cuatro
documentos con los mismos campos.

## Archivos y decisiones de la receta

| Archivo | Función |
|---|---|
| [compose.yaml](compose.yaml) | Broker KRaft, MySQL, MongoDB y contenedor Connect; puertos y volúmenes independientes. |
| [Dockerfile](Dockerfile) | Base configurable (`CONNECT_VERSION`, 7.7.1 por defecto); Compose elige 7.8.0. Instala JDBC 10.8.9, Mongo 1.13.0 y driver MySQL 8.4.0. |
| [mysql/init.sql](mysql/init.sql) | Tabla y tres filas exactas de la captura del PDF, p. 60. |
| [config/connect-standalone.properties](config/connect-standalone.properties) | Broker interno, convertidores JSON con schema, plugins, REST y offsets persistentes. |
| [config/mysql-source.properties](config/mysql-source.properties) | JDBC source, `category_id` incremental y prefijo del topic. |
| [config/mongodb-sink.properties](config/mongodb-sink.properties) | Sink del topic a `iabd.categories`. |
| [preparar_lab.py](preparar_lab.py) | Crea credenciales solo para este laboratorio en archivos locales ignorados; conserva las existentes. |
| [registrar_conector.py](registrar_conector.py) | Previsualiza o registra un conector por REST, leyendo sus properties; no sobrescribe conectores existentes. |
| [verificar_lab.py](verificar_lab.py) | Consulta el laboratorio real y guarda evidencia agregada sin contraseñas; no inserta ni modifica datos. |

Las capturas de las pp. 58–60 se revisaron visualmente porque el código
incrustado no sale con `pdftotext`. Se mantiene el arranque manual del worker
del PDF. Se cambian los nombres fijos de contenedor por el
proyecto Compose **`aabd-kafka-connect-20261005-v78`**, se publican los puertos solo
en `127.0.0.1`, se conservan los cuatro volúmenes y se fijan los plugins en
vez de usar `latest`. Las credenciales docentes `root/iabd` se sustituyen por
valores aleatorios locales; no hay datos personales ni credenciales reales.

El sink añade una clave `_id` estable basada en `category_id` y escritura
`ReplaceOneDefaultStrategy`: una entrega repetida se resuelve como upsert.
Esto no convierte el pipeline en exactly-once. La explicación de ambas
opciones está en la [documentación oficial de MongoDB 1.13](https://www.mongodb.com/docs/kafka-connector/v1.13/sink-connector/configuration-properties/all-properties/).

| Servicio | Acceso desde el host | Acceso dentro de Docker | Límite de RAM |
|---|---|---|---|
| Kafka | `localhost:19094` | `kafka:29092` | 512 MiB; heap 256 MiB |
| MySQL | `localhost:13307` | `mysql:3306` | 512 MiB |
| MongoDB | `localhost:12718` | `mongodb:27017` | 384 MiB; caché 0,25 GiB |
| Connect REST | `localhost:18083` | `connect:8083` | 512 MiB; heap 256 MiB |

Son límites para cuatro filas sintéticas, no valores de producción. El
contenedor Connect arranca con `sleep infinity`: un contenedor activo no
significa que su REST API esté disponible. El PDF pide `curl` antes de arrancar
el worker; esa comprobación debe hacerse **después del paso 3** de esta receta.
La imagen base trae un healthcheck REST; se desactiva para esta fase manual,
porque `up --wait` bloquearía antes de poder iniciar el worker. La API y ambas
tareas se verifican expresamente en el paso 3 y con `verificar_lab.py`.

## 1. Preparar y construir

Se necesitan Docker Engine, Docker Compose, Python 3 y `curl`. Esta receta de
bind mounts usa el UID **1000**, igual que `appuser` en la imagen Connect.
En otra máquina hay que adaptar propiedad de archivos/volumen antes de usarla;
el preparador se detiene si el UID no coincide. Ejecutar desde este directorio:

```bash
cd 07_Kafka/soluzioak/kafka_aurreratua_connect/caso5
free -h
df -h .
ss -ltn '( sport = :19094 or sport = :13307 or sport = :12718 or sport = :18083 )'
python preparar_lab.py
docker compose config --quiet
docker compose build connect
```

Los cuatro puertos deben estar libres. Las descargas proceden de las imágenes
oficiales, Confluent Hub y Maven Central. Las licencias son Confluent Community
License para JDBC y Apache 2.0 para MongoDB Connector. La imagen base del PDF
usa el cliente `confluent-hub`, que instala los plugins en
`/usr/share/confluent-hub-components`; el driver se coloca en el subdirectorio
`lib/` de JDBC. No se reutiliza el montaje artesanal de JAR del laboratorio antiguo.

`.env` y `private/mysql.properties` quedan fuera de Git y del contexto de
construcción. No ejecutar `docker compose config` sin `--quiet` para capturas:
la configuración expandida contiene las contraseñas del laboratorio.

## 2. Arrancar los cuatro contenedores y consultar MySQL

```bash
docker compose up -d --wait --wait-timeout 240
docker compose ps
docker compose exec -T mysql sh -c \
  'MYSQL_PWD="$MYSQL_PASSWORD" mysql -uiabd retail_db -e "SELECT * FROM categories"'
```

En un volumen MySQL nuevo el resultado inicial es:

```text
category_id  category_department_id  category_name
1            1                       Football
2            2                       Basketball
3            3                       Running
```

`category_id` es la clave primaria autoincremental; el segundo campo identifica
el departamento y el tercero es el nombre. `init.sql` solo se aplica al
inicializar un volumen vacío. Volver a ejecutar `up` conserva los datos: si
ya está `Streaming`, no se espera que desaparezca ni se reinicializa el volumen.

## 3. Arrancar manualmente el worker y registrar los dos conectores

En una terminal A, dejar este proceso en primer plano:

```bash
docker compose exec -T -w /opt/kafka-connect/config connect \
  connect-standalone connect-standalone.properties
```

Desde otra terminal, esperar al mensaje `REST resources initialized` del worker
(la exploración de plugins tardó unos 40–55 segundos en esta máquina) y registrar
los conectores **por separado**. La contraseña JDBC se lee mediante el `FileConfigProvider`
configurado en el worker; un `.properties` normal no expande variables shell.

```bash
curl --fail --max-time 20 http://localhost:18083/
curl --fail --max-time 20 http://localhost:18083/connectors
python registrar_conector.py mysql-source              # solo previsualización
python registrar_conector.py mysql-source --aplicar
curl --fail --max-time 20 http://localhost:18083/connectors/mysql-source/status
python registrar_conector.py mongodb-sink --aplicar
curl --fail --max-time 20 http://localhost:18083/connectors
curl --fail --max-time 20 http://localhost:18083/connectors/mongodb-sink/status
```

Se esperan los nombres `mysql-source` y `mongodb-sink`. Para cada conector,
comprobar **`connector.state = RUNNING` y `tasks[0].state = RUNNING`**. El mero
estado del contenedor o un conector `RUNNING` con su task `FAILED` no basta.

**Diferencia comprobada con el PDF:** su comando
`connect-standalone connect-standalone.properties mysql-source.properties mongodb-sink.properties`
produjo un deadlock en esta imagen. Se conserva el
[diagnóstico `jstack`](evidencias/deadlock_cli_2026-10-05.txt): `StandaloneHerder`
y `MemoryConfigBackingStore` bloquean mutuamente la reconfiguración solicitada
por `TableMonitorThread`. Arrancar con solo el source en la CLI también reprodujo
el problema. Un primer registro REST funcionó, pero el deadlock volvió al
[reiniciar y registrar de nuevo](evidencias/deadlock_rest_reinicio_2026-10-05.txt).
El mero cambio a REST no basta.

El patrón de locks observado coincide con el publicado en
[KAFKA-16051](https://issues.apache.org/jira/browse/KAFKA-16051), cuya corrección
upstream figura en Kafka 3.8.0. Es una correspondencia de diagnóstico, no una
prueba de identidad entre builds. Por ello Compose elige el worker **7.8.0**;
el broker sigue en **7.7.1**, y se conservan modo incremental, tabla, topic y
destino. La receta final arranca el worker vacío y registra por REST.
El proyecto de diagnóstico `aabd-kafka-connect-20261005` queda parado con sus
volúmenes conservados. El sufijo `-v78` crea volúmenes nuevos para verificar el
recorrido completo desde tres filas, sin borrar los datos del intento anterior.

Con el worker 7.7.1, en el primer POST del source se observó un timeout de 30 segundos,
con la tarea ya `RUNNING` y los tres mensajes publicados. El registrador consulta
el estado tras ese timeout y solo lo acepta si conector **y tareas** están
`RUNNING`; no afirma haber recibido HTTP 201 ni repite el POST a ciegas. El
registro del sink sí devolvió HTTP 201. Si el source aún no está listo, esperar
y comprobar sus estados antes de registrar el sink.

## 4. Comprobar el topic y MongoDB

```bash
docker compose exec -T kafka kafka-console-consumer \
  --bootstrap-server kafka:29092 --topic iabd-retail_db-categories \
  --from-beginning --max-messages 3 --timeout-ms 10000
docker compose exec -T mongodb mongosh --quiet --eval \
  'db.getSiblingDB("iabd").categories.find().sort({category_id:1}).forEach(printjson)'
python verificar_lab.py --etapa inicial --salida evidencias/inicial_nueva.json
```

El mensaje Kafka tiene `schema` y `payload`, por ejemplo:

```json
{"schema":{"type":"struct","fields":[{"type":"int32","optional":false,"field":"category_id"},{"type":"int32","optional":false,"field":"category_department_id"},{"type":"string","optional":false,"field":"category_name"}],"optional":false,"name":"categories"},"payload":{"category_id":1,"category_department_id":1,"category_name":"Football"}}
```

MongoDB contiene los campos del `payload`, con `_id: {category_id: 1}` en el
primer documento. El verificador contrasta las filas completas y el esquema,
los offsets finales del topic, los documentos y los dos estados REST; además
comprueba que no haya contenedores terminados por OOM. Sale con código distinto
de cero si alguno no coincide y conserva el JSON para diagnosticarlo.

## 5. Prueba dinámica: Streaming

Ejecutar **una sola vez** en este laboratorio:

```bash
docker compose exec -T mysql sh -c \
  'MYSQL_PWD="$MYSQL_PASSWORD" mysql -uiabd retail_db' <<'SQL'
INSERT INTO categories (category_department_id,category_name) VALUES (2, 'Streaming');
SQL
```

Esperar unos segundos (el source consulta cada segundo) y comprobar:

```bash
docker compose exec -T kafka kafka-console-consumer \
  --bootstrap-server kafka:29092 --topic iabd-retail_db-categories \
  --from-beginning --max-messages 4 --timeout-ms 10000
docker compose exec -T mongodb mongosh --quiet --eval \
  'db.getSiblingDB("iabd").categories.find({category_name:"Streaming"}).forEach(printjson)'
python verificar_lab.py --etapa streaming --salida evidencias/streaming_nueva.json
```

Se espera `category_id=4`, `category_department_id=2`, `category_name=Streaming`
en los tres destinos. La consulta MongoDB corrige el paréntesis extra de la
p. 68 (`find({...}))`). Repetir el INSERT crearía otra fila; si ya existe,
consultarla y verificar en lugar de volver a insertarla.

## 6. Verificar la persistencia y parar conservando datos

El source guarda su posición en `/var/lib/kafka-connect/source.offsets`, dentro
del volumen `connect-offsets`. El sink confirma su consumo en Kafka, mediante
el grupo `connect-mongodb-sink`. Para probar un reinicio normal:

1. Enviar SIGTERM **al worker**, que está dentro de un `docker exec`, y esperar
   el cierre de la terminal A:

   ```bash
   docker compose exec -T connect pkill -TERM -f '[o]rg.apache.kafka.connect.cli.ConnectStandalone'
   ```

   Esto permite el cierre normal y flush. El PID 1 del contenedor es `sleep`:
   parar solo el contenedor no sustituye esta comprobación del cierre del worker.
2. Ejecutar `docker compose stop -t 30 connect` y `docker compose up -d connect`.
3. Repetir el arranque manual y el registro secuencial del paso 3. En standalone
   las configuraciones REST de los conectores residen en memoria; hay que
   registrarlas de nuevo, aunque sus offsets sí se conserven.
4. Esperar a que ambas tareas estén `RUNNING` y ejecutar:

```bash
python verificar_lab.py --etapa reinicio --salida evidencias/reinicio_nueva.json
```

El topic debe seguir teniendo **cuatro mensajes**, y MySQL/MongoDB cuatro
registros. Además se comprueba la presencia del archivo de offsets. Es evidencia
de reanudación tras este reinicio, no una prueba de ausencia de duplicados ante
cualquier fallo. Para parar todo al terminar:

```bash
docker compose stop -t 30
```

Este comando conserva contenedores y volúmenes. Para reanudar, usar `up -d`
y arrancar manualmente el worker y registrar de nuevo los conectores. Si el
worker sigue activo al terminar, enviarle primero SIGTERM como arriba y esperar
su cierre antes de parar el contenedor. No se usa `down -v`, `prune` ni borrado de
datos, y no se detiene ningún servicio de otros proyectos.

## Respuestas a las nueve preguntas (p. 69)

1. **¿Para qué sirve `connect-standalone.properties`?** Configura el worker
   común: conexión al broker, serialización JSON, almacenamiento de offsets,
   búsqueda de plugins y API REST. No define la tabla ni la colección.
2. **¿Para qué sirve `mysql-source.properties`?** Instancia `mysql-source`:
   conecta por JDBC a MySQL, selecciona `categories` y publica las filas nuevas
   en Kafka según el `category_id`.
3. **¿Para qué sirve `mongodb-sink.properties`?** Instancia `mongodb-sink`:
   consume el topic indicado y escribe documentos en `iabd.categories`.
4. **¿Qué significa `mode=incrementing`?** Guarda el mayor `category_id`
   emitido y en cada consulta busca IDs mayores. Requiere una columna estrictamente
   creciente y no nula. No detecta cambios ni borrados de filas anteriores;
   no es CDC del binlog. Véase la [documentación oficial de JDBC 10.8](https://docs.confluent.io/kafka-connectors/jdbc/10.8/source-connector/source_config_options.html).
5. **¿Qué topic se crea y qué contiene?** `iabd-retail_db-categories`, resultado
   de `topic.prefix=iabd-retail_db-` más `categories`. Contiene un registro JSON
   con `schema` y `payload` por cada fila detectada, incluidos los tres campos
   SQL y la fila `Streaming` de la prueba.
6. **¿Qué indica `topics` en el sink?** La suscripción de Kafka que debe
   consumir. Es el nombre del topic, no el nombre de la base de datos MongoDB.
7. **¿Qué papel tiene Kafka?** Conserva los registros en un log ordenado por
   partición y desacopla origen y destino. El source produce y el sink consume
   a través de Connect; MongoDB puede recuperar registros conservados en Kafka.
8. **¿Por qué no escribimos producer/consumer en Python?** Los plugins de
   Connect ya implementan lectura JDBC, publicación, consumo y escritura MongoDB,
   además de offsets y ciclo de vida. Se configuran esas implementaciones.
9. **¿Cuál es el recorrido completo?** INSERT en `retail_db.categories` →
   consulta incremental JDBC → registro Connect → `JsonConverter` → topic
   `iabd-retail_db-categories` → task MongoDB sink → conversión a documento BSON
   → upsert en `iabd.categories`.

## Ejecución y límites de la evidencia

Los resultados de la ejecución local de 2026-10-05 se incorporan en
[EXEKUZIOA_2026-10-05.md](EXEKUZIOA_2026-10-05.md), con JSON separados por etapa.
El ejercicio no prueba seguridad de producción, carga sostenida, cambios/borrados
SQL ni entrega en Moodle. Las versiones de imagen y los límites observados se
guardan con la evidencia; los tags MySQL `8.4` y Mongo `8` pueden recibir parches.
