# CNC Guard · Contrato UX y asignación de trabajo (propuesta 2026-10-18)

> **CORRECCIÓN DE ALCANCE (19/10/2026): STREAMLIT OBLIGATORIO PARA LA UI.** Este PR contiene wireframes e infografías de referencia; el frontend de entrega se construirá con Streamlit (vistas nativas + Plotly, `st.session_state` y consultas parametrizadas a Elastic/DuckDB). El HTML anterior es una herramienta de revisión UX, no la aplicación final. El prototipo Streamlit completo está disponible como ZIP adjunto en la conversación de ChatGPT, sin conexión a producción. Se documentarán pruebas de arranque y pantallas una vez instalado Streamlit. Kibana solo tendrá evidencias mínimas donde la rúbrica lo obligue.\n\n**Estado: diseño para revisión, no código implantado.** Fuentes: `Erronka1_ikaslearen_errubrika.xlsx`, historia del reto y [backlog principal del equipo](https://github.com/AABD-Ethazi-2627/T2-erronka1/issues). El proyecto real se evalúa en el repositorio del equipo; las issues creadas en este repositorio personal son una capa de coordinación para el estudio.

## Pantallas

- [CENTRO DE OPERACIONES](pantallas/00-overview.svg) — 50 CNC · MAPA INTERACTIVO
- [DIAGNÓSTICO DE MÁQUINA](pantallas/01-machine.svg) — SENSORES · RF / IF · DECISIÓN
- [CALIDAD DE MODELOS](pantallas/02-ml.svg) — TP / FP / FN / TN · UMBRAL
- [PLANIFICADOR DE MANTENIMIENTO](pantallas/03-maintenance.svg) — SÁBADO / DOMINGO · PRIORIDADES
- [HISTÓRICO Y COSTES](pantallas/04-analytics.svg) — DUCKDB · COSTE ESCENARIOS
- [DATOS Y TRAZABILIDAD](pantallas/05-pipeline.svg) — KAFKA · NIFI · FASTAPI · ELASTIC

## Responsabilidades

- [ML Y COORDINACIÓN](infografias/01-ml-coordinacion.svg) — @tears-mysthrala
- [INFRAESTRUCTURA](infografias/02-infraestructura.svg) — @petiteiker
- [DESARROLLO E INTEGRACIÓN](infografias/03-desarrollo.svg) — @Niistal
- [DISEÑO Y UX / BI](infografias/04-diseno.svg) — @Angiecrizu
- [REVISIÓN DE EQUIPO](infografias/05-equipo.svg) — revisión cruzada

## Política de alcance

- **Nivel 10:** entrenamiento RF/IF reproducible, TP/FP/FN/TN y errores, NiFi/Kafka, streaming/recuperación, Kibana exportable, privacidad y seguridad, datos verificables.
- **Extra alcanzable:** mapa 50 CNC mediante catálogo versionado, triaje de mantenimiento, tiempo de dato, agenda sencilla, costes hipotéticos.
- **Fuera del MVP:** vida útil restante física, anticipación validada 10 min, control de parada, OPC UA real, gemelo digital completo, optimizador industrial de agenda, HA real y cache KV sin prueba de cuello de botella.
- Un documento `CNC-xxx` de estado por máquina puede facilitar vista operativa; no reemplaza histórico inmutable con `event_id`.
- La etiqueta `machine_failure` de AI4I **no** etiqueta mantenimiento urgente ni tiempo restante hasta avería.
- No usar `cnc_10M` como datos de origen del reto: es un laboratorio previo independiente.
- Coste 1200 €/h es supuesto académico para parada productiva, no ahorro medido.
- KPI/OEE/RUL no rellenables sin las fuentes correspondientes.

## Modelo de pruebas

Un criterio no se da por completado sin: código versionado, comando, dataset/sha, resultado, interpretación, limitaciones y revisión entre pares. No se considera que estas imágenes demuestren cumplimiento de la rúbrica.
