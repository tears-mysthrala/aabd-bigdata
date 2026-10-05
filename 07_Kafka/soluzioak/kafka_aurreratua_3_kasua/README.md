# Kafka avanzado · caso 3: Bronze / Silver / Gold

Fuente: [PDF docente, pp. 18–37](../../materialak/01_04_ApacheKafka_aurreratua.pdf). Los seis scripts solicitados están implementados. **Kafka/MongoDB verificados con fixture sintética y con respuestas reales de Open-Meteo el 2026-10-02**. La API original el-tiempo.net devolvió HTTP 405; Open-Meteo es una variante explícita de proveedor. El caso de NiFi AEMET es otra práctica.

## Preparación

Desde esta carpeta:

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
# Proyecto dedicado: no conecta al broker compartido de infra/.
docker compose -p aabd-kafka3-lab up -d
```

Compose usa tres brokers Kafka 3.7.0 en modo ZooKeeper, como el laboratorio del caso 2. Solo publica puertos loopback 29092–29094 y MongoDB 27027. Usa una partición por topic y RF=2: basta para ilustrar los tres grupos independientes y mantiene el orden de las medidas de un municipio. El PDF no fija otra cantidad para estos topics. No usa credenciales ni servicios personales; no exponer este laboratorio a otras redes.

## Reproducir la prueba completa

En un laboratorio **nuevo**, con topics y colección vacíos:

```bash
.venv/bin/python -m pytest -q test_pipeline.py
.venv/bin/python egiaztatu_laborategia.py --output /tmp/kafka3-evidencias-nuevas
# Cuando termines, detén solo este proyecto:
docker compose -p aabd-kafka3-lab down
```

El verificador crea los tres topics, genera 20 payloads sintéticos, ejecuta los seis scripts, comprueba los mensajes y los documentos y lee los offsets de los tres grupos. Si el laboratorio ya tiene estos topics o documentos, aborta sin borrar datos: usa otro laboratorio/carpeta de salida nueva. El verificador no arranca ni elimina contenedores. Los datos del lab no se usan como observaciones reales de Elche.

[Resultado observado](evidencias/resultado.json): **20 Bronze = 20 Silver = 20 JSONL = 20 documentos MongoDB**. Cada ruta Gold emite dos agregaciones (lotes de diez): medias de temperatura 14,5 y 24,5; humedad 44,5 y 54,5. Los grupos `iabd-3kasua-fitxategia`, `iabd-3kasua-mongo` e `iabd-3kasua-gold` confirman offset 20 independientemente. MongoDB usa upsert por identidad del mensaje Silver, por lo que el consumer independiente no duplica los documentos ya escritos en la primera parte.

Doce pruebas verifican conversión sin alterar Bronze, medidas inválidas, unidades y hora del modelo Open-Meteo, cálculo Gold, consultas repetidas, lote incompleto y confirmación del offset exacto sin saltarse mensajes del mismo poll. Los tres topics tenían RF=2 e ISR de dos brokers. [Registro](evidencias/topologia.txt).

## Variante Open-Meteo: fuente remota verificada

[Open-Meteo](https://open-meteo.com/en/docs) ofrece temperatura a 2 m y humedad relativa, sin clave para este uso educativo no comercial. Sus condiciones actuales proceden de modelos con pasos de quince minutos, no de nuevas observaciones de una estación por cada GET. [Condiciones y límites](https://open-meteo.com/en/terms): atribución CC BY 4.0 y límites del servicio gratuito. Fuente de los datos de esta variante: **Open-Meteo**.

En las tres terminales de la primera parte, usa:

```bash
.venv/bin/python prozesatu_urrea.py --idle-timeout 0
.venv/bin/python prozesatu_zilarra.py --city 'Elche/Elx' --idle-timeout 0
.venv/bin/python producer_brontzea.py --provider open-meteo
```

El producer consulta `https://api.open-meteo.com/v1/forecast`, coordenadas 38.26218, −0.70107 (Elche/Elx), `current=temperature_2m,relative_humidity_2m`, `temperature_unit=celsius` y `timezone=UTC`. Conserva toda la respuesta en Bronze. El intervalo por defecto es **900 segundos**; `--latitude`, `--longitude` y `--city` permiten otra ubicación. Si cambias la ciudad, indica también el mismo `--city` a Silver: la API devuelve coordenadas y el nombre procede de esta configuración.

Silver valida °C, %, humedad 0–100, medidas finitas y UTC. `data` es la hora de ingesta; `source_time` es la hora del modelo y `source_interval_seconds` su intervalo. Gold sigue agregando diez mensajes como pide el ejercicio, pero incorpora `unique_source_times`: diez consultas del mismo instante no equivalen a diez observaciones independientes.

Para repetir la prueba remota en un **laboratorio nuevo**, sustituye el verificador sintético por:

```bash
.venv/bin/python egiaztatu_laborategia.py --source open-meteo --output /tmp/kafka3-openmeteo-nuevas
```

La prueba acotada acelera veinte GET a intervalos de 0,5 s para comprobar el transporte, dentro de los límites de peticiones. [Resultado real](evidencias_open_meteo_final/resultado.json): **20 Bronze = 20 Silver = 20 JSONL = 20 documentos MongoDB**, dos lotes Gold por ruta y tres offsets en 20. Los veinte mensajes corresponden a **un instante del modelo**; Gold lo registra. La respuesta observada da 20,6 °C y 88 % de humedad, valores de esa ejecución y ubicación. [Bronze original](evidencias_open_meteo_final/bronze_live.jsonl), [Silver](evidencias_open_meteo_final/silver_datuak.jsonl), [topología](evidencias_open_meteo_final/topologia.txt).

Esta variante verifica una API remota real y el pipeline completo. El proveedor original sigue pendiente de responder; si la entrega exige exactamente el-tiempo.net, debe autorizarse académicamente el cambio. No hay fallback silencioso ni equivalencia declarada con observaciones AEMET.

## Primera parte: API → Bronze → Silver/Mongo → Gold

Crear los topics si no usas el verificador:

```bash
for topic in iabd-aemet-brontzea iabd-aemet-zilarra iabd-aemet-urrea; do
  docker compose -p aabd-kafka3-lab exec -T kafka1 /opt/kafka/bin/kafka-topics.sh \
    --bootstrap-server kafka1:9092 --create --topic "$topic" --partitions 1 --replication-factor 2
done
```

Abrir tres terminales, en este orden:

```bash
.venv/bin/python prozesatu_urrea.py --idle-timeout 0
.venv/bin/python prozesatu_zilarra.py --idle-timeout 0
.venv/bin/python producer_brontzea.py
```

El producer consulta el JSON cada diez segundos. `raise_for_status()` impide enviar HTML de un error HTTP como meteorología. `--fixture evidencias/bronze_fixture.jsonl --interval 0 --max 20` reproduce entradas sintéticas sin consultar la API. Para una ejecución acotada, `--max 20` en cada consumer; los Gold requieren múltiplos de diez. `--bootstrap` y `--mongo-uri` permiten indicar otros endpoints autorizados. Los defaults apuntan al laboratorio dedicado.

Silver acepta el contrato mostrado en el PDF (`municipio.NOMBRE`, `temperatura_actual`, `humedad`) y el contrato Open-Meteo documentado arriba. Produce fecha UTC, ciudad y medidas float. La humedad debe estar en 0–100 y ambas medidas ser finitas. **El contrato del proveedor original necesita confirmarse con un payload real cuando vuelva su API**.

## Segunda parte: tres consumers Silver independientes

La variante del productor Silver se ejecuta con `--without-mongo`; MongoDB queda a cargo de su consumer. No ejecutar a la vez dos consumidores Gold del mismo ejercicio si esperas solo una serie de agregaciones.

```bash
.venv/bin/python kontsumitzaileZilarraFitxategia.py --idle-timeout 0
.venv/bin/python kontsumitzaileZilarraMongoDB.py --idle-timeout 0
.venv/bin/python kontsumitzaileZilarra_EkoizleaUrrea.py --idle-timeout 0
.venv/bin/python prozesatu_zilarra.py --without-mongo --idle-timeout 0
.venv/bin/python producer_brontzea.py
```

Los grupos nuevos leen desde el principio; un grupo existente reanuda desde su offset confirmado. El JSONL se abre en append, y puede duplicar una línea si el proceso cae tras escribirla pero antes del commit. Kafka send, MongoDB/JSONL y commit no son una transacción: la garantía es **al menos una vez**, con duplicados posibles, también en Silver/Gold tras un fallo. MongoDB evita repetir el mismo ID Kafka; no deduplica observaciones distintas con el mismo valor.

Gold confirma offsets después de publicar un lote completo de diez. Un lote incompleto se relee al reiniciar y no se pierde por commit anticipado. El ejercicio trabaja con un municipio; un lote con ciudades mezcladas se rechaza. No se afirma tolerancia a fallos o exactly-once más allá de estas pruebas.

## Ocho respuestas de reflexión (p. 36)

1. **Bronze/Silver/Gold:** Bronze conserva el JSON completo; Silver tipa y selecciona medidas; Gold agrega diez registros. La fixture observada produce medias 14,5 y 24,5, calculadas desde sus entradas.
2. **Topic entre capas:** desacopla etapas, conserva mensajes durante retention y permite relecturas/grupos independientes. Retention no se ha ensayado durante varios días.
3. **Silver es consumer y producer:** lee Bronze, transforma y publica Silver; en la primera parte escribe también MongoDB.
4. **Conservar Bronze:** permite auditar el origen y reprocesar con otra transformación sin repetir la consulta, mientras su retention lo conserve.
5. **Parar/reiniciar:** el mismo grupo continúa desde el offset confirmado. El estado parcial Gold vive en memoria, por eso sus offsets no se confirman hasta completar el lote; puede releerse. Un fallo entre efectos y commit puede duplicar datos.
6. **group_id:** identifica el progreso y el conjunto de consumidores que se reparten las particiones de un topic.
7. **Tres IDs distintos:** cada destino recibe todas las medidas. En la prueba los tres grupos llegaron al offset 20. Con un único grupo compartirían particiones: en nuestro topic de una partición solo uno tendría asignación, dejando destinos sin todas las medidas.
8. **Scripts independientes:** facilita observar, probar y reiniciar cada etapa. Esa independencia requiere gestionar offsets, reintentos y duplicados; no ofrece atomicidad entre destinos.
