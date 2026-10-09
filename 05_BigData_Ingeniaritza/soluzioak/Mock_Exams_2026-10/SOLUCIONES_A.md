# Soluciones y rúbrica — Big Data e ingeniería de datos, simulacro A

[Volver al examen](../../materialak/Mock_Exams_2026-10/EXAMEN_A.md).
Corrección propuesta, no baremo docente. Se admiten alternativas coherentes con
los requisitos. Concede crédito parcial por razonamiento correcto aunque haya
un error aritmético posterior; no cuentes dos veces el mismo mérito.
Los valores calculados son respuestas de casos sintéticos, no resultados de planta.

## 1 — 2 puntos

Variety=audio/JSON/logs; Volume=millones; Velocity=continuidad;
Veracity=edades incorrectas; Value=recomendaciones útiles;
Visualization=dashboard; **Viability=viabilidad coste/beneficio**. Esta es la
lista del PDF: no sustituir Viability por Variability sin explicar otra taxonomía.
Analítica: descriptiva/diagnóstica/predictiva/prescriptiva. OLTP registra operaciones
con baja latencia y consistencia; OLAP agrega histórico. 1/0.5/0.5.

## 2 — 2 puntos

500/5=**100 lecturas/s**; 8.640.000/día; 864.000.000 bytes=**0.864 GB/día**.
Generación sensor; ingesta NiFi/Kafka; almacenamiento bruto; transformación de
unidades/calidad; consumo dashboard/ML. Lake conserva heterogeneidad; Warehouse
para analítica estructurada; Lakehouse si precisa gestión y analítica sobre lake;
cache para estado reciente, sin sustituir persistencia. HDD histórico barato,
SSD acceso frecuente, RAM temporal; tecnología física no es abstracción lógica.
ETL transforma antes de destino; ELT carga original y transforma después.
No imponer «Big Data siempre ELT». 0.5/0.5/0.75/0.25.

## 3 — 2 puntos

v5 rechazado por precio; v4 huérfano en cuarentena, no atribuir ciudad.
Join válido many-to-one contra IDs de clientes únicos; strip ciudad.
Eibar: v1=40 y v3=45 → **85 €**. Conservar original y motivo de rechazos.
CSV hoja; JSON objeto; JSONL eventos; Parquet analítica columnar con proyección.
Faker.seed(42), Faker('es_ES'); IDs 1..100; edad con RNG explícitamente sembrado
si se usa random fuera de Faker. Verificar conteo, rango, columnas e IDs únicos.
Seed reproduce bajo mismas versiones, llamadas y orden; no garantiza realismo,
privacidad ni salida idéntica entre versiones. Para escala, escritura por lotes
JSONL/Parquet, no una lista enorme. Puntos 1/0.5/0.5.

## 4 — 2.5 puntos

Mapping nombre=text (opcional subcampo keyword), categoria=keyword,
precio=float/scaled_float según precisión monetaria, id=keyword.
Consulta `{"query":{"match":{"nombre":"taladro"}}}` → p1,p2.
Consulta `{"query":{"bool":{"filter":[{"term":{"categoria":"Herramientas"}},
{"range":{"precio":{"gte":100}}}]}}}` → p1. Si categoria es multifield,
usar categoria.keyword. El texto tokenizado no sustituye al keyword exacto.
Para ventas: ciudad keyword, timestamp date, importe numérico definido como
ingreso (no precio unitario). terms ciudad + sum importe; date_histogram mensual
+ sum importe. Data view patrón correcto y campo temporal; Lens dimensiones y
métrica; filtros y rango coherentes; comprobar documentos en Discover.
Shard primario distribuye documentos; réplica copia para disponibilidad/lectura,
no duplica ventas al consultar el índice. Dashboard vacío puede ser rango,
filtro, data view o campo temporal incorrecto. 0.5/0.75/0.75/0.5.

## 5 — 1.5 puntos

Filebeat recoge; Logstash parsea/transforma; Elasticsearch indexa/busca;
Kibana consulta/visualiza. Grok:
`%{TIMESTAMP_ISO8601:ts} %{LOGLEVEL:nivel} maquina=%{WORD:maquina} temp=%{NUMBER:temperatura:float}`.
Filtro date sobre ts con ISO8601 a @timestamp; gestionar _grokparsefailure
mediante cuarentena/log de error, sin enviar como éxito silencioso.
ILM: hot inicial; warm min_age=7d; cold min_age=30d; delete min_age=90d.
Definir acciones compatibles con recursos y requisitos del caso.
Comprobar política, index template y asociación efectiva; si hay rollover,
configurar alias/data stream apropiado y entender que min_age se referencia al
rollover para índices rotados. No asumir que crear una política la aplica a todos
los índices existentes. 0.5 por apartado.
