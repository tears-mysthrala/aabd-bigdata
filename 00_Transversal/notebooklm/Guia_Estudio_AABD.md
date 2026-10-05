# Guía de Estudio: Inteligencia Artificial y Big Data (AABD)

Esta guía de estudio sintetiza los materiales y conceptos fundamentales del programa de Inteligencia Artificial y Big Data (AABD), abarcando desde la organización del trabajo en equipo hasta la ingeniería de datos avanzada con Apache NiFi y la arquitectura de capas.

---

## 1. Organización y Planificación del Trabajo (ETHAZI)

El éxito en proyectos complejos de Big Data requiere una estructura organizativa clara y compromisos individuales definidos. Según los protocolos establecidos (Anexo 1 - Contrato), la gestión de equipos se divide en roles específicos:

### Roles y Responsabilidades del Equipo

| Rol | Responsabilidades Principales |
| :--- | :--- |
| **Coordinador/a** | Moderar, asegurar el seguimiento de los pasos de la estructura y animar a los miembros. |
| **Portavoz** | Comunicar las decisiones tomadas y actuar como enlace con el profesorado. |
| **Secretario/a** | Redactar y recoger documentos del grupo, gestionar el Classroom/Drive y supervisar el uso del lenguaje. |
| **Ayudantes** | Controlar el tono de voz (Ayudante 1) y gestionar los tiempos (Ayudante 2). |

### Objetivos y Compromisos
El modelo de trabajo fomenta objetivos tanto grupales (aprender a trabajar en equipo, ayudarse mutuamente) como personales (ser positivo, no distraerse, solicitar ayuda ante dudas y mantener el material ordenado).

---

## 2. Fundamentos de Big Data y DataFlow

### El Dato: En Reposo vs. En Movimiento
*   **Dato en Reposo (*at rest*):** Se refiere a sistemas tradicionales de Big Data donde la información reside en archivos, tablas o lagos de datos (*data lakes*).
*   **Dato en Movimiento (*in motion*):** Enfoque de *streaming* donde los datos se generan y procesan continuamente (sensores, transacciones, *click-streams*). El módulo de Apache NiFi se centra en esta fase de movimiento y transformación.

### Apache NiFi: Definición y Filosofía
Apache NiFi es un proyecto desarrollado originalmente por la NSA para la **ingestión y transformación de datos**.
*   **Programación DataFlow:** Basada en Grafos Dirigidos Acíclicos (DAG).
*   **Filosofía No-Code:** Utiliza una interfaz de "arrastrar y soltar" (drag-and-drop) para definir *pipelines* sin necesidad de escribir líneas de código.
*   **Trazabilidad:** Permite el seguimiento del linaje de los datos.

---

## 3. Conceptos Técnicos de Apache NiFi

Para dominar la herramienta, es esencial comprender sus componentes básicos y estrategias de optimización:

*   **FlowFile (FF):** El objeto central que se mueve a través del sistema. Contiene el contenido (los datos) y los atributos (metadatos).
*   **Procesadores:** Unidades que realizan operaciones (ej. `GetFile`, `PutFile`, `ConvertRecord`). Existen más de 300 conectores disponibles.
*   **Colas (Queues):** Conexiones entre procesadores donde los FlowFiles esperan a ser procesados.
*   **Apache Calcite:** Motor utilizado por NiFi para ejecutar consultas SQL sobre el contenido de los FlowFiles (ej. en el procesador `QueryRecord`).

### Optimización de Rendimiento
Un error común es el uso excesivo de `SplitRecord`, que crea un FlowFile por cada fila de un CSV, sobrecargando la memoria. Las soluciones incluyen:
1.  **Agrupación:** Dividir en grupos de filas (ej. 10 filas por FF).
2.  **Filtrado Directo:** Conectar `GetFile` directamente a `QueryRecord` para que el motor Calcite filtre internamente sin fragmentar el archivo.

---

## 4. Arquitectura de Medallón (Bronze, Silver, Gold)

El procesamiento avanzado de datos en NiFi suele seguir la arquitectura de capas para garantizar la calidad y disponibilidad:

1.  **Capa BRONZE (Datos Brutos):**
    *   **Estado:** Datos originales en su formato de origen.
    *   **Acción:** Capturar y guardar sin transformar.
    *   **Destino:** Almacenamiento histórico (Data Lake).

2.  **Capa SILVER (Datos Limpios/Normalizados):**
    *   **Estado:** Datos con esquema unificado y controles de calidad aplicados.
    *   **Herramientas:** `EvaluateJSONPath` y `AttributesToJSON` para extraer campos de interés.
    *   **Destino:** Almacenamiento operativo (ej. MongoDB) y archivos de sistema.

3.  **Capa GOLD (Datos Agregados/Optimizados):**
    *   **Estado:** Datos listos para analítica avanzada.
    *   **Herramientas:** `MergeContent` para agrupar mensajes y `QueryRecord` para realizar agregaciones SQL (promedios, máximos).
    *   **Formato:** Uso preferente de **Parquet** (formato orientado a columnas) para eficiencia.

---

## 5. Cuestionario de Respuesta Corta

1.  **¿Qué es un DAG en el contexto de NiFi?**
    Es un Grafo Dirigido Acíclico que define cómo fluyen los mensajes a través de conexiones predefinidas entre procesos.
2.  **¿Cuál es la principal ventaja de la "Dual-Storage" mencionada en la arquitectura avanzada?**
    Permite tener un archivo histórico para analítica *batch* y, simultáneamente, una base de datos (MongoDB) para consultas operativas rápidas.
3.  **¿Para qué sirve el procesador `MergeContent` en la capa Gold?**
    Sirve para agrupar múltiples FlowFiles individuales en un solo lote antes de realizar agregaciones o cálculos estadísticos.
4.  **¿Qué ventaja ofrece la arquitectura de capas respecto al procesamiento de errores?**
    Permite el re-procesamiento: las capas Silver y Gold se pueden reconstruir en cualquier momento a partir de la capa Bronze.
5.  **En el procesador `QueryRecord`, ¿qué representa el término `FLOWFILE` dentro de una consulta SQL?**
    Es una convención especial de Apache Calcite que indica que el contenido del FlowFile actual debe tratarse como la fuente de datos de la consulta.

---

## 6. Temas de Ensayo para Profundización

1.  **Evolución del Big Data: De Datos en Reposo a Datos en Movimiento.**
    *Analice cómo las necesidades de negocio (como el análisis de clics en tiempo real o sensores IoT) han desplazado el foco desde los lagos de datos estáticos hacia sistemas de ingestión continua como Apache NiFi y Kafka.*

2.  **La Importancia de la Arquitectura de Medallón en la Ingeniería de Datos Moderna.**
    *Explore por qué es crítico mantener una copia de los datos en bruto (Bronze) y cómo el proceso de refinamiento hasta la capa Gold facilita la toma de decisiones basada en datos optimizados.*

3.  **Dinámicas de Equipo en Proyectos de IA y Big Data.**
    *Debata cómo la asignación de roles técnicos y de gestión (según el modelo ETHAZI) previene conflictos y asegura que los entregables técnicos (como scripts de Python o pipelines de NiFi) se completen eficientemente.*

---

## 7. Glosario de Términos Importantes

*   **AttributesToJSON:** Procesador que convierte atributos específicos de un FlowFile en un documento JSON.
*   **Docker Compose:** Herramienta utilizada para levantar contenedores (ej. MariaDB y MongoDB) necesarios para las prácticas de ingeniería de datos.
*   **FlowFile Lineage:** Seguimiento histórico que permite ver de dónde viene un dato y qué transformaciones ha sufrido.
*   **Jupyter Notebook (.ipynb):** Formato de archivo estándar para el desarrollo interactivo de ciencia de datos y lenguajes de programación.
*   **Logica Lausoa (Lógica Difusa):** Uno de los modelos de IA incluidos en el material conceptual del curso.
*   **NDJSON:** Formato de JSON delimitado por nuevas líneas, comúnmente usado como entrada para lectores como `JsonTreeReader`.
*   **Parquet:** Formato de almacenamiento en disco optimizado para consultas analíticas rápidas en entornos Big Data.
*   **PutMongoRecord:** Procesador que utiliza la API de registros de NiFi para insertar datos en MongoDB de forma más eficiente que el `PutMongo` clásico.
*   **Run Schedule:** Parámetro que define la frecuencia con la que un procesador se ejecuta (ej. cada 5 segundos o 30 segundos).