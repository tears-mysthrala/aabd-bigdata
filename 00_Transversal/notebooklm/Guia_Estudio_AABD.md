# Guía de Estudio: Inteligencia Artificial, Big Data y Gestión de Proyectos

Esta guía de estudio ha sido diseñada para sintetizar los conceptos fundamentales, las herramientas técnicas y las metodologías de trabajo en equipo descritas en los materiales del programa de Inteligencia Artificial y Big Data (AABD).

---

## 1. Conceptos Clave

### Gestión de Proyectos y Trabajo en Equipo
El éxito de un proyecto tecnológico no solo depende de la técnica, sino de una organización estructurada. Según el "Anexo 1" del proyecto CNC Guard, los equipos deben definir claramente sus roles y compromisos:

*   **Roles en el Equipo:**
    *   **Coordinador:** Modera, asegura el seguimiento de los pasos y anima a los miembros.
    *   **Secretario:** Escribe y recopila documentos, gestiona archivos en la nube y supervisa el uso correcto del lenguaje.
    *   **Portavoz:** Informa sobre las decisiones tomadas y comunica con los docentes.
    *   **Ayudantes:** Controlan el tono de voz y gestionan el tiempo de trabajo.
*   **Objetivos Grupales:** Fomentar el aprendizaje colaborativo, el respeto a las opiniones ajenas y la entrega puntual de trabajos bajo una planificación de costes y tiempos.

### Fundamentos de DataFlow y Apache NiFi
El procesamiento de datos en entornos de Big Data se divide en dos estados principales: **dato en reposo** (*at rest*), como archivos o tablas en un data lake, y **dato en movimiento** (*in motion*), donde el flujo es continuo (sensores, transacciones).

*   **Apache NiFi:** Es un proyecto de Apache (originalmente desarrollado por la NSA) diseñado para la **ingestión y transformación de datos**.
*   **Filosofía:** Se basa en la programación de flujo de datos (*dataflow*) mediante una interfaz gráfica de "arrastrar y soltar" (no-code).
*   **Arquitectura:** Las aplicaciones se definen como **Grafos Dirigidos Acíclicos (DAG)**, donde los mensajes se intercambian a través de conexiones predefinidas.

### Arquitectura de Medallón (Medallion Architecture)
Para organizar el ciclo de vida del dato en un pipeline, se utilizan capas de calidad:
1.  **Bronze (Bronce):** Datos crudos/originales (*gordinak*). Se guardan tal cual llegan de la fuente sin transformaciones.
2.  **Silver (Plata):** Datos limpios y normalizados. Se aplican esquemas unificados y controles de calidad.
3.  **Gold (Oro):** Datos agregados y optimizados. Listos para el análisis, a menudo en formatos columnares como Parquet.

---

## 2. Cuestionario de Práctica (Respuesta Corta)

**Pregunta 1: ¿Cuál es la principal diferencia entre el dato "en reposo" y el dato "en movimiento"?**
*Respuesta:* El dato en reposo se refiere a información almacenada de forma estática (archivos, lagos de datos), mientras que el dato en movimiento se genera y procesa en tiempo real (streaming), como clics en una web o señales de sensores.

**Pregunta 2: En Apache NiFi, ¿qué es un FlowFile?**
*Respuesta:* Es la unidad básica de datos que se mueve a través del sistema, compuesta por el contenido del dato y sus atributos asociados.

**Pregunta 3: ¿Por qué es preferible usar `QueryRecord` en lugar de `SplitRecord` para filtrar grandes volúmenes de datos?**
*Respuesta:* `SplitRecord` crea un FlowFile por cada fila, lo que genera una gran carga en la memoria. `QueryRecord` aplica filtros SQL internamente (usando el motor Apache Calcite) sobre el archivo completo, reduciendo el número de FlowFiles y mejorando el rendimiento.

**Pregunta 4: ¿Cuáles son los cuatro roles principales en un pipeline de datos moderno?**
*Respuesta:* Ingestión (ej. NiFi, Kafka), Procesamiento (ej. Spark Streaming), Windowing (gestión del tiempo) y Orquestación (ej. Airflow).

**Pregunta 5: ¿Qué permite el "linaje" (*lineage*) en Apache NiFi?**
*Respuesta:* Permite realizar el seguimiento del recorrido y las transformaciones de un dato a lo largo de todo el flujo de procesamiento.

---

## 3. Temas de Ensayo para Profundización

### Ensayo A: La transición de Bronze a Gold en la Ingeniería de Datos
Analice la importancia de implementar una Arquitectura de Medallón en un sistema de Big Data. ¿Por qué es crítico mantener la capa *Bronze* intacta? Explique cómo herramientas como Apache NiFi facilitan el paso a la capa *Silver* mediante procesadores como `EvaluateJSONPath` y `AttributesToJSON`, y cómo se llega a la capa *Gold* mediante agregaciones SQL en `QueryRecord`.

### Ensayo B: Eficiencia y Escalabilidad en la Ingestión de Datos
Compare el uso de procesadores "clásicos" de NiFi (como `SplitText` y `PutMongo`) frente al uso de procesadores basados en registros (*record-oriented*) como `PutMongoRecord`. Discuta el impacto en la complejidad del diseño del flujo y en el consumo de recursos de hardware del sistema cuando se manejan conjuntos de datos masivos.

---

## 4. Glosario de Términos Importantes

| Término | Definición |
| :--- | :--- |
| **DAG (Directed Acyclic Graph)** | Estructura lógica que representa el flujo de datos sin ciclos cerrados. |
| **Apache Calcite** | Motor utilizado por NiFi para permitir consultas SQL sobre el contenido de los FlowFiles. |
| **Parquet** | Formato de archivo optimizado para almacenamiento columnar, utilizado habitualmente en la capa *Gold*. |
| **JSONTreeReader** | Servicio de controlador en NiFi que permite interpretar datos en formato JSON para procesarlos como registros. |
| **Docker Compose** | Herramienta utilizada para levantar contenedores (como MariaDB o MongoDB) necesarios para las prácticas de DataFlow. |
| **FlowFile Attribute** | Metadatos asociados a un FlowFile que pueden ser usados para el enrutamiento o filtrado mediante procesadores como `RouteOnAttribute`. |
| **Dual-Storage** | Estrategia de almacenamiento que combina un data lake (para histórico/batch) y bases de datos como MongoDB (para consultas rápidas). |
| **ETHAZI** | Metodología de aprendizaje basada en retos aplicada en los materiales de programación y Big Data. |

---
**Nota para el estudiante:** Se recomienda revisar los cuadernos Jupyter (`.ipynb`) y scripts de Python (`.py`) proporcionados en las carpetas de materiales para practicar la implementación técnica de estos conceptos.