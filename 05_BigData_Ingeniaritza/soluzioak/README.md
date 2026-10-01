# Ingeniería de Big Data: recorrido de las soluciones

Este módulo combina respuestas razonadas y laboratorios. Lee el enunciado de
`materialak/` junto a su solución; los ejemplos de organizaciones y arquitecturas
son propuestas docentes, no auditorías de esas organizaciones.

| Bloque | Enunciado | Solución y forma de comprobarla |
|---|---|---|
| 01 · Introducción | [Ejercicios 01_01](../materialak/Ariketak_01_01_big_data_sarrera.md) | [Respuestas sobre 7V, Spotify y roles](01_Big_Data_Sarrera/Ariketak_01_01_Big_Data_Sarrera_Ebazpena.md). Compara cada pregunta con su respuesta y justifica la V o el rol elegido; puede haber alternativas razonadas. |
| 02 · Ingeniería | [Ejercicios 01_02](../materialak/Ariketak_01_02_datuen_ingeniaritza.md) | [Ciclo de vida, ETL/ELT, Lakehouse y formatos](02_Datuen_Ingeniaritza/Ariketak_01_02_Datuen_Ingeniaritza_Ebazpena.md). Sigue el dato desde su origen hasta el consumo y diferencia transformación y almacenamiento. |
| 02 · Faker | Mismo enunciado, apartados 12–15 | [Guía de ejecución](02_Datuen_Ingeniaritza/README.md): genera CSV/JSON y comprueba filas, columnas y reproducibilidad. |
| 03 · Elastic | [PDF Elastic Stack](../materialak/02_elastic_stack.pdf) | [Guía de P1–P14](03_Elastic_Stack/README.md), [solución](03_Elastic_Stack/Ebazpena_Elastic_Praktikak.md) y [entrega de Kibana](03_Elastic_Stack/dashboards/README.md). |

Las respuestas escritas no necesitan servicios en marcha. Faker tiene su propio
`pyproject.toml` y `uv.lock`; ejecuta sus comandos dentro de esa carpeta. Elastic
necesita un laboratorio independiente: sus scripts escriben datos y recrean
índices. Un archivo de resultados existente acredita contenido guardado; el
registro fechado indica qué se verificó y las limitaciones de esa comprobación.
