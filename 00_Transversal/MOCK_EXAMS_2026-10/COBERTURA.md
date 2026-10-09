# Cobertura y decisiones

[Índice de simulacros](README.md). Revisión de fuentes locales el 9/10/2026.
Se leyeron guías/enunciados Markdown, bloques de ejercicios de los cuadernos de
Programación y texto extraído de PDFs de ML, Big Data, NiFi, Kafka y reto CNC.
El texto extraído sirve para preparar preguntas; no valida todos los diagramas
ni acredita que cada apartado se haya impartido en clase.

| Bloque | Contenido incluido |
|---|---|
| Reto integrado CNC Guard | objetivos, PERT/Gantt, arquitectura, fuzzy/anomalías, coste y defensa |
| 5071 — Modelos de inteligencia artificial | IA/sistemas expertos, fuzzy, sesgo COMPAS, seguridad, privacidad y ética |
| 5072 — Machine Learning | preprocesado, regresiones, KNN/árbol/SVM/RF/boosting, métricas, CV e Iris |
| 5073 — Programación para IA | 30 test; Python/JSON/Git/uv, NumPy/Pandas/gráficos, pipeline/métricas/Pydantic |
| Big Data e ingeniería de datos | 7 V (incluida Viability), analítica, ETL/ELT, Faker/formatos, Elastic/Kibana/Grok/ILM |
| NiFi y series temporales | FlowFile, ConvertRecord/QueryRecord, provenance, bases/API/medallion, tiempo y alertas |
| Kafka básico y avanzado | particiones/keys/groups/offsets, RF/ISR, medallion, idempotencia y Connect |

## Límites y realismo

- CNC Guard reproduce el contexto de 50 máquinas/1.200 €/h del reto, con red
  PERT y resultados propios nuevos. El reto docente es grupal; el simulacro es
  individual y no sustituye entregables ni defensa real.
- AA combina introducción, sistemas expertos/fuzzy y material reciente de sesgo,
  seguridad y privacidad. El caso normativo es análisis conceptual; no introduce
  calendarios ni clasificación legal cerrada sin contexto.
- ML incluye modelos disponibles hasta Boosting y metodología de validación.
  Iris mantiene la comparación logística/KNN de clase, añadiendo evaluación
  holdout y separación de visualización 2D. No se prometen métricas concretas.
- Programación sigue Moodle 64153 y checklist; CSV nuevo de refrigeración exige
  adaptar rangos, no copiar filtros CNC. No exige API HTTP desplegada ni SMOTE
  en la práctica principal. Los otros temas del curso aparecen en el test.
- Big Data mantiene la lista del PDF: Variety, Volume, Velocity, Value, Veracity,
  **Viability**, Visualization; no sustituye Viability por otra V habitual.
- NiFi incluye el PDF actualizado de series temporales y reto de lecturas
  consecutivas. Diseño NiFi y cálculo Pandas son evidencias distintas.
- Kafka cubre básico y avanzado, grupos independientes, replicas/ISR,
  Bronze/Silver/Gold y Connect. Trazas sintéticas no afirman caídas reales.

Un simulacro es una muestra de evaluación, no un banco exhaustivo: las fuentes
siguen siendo la referencia para detalles de instalación, ejercicios adicionales,
variantes y proyectos. Los rangos/tiempos/costes/umbrales nuevos están declarados;
no se atribuyen al profesor. No se modifica ningún original ni solución previa.
