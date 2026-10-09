# Simulacro A — Big Data e ingeniería de datos

Elaboración propia, 9 de octubre de 2026. Basado en la materia local disponible;
no es un examen oficial ni una predicción de preguntas del profesorado.
Duración propuesta: **120 minutos**. Nota máxima: **10 puntos**.
Los tiempos, reparto de puntos y condiciones son de autoestudio, salvo el formato
3 + 7 de Programación documentado en su guía docente.

## Condiciones y entrega

Resuelve primero sin abrir la [solución y rúbrica](../../soluzioak/Mock_Exams_2026-10/SOLUCIONES_A.md).
Teoría sin apuntes; práctica con copias locales de los apuntes, sin Internet ni IA.
Calculadora básica permitida en cálculos. Entrega respuestas razonadas y, donde
se pida código, notebook o script con salidas y explicación. No basta nombrar una
herramienta: justifica su elección. Los casos y números nuevos son sintéticos.
No necesitas levantar servicios para los apartados de diseño o traza.

## Materia de referencia

- [Ariketak_01_01_big_data_sarrera.md](../Ariketak_01_01_big_data_sarrera.md)
- [Ariketak_01_02_datuen_ingeniaritza.md](../Ariketak_01_02_datuen_ingeniaritza.md)
- [01_01_big_data_sarrera.pdf](../01_01_big_data_sarrera.pdf)
- [02_elastic_stack.pdf](../02_elastic_stack.pdf)

## 1. Fundamentos aplicados (2 puntos; 20 min)

Una plataforma musical ingiere audio, JSON y logs; millones de eventos; llegadas
continuas; edades imposibles; recomendaciones; dashboard; un piloto cuyo coste
supera el valor generado. Asocia las siete situaciones a las **7 V del material**
y justifica (1). Clasifica «ventas de ayer», «causa de caída», «predicción de
ventas» y «recomendación de stock» por tipo de analítica (0.5). Distingue OLTP
para compra de OLAP para histórico (0.5).

## 2. Diseño de Smart Factory (2 puntos; 20 min)

500 sensores emiten una lectura de 100 bytes cada 5 s, todo el día. Calcula
lecturas/s y GB/día decimales sin overhead (0.5). Explica las cinco fases del
ciclo de datos con un ejemplo (0.5). Elige almacenamiento de originales,
analítica histórica y cache operacional, distinguiendo HDD/SSD/RAM de
Lake/Warehouse/Lakehouse/Cache (0.75). Compara ETL y ELT para este caso (0.25).

## 3. Transformación y formatos (2 puntos; 25 min)

Tablas sintéticas:

| cliente_id | ciudad |
|---|---|
| 1 | `Eibar ` |
| 2 | `Bilbao` |
| 3 | `Eibar` |

| venta_id | cliente_id | precio | unidades |
|---|---:|---:|---:|
| v1 | 1 | 20 | 2 |
| v2 | 2 | 10 | 1 |
| v3 | 3 | 15 | 3 |
| v4 | 9 | 50 | 1 |
| v5 | 1 | -5 | 2 |

Describe/codifica ETL: validar precios no negativos, limpiar espacios, join
controlando huérfanos y calcular ingresos Eibar (1). Elige CSV/JSON/JSONL/Parquet
para hoja de cálculo, objeto de API, logs continuos y lectura de dos columnas
de 500 millones de filas (0.5). Diseña 100 clientes Faker('es_ES'), edades 18–80,
IDs únicos, semilla 42; explica validación, alcance de seed y escalado sin cargar
todo JSON en RAM (0.5).

## 4. Elasticsearch y Kibana (2.5 puntos; 35 min)

Documentos:
`{id:'p1', nombre:'Taladro profesional', categoria:'Herramientas', precio:120}`,
`{id:'p2', nombre:'Taladro compacto', categoria:'Herramientas', precio:80}`,
`{id:'p3', nombre:'Cable USB', categoria:'Accesorios', precio:10}`.
Propón mapping de nombre/categoria/precio (0.5), consulta full-text por
«taladro» y filtro exacto Herramientas con precio>=100 (0.75). Diseña agregación
de ingresos por ciudad y serie mensual para ventas con timestamp/importe,
describiendo data view, Lens y filtro temporal (0.75). Explica shards primarios,
réplicas y por qué un dashboard vacío no prueba ausencia de documentos (0.5).

## 5. Logs y ciclo de vida (1.5 puntos; 20 min)

Log sintético: `2026-10-09T08:00:00Z INFO maquina=C01 temp=42.5`.
Describe Filebeat → Logstash → Elasticsearch → Kibana (0.5). Escribe patrón
Grok con nombres de campos y conversión fecha/número; ruta para fallo de parsing
(0.5). Propón política ILM conceptual hot hasta 7 días / warm de 7 a 30 / cold de 30 a 90 / delete desde
90 días y explica qué comprobar para aplicarla a índices nuevos (0.5).
No ejecutes borrados; los días son requisitos ficticios, no política de clase.
