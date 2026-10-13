# tears_style: pipeline realista Python → Kafka → MySQL → Mongo

Variante completa del ejercicio de Kafka Connect: en vez del volcado
directo MySQL → Mongo, aquí el flujo es el de un pipeline realista con
zona raw, landing verificada, curado con cuarentena y lectura final extra.

```text
generador.py ──15 msgs──▶ tears-raw ──▶ aterrizaje.py ──▶ MySQL raw (14 filas)
   (semilla 7)                          (verifica sha por fila;
                                          PK frena el duplicado)

MySQL raw ──▶ procesador.py ──13──▶ tears-curated ──▶ Connect MongoSink ──▶ Mongo curated
   (relee y                                  │
    revalida)                    1 veneno ──▶ tears-dlq (cuarentena con motivo)

verificar_lab.py: manifiesto(semilla) → raw → MySQL → curated/DLQ → Mongo.
```

## Por qué así (decisiones y su motivo)

- **El sha256 viaja con cada registro** (`modelos.py`): cada etapa lo
  recomputa en lectura. La verificación es contra el manifiesto
  recomputado desde la semilla, no contra ficheros de confianza.
- **Raw es raw**: hasta el veneno aterriza en MySQL. La zona raw conserva
  evidencia; juzgar corresponde al borde de curado. Si el landing
  filtrase, perderías la prueba de la corrupción.
- **El aterrizaje es Python, no JDBC sink**: el landing necesita
  verificación por fila y conteo de duplicados, que es lógica de
  aplicación, no configuración de conector. (Extensión propuesta:
  repetirlo con JDBC sink + `errors.tolerance=all` y comparar.)
- **Connect solo donde brilla**: el sink puro curated → Mongo, sin
  lógica. `_id` estable por `id` + `ReplaceOne` = los replays
  at-least-once son upserts (a prueba de reinicios).
- **1 partición por topic**: orden global determinista para evidencias.
  Con claves y N particiones hay orden por clave, no global (extensión).
- **Puertos solo en 127.0.0.1** (19095/13308/12719/18084) y los mismos
  límites de memoria que `caso5`; credenciales en `.env`/`private/`
  ignorados (ver `preparar_lab.py`).

## Casos cubiertos (y por qué existen)

| # | Caso | Dónde se ve | Por qué |
|---|------|-------------|---------|
| 1 | Camino feliz 13 registros | raw→MySQL→curated→Mongo, hash intacto | el pipeline funciona |
| 2 | Veneno id=99 (sha roto) | aterriza en MySQL, va a DLQ con motivo, nunca a Mongo | la corrupción se conserva como evidencia y se cuarentena |
| 3 | Duplicado id=3 (bytes idénticos) | 15 msgs raw → 14 filas MySQL (`duplicados_pk=1`) | Kafka es at-least-once; el PK es la idempotencia del landing |
| 4 | Evolución de esquema v2 (`bateria`) | ids 11–13, `None` en v1 | los sensores evolucionan; v1 no debe romper |
| 5 | Reprocesado/reinicio | re-ejecutar procesador → mismo curated; Mongo upsert estable | los reinicios no duplican en serving |
| 6 | Linaje | `linaje.sha_origen` en cada doc curado | trazabilidad raw→serving |
| 7 | Lectura extra final | Mongo comparado contra manifiesto, no contra MySQL | cierra el bucle que pide el enunciado |

## Runbook

```bash
cd 07_Kafka/soluzioak/kafka_aurreratua_connect/tears_style
python3 preparar_lab.py
docker compose -p aabd-kafka-tears-style up -d
docker compose -p aabd-kafka-tears-style exec -d connect \
  connect-standalone /opt/kafka-connect/config/connect-standalone.properties \
  /opt/kafka-connect/config/mongo-sink-curated.properties
# El modo REST requiere iniciar antes un worker distributed independiente.
# No ejecutes registrar_conector.py sobre el contenedor inactivo.
U=127.0.0.1:19095
uv run --with kafka-python generador.py --bootstrap $U --manifiesto manifest.json
export MYSQL_PASSWORD=$(grep MYSQL_PASSWORD .env | cut -d= -f2)  # solo entorno local
uv run --with kafka-python --with mysql-connector-python aterrizaje.py --bootstrap $U
uv run --with kafka-python --with mysql-connector-python procesador.py --bootstrap $U
uv run --with pymongo verificar_lab.py --etapa curado --salida evidencias/curado-$(date +%Y%m%dT%H%M%S).json
```

Etapas de evidencia: `aterrizaje` (14 filas + hash OK), `curado`
(13 curated + 1 DLQ + 13 docs Mongo), `reinicio` (reprocesar y reverificar
estabilidad). Ver `EXEKUZIOA.md` para la ejecución fechada.
