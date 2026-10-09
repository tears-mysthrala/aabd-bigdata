# AABD · Big Data Aplicado — Ejercicios resueltos y laboratorios

Repositorio de estudio del ciclo **IA y Big Data**: apuntes, ejercicios resueltos
y laboratorios Docker de todo el curso, organizados **por asignatura con sus
soluciones dentro**. En euskera (material de clase) con resúmenes en español.

Empieza por la [guía para llegar del enunciado a su solución](#cómo-moverse-por-el-repositorio).

Consulta la [auditoría de ejercicios](00_Transversal/AUDITORIA_EJERCICIOS.md)
para localizar enunciados, soluciones y comprobaciones, incluidos los materiales
de archivo y las tareas que aún dependen de evidencia humana o de laboratorio.

La [revisión documental](00_Transversal/REVISION_DOCUMENTACION_EJERCICIOS.md)
recoge las mejoras de explicación, guías de uso y problemas de resultados aún
pendientes. Para Python empieza por el
[recorrido de programación](04_Programazioa_5073/soluzioak/README.md).

> ⚠️ Material de estudio, no software de producción. MongoDB/Kafka van sin
> autenticación y atados a `127.0.0.1`: apto para laboratorio, no para exponer.
> Lee [SECURITY.md](SECURITY.md).

## Estructura

| Carpeta | Contenido | Estado |
|---|---|---|
| `00_Transversal/` | `SECURITY.md` del lab, `SBOM/`, `notebooklm/`, programaciones | ✅ |
| `01_Erronka1_CNC_Guard/` | Reto 1: `materialak/`, `proyecto_cnc_guard/` (uv + tests), `soluzioak/` | ✅ |
| `02_AA_Ereduak_5071/` | Paradigmas IA + Lógica difusa | ✅ |
| `03_ML_5072/` | ML: EDA, preprocesado, regresión, clasificación | ✅ |
| `04_Programazioa_5073/` | Python, `materialak/` + `soluzioak/` (6 bloques), `data/`, ejercicio Git 4.2 | Material mixto |
| `05_BigData_Ingeniaritza/` | 7V, ciclo de vida, ETL/ELT, Lakehouse | ✅ |
| `06_NiFi/` | 7 casos NiFi (12 flujos, incluida variante Open-Meteo), labs MariaDB→MongoDB y AEMET Medallion | Casos 1–6 y variante Open-Meteo probados en lab; AEMET original parcial |
| `07_Kafka/` | Pub/sub, consumer groups, lab Python y broker compartido en `infra/` | Prácticas en broker aislado |
| `infra/` | nginx frontal + Kafka compartidos (red `iabd-infra-net`) | ✅ |
| `_archivo_legacy/` | Duplicados antiguos (no usar) | 🗄️ |
| `INDICE.md` | Mapa detallado + auditoría de seguridad 2026-09-22 | 📖 |

Compatibilidad: `materialak/`, `soluzioak/`, `notebooks_compat/`, `SBOM_compat/`,
`notebooklm_compat/` y `katalogoa.*` son **symlinks** a las rutas canónicas.

Los estados de esta tabla orientan sobre el contenido disponible; no certifican
que todos los ejercicios se hayan ejecutado. Consulta la
[auditoría de ejercicios](00_Transversal/AUDITORIA_EJERCICIOS.md) para distinguir
soluciones existentes, comprobaciones y evidencias pendientes.

## Qué se estudia en cada módulo

| Módulo | Conceptos y prácticas |
|---|---|
| [00 · Transversal](00_Transversal/) | Programaciones y recursos comunes, seguridad del laboratorio, inventario de componentes (SBOM), herramientas de estudio y seguimiento de ejercicios. |
| [01 · CNC Guard](01_Erronka1_CNC_Guard/) | Reto integrador de detección de anomalías en máquinas CNC: datos sintéticos, reglas difusas Mamdani, Isolation Forest y evaluación de alertas. Los resultados con datos sintéticos no demuestran eficacia industrial. |
| [02 · AA Ereduak 5071](02_AA_Ereduak_5071/) | Modelos y paradigmas de IA, lógica difusa, sesgos, ética y marco legal, incluida la clasificación de riesgos del AI Act. |
| [03 · ML 5072](03_ML_5072/) | Exploración y preparación de datos, regresión lineal y logística, clasificación, regularización y evaluación de modelos con Python y Orange. |
| [04 · Programazioa 5073](04_Programazioa_5073/) | Fundamentos de Python, funciones y estructuras de datos; NumPy, Pandas y gráficos; formatos de archivo, Git, DVC y ejercicios de frameworks y herramientas de IA. Las soluciones se agrupan en seis bloques. |
| [05 · Big Data Ingeniaritza](05_BigData_Ingeniaritza/) | Características y ciclo de vida de Big Data, generación de datos, CSV/JSON/Parquet, ETL/ELT y organización de Data Lake/Lakehouse con capas Bronze, Silver y Gold. |
| [06 · NiFi](06_NiFi/) | Flujos de ingestión y transformación: contenido y atributos, Record API, filtrado y conversión, HTTP, MariaDB → MongoDB y datos de AEMET. Importar un JSON no basta para validar un flujo. |
| [07 · Kafka](07_Kafka/) | Topics, particiones, claves, offsets y grupos de consumidores; productores y consumidores Python y prácticas de streaming con un broker de laboratorio. |
| [Infraestructura](infra/) | Servicios Docker compartidos y su configuración: red del laboratorio, nginx y Kafka. La guía de cada práctica indica qué servicios necesita. |

## Cómo moverse por el repositorio

**Para estudiar un ejercicio, empieza en esta guía y abre su resolución desde
las tablas siguientes.** Cada fila relaciona el material de partida con la
carpeta o archivo que necesitas. Los enlaces funcionan desde este README tanto
en GitHub como en un editor que permita abrir Markdown.

1. Identifica la **asignatura, tema y edición** del ejercicio: PDF, cuaderno o
   ampliación de Drive. Un número como «3.5» puede significar cosas distintas.
2. Abre el **enunciado** y después la **guía de la solución** de la misma fila.
   La guía contiene dependencias, carpeta desde la que ejecutar y archivos de salida.
3. Para leer Python, abre el `.ipynb` resuelto: enunciado, explicación y código
   están juntos en las celdas. Para ejecutarlo como script, usa el `.py` indicado
   en su guía. Algunas parejas tienen diferencias documentadas.
4. Consulta el estado en la [matriz de ejercicios](00_Transversal/AUDITORIA_EJERCICIOS.md).
   Si falta una solución o una evidencia, esa matriz explica qué queda pendiente.
   Los [estado actualizado el 2026-10-02](00_Transversal/REVISION_NOVEDADES_EJERCICIOS_2026-10-02.md)
   dan el orden de trabajo fuera de CNC Guard.

### Acceso por asignatura

| Buscas… | Abre primero… |
|---|---|
| AA: conceptos, ética, marco legal o COMPAS | [Rutas de AA](#aa-conceptos-ética-y-marco-legal) |
| ML: Python, Orange o Iris | [Rutas de ML](#ml-python-orange-e-iris) |
| Python, NumPy/Pandas, Git o frameworks | [Los seis bloques de Programación](#programación-seis-bloques-y-sus-versiones) |
| Big Data, Faker o Elastic/Kibana | [Rutas de Ingeniería](#big-data-ingeniería-y-elastickibana) |
| Un caso NiFi del 1 al 7 | [Rutas de NiFi](#nifi-casos-1-a-7) |
| Kafka básico, clúster o Connect | [Rutas de Kafka](#kafka-básico-y-avanzado) |
| CNC Guard | [Guía del proyecto](01_Erronka1_CNC_Guard/proyecto_cnc_guard/README.md) y [guía de entregas](01_Erronka1_CNC_Guard/soluzioak/README.md). Aplazado según la revisión de 2026-10-01. |
| Recursos comunes y herramientas de estudio | [Transversal](00_Transversal/) y [NotebookLM](00_Transversal/notebooklm/README.md) |

### AA: conceptos, ética y marco legal

| Tema | Enunciado o material | Resolución y guía |
|---|---|---|
| Introducción / IE1 | [Introducción conceptual](02_AA_Ereduak_5071/materialak/5071-IE1-Sarrera_Kontzeptuala.md) | [Respuestas IE1](02_AA_Ereduak_5071/soluzioak/IE1_Sarrera_Ariketak.md) |
| Ética y sesgos | [PDF de ética](02_AA_Ereduak_5071/materialak/E1-Ereduak-Etika_eta_legea.pdf) | [Respuestas y fichas](02_AA_Ereduak_5071/soluzioak/etikako_ariketa_osagarriak.md); identifica la página/actividad del PDF. |
| Marco legal / IE6 | [Material IE6](02_AA_Ereduak_5071/materialak/5071-IE6-Marko_legala.md) | [Respuestas por actividad](02_AA_Ereduak_5071/soluzioak/IE6_Marko_Legala/ariketak_eta_jarduerak.md) y [guía de las entregas](02_AA_Ereduak_5071/soluzioak/README.md) |
| COMPAS | [Guía de fuente, umbral y métricas](02_AA_Ereduak_5071/materialak/Alborapenak/README.md) | [Notebook ejecutado y reconciliado](02_AA_Ereduak_5071/soluzioak/COMPAS/COMPAS_reconciliado.ipynb), con umbrales 7/5 separados; material docente original conservado. |
| Lógica difusa vinculada a CNC | [Material de lógica difusa](02_AA_Ereduak_5071/materialak/5071-IE1-Logika_Lausoa.md) | [Resumen conjunto AA/CNC](01_Erronka1_CNC_Guard/soluzioak/Ebazpena_CNC_Guard_eta_AA_Ereduak.md); distingue propuesta de código implementado. |

### ML: Python, Orange e Iris

| Práctica | Enunciado o material | Guía / resolución que debes abrir |
|---|---|---|
| EDA y preprocesado Python | [Material de datos](03_ML_5072/materialak/5072_1_Datua_eta_Aurreprozesamenua.pdf) | [Guía ML](03_ML_5072/soluzioak/README.md) → [notebook resuelto](03_ML_5072/soluzioak/5072_ML_praktika.ipynb) |
| Regresión lineal en Orange | [Material de regresión lineal](03_ML_5072/materialak/5072_2_01_Erregresio_Lineala.pdf) | [Guía Auto MPG](03_ML_5072/soluzioak/README.md) → [PDF de entrega](03_ML_5072/soluzioak/Orange_Erregresio_Lineala_Entregagarria.pdf) |
| Regresión logística en Orange | [Material de regresión logística](03_ML_5072/materialak/5072_2_02_Erregresio_Logistikoa.pdf) | [Guía WDBC](03_ML_5072/soluzioak/README.md) → [PDF de entrega](03_ML_5072/soluzioak/Orange_Regresion_Logistica_Entregable.pdf) |
| KNN Iris en Orange | [Teoría KNN](03_ML_5072/materialak/5072_2_03_KNN.pdf) | [Guía y estado de Iris KNN](03_ML_5072/soluzioak/Orange_KNN_Iris.md): enlaza workflow, CSV y PDF; exportado corregido y verificado por fila (CA 0,9600). |
| LogReg vs KNN, Iris 2D / Jupyter | [Notebook de partida](03_ML_5072/materialak/ikaskuntza_gainbegiratua_ikaslea.ipynb) y [plantilla de informe](03_ML_5072/materialak/txostena_ikaslea.md) | [Guía Iris 2D](03_ML_5072/soluzioak/Iris_LogReg_KNN/README.md) → [informe completado](03_ML_5072/soluzioak/Iris_LogReg_KNN/txostena_beteta.md). La carpeta contiene script, figura y notebook resuelto ejecutado. |
| Árbol y Random Forest | [Árbol](03_ML_5072/materialak/5072_2_04_Decision_Tree.pdf) y [Random Forest](03_ML_5072/materialak/5072_2_06_Random_Forest.pdf) | [Base Heart Disease](03_ML_5072/soluzioak/README.md): incluye ambos modelos; resultados CV y figuras regenerados; [guía de evaluación](03_ML_5072/soluzioak/Heart_Disease_Evaluacion.md). |
| SVM, SVC/SVR | [PDF SVM](03_ML_5072/materialak/5072_2_05_SVM.pdf) | [Guía y notebook ejecutado](03_ML_5072/soluzioak/SVM/README.md); ejemplos del PDF y extensión educativa separados. Tarea confirmada con enunciado vacío y sin plazo visible. |
| Interpretación de datos en Orange | [Requisitos de la tarea 63638 y pendientes](00_Transversal/REVISION_NOVEDADES_EJERCICIOS_2026-10-01.md) | [PDF específico y guía](03_ML_5072/soluzioak/Interpretacion_Datos/README.md), con introducción, capturas reales y conclusiones. |

**Las dos prácticas Iris son distintas:** Orange KNN usa cuatro atributos y CV;
Iris 2D usa dos atributos y accuracy de entrenamiento. Elige por el título del
enunciado, no solo por la palabra «Iris».

### Programación: seis bloques y sus versiones

Abre la [guía de Programación](04_Programazioa_5073/soluzioak/README.md) para
preparar el entorno. Estas son las correspondencias entre fuentes y soluciones:

| Bloque / edición | Enunciado | Guía junto a la solución |
|---|---|---|
| 01 · Cuaderno de lenguajes | [Cuaderno original](04_Programazioa_5073/materialak/notebooks/5073_1_Lengoaiak_Ariketak.ipynb) | [25 ejercicios: guía, notebook y script](04_Programazioa_5073/soluzioak/01_Lengoaiak_Ariketak/README.md) |
| 02 · Cuaderno de datos | [Cuaderno original](04_Programazioa_5073/materialak/notebooks/5073_2_Datu_Zientzia_Ariketak.ipynb) | [25 ejercicios: guía, notebook y script](04_Programazioa_5073/soluzioak/02_Datu_Zientzia_Ariketak/README.md) |
| 03 · PDF de lenguajes | [PDF de lenguajes](04_Programazioa_5073/materialak/5073_1_Lengoaiak.pdf) | [Guía y archivos](04_Programazioa_5073/soluzioak/03_Lengoaiak_PDF_Ariketak/README.md) y [variantes del PDF](04_Programazioa_5073/soluzioak/03_Lengoaiak_PDF_Ariketak/ariketa_pdf_aldaerak.md) |
| 04 · PDF de datos | [PDF de datos](04_Programazioa_5073/materialak/5073_2_Datu_Zientzia.pdf) | [Guía, notebook y variantes CSV](04_Programazioa_5073/soluzioak/04_Datu_Zientzia_PDF_Ariketak/README.md) |
| 05 · PDF de frameworks | [PDF de Programazioa](04_Programazioa_5073/materialak/5073_3_Programazioa.pdf) | [26 ejercicios: guía, notebook, API y Streamlit](04_Programazioa_5073/soluzioak/05_Frameworkak_PDF_Ariketak/README.md) |
| 06 · Cuaderno ML/API | [Cuaderno original](04_Programazioa_5073/materialak/notebooks/5073_3_Programazioa_Ariketak.ipynb) | [Guía, notebook y ampliaciones del script](04_Programazioa_5073/soluzioak/06_Programazioa_Ariketak/README.md) |
| Git, ejercicio 4.2 | [Guía del PDF de lenguajes](04_Programazioa_5073/soluzioak/03_Lengoaiak_PDF_Ariketak/README.md) | [Práctica Git separada](04_Programazioa_5073/git_ariketa_4_2/README.md): script, tests y registro local. |
| Datos grandes / 10M | [Guía de generación y evaluación](04_Programazioa_5073/data/README_10M.md) | Scripts en la misma carpeta `data/`; el CSV grande se genera localmente. |

**PDF y cuaderno no siempre piden lo mismo aunque coincida el número.** En el
bloque 06 las ampliaciones de Drive están en el `.py` y en el notebook
ejecutado; este conserva los ejercicios base y añade bloques de ampliación identificados. Para identificar qué descarga corresponde a cada
edición, consulta el [registro de fuentes Moodle/Drive](04_Programazioa_5073/materialak/MOODLE_URLs.md).

**Novedades de Moodle (05/10):** [revisión y resultados](00_Transversal/REVISION_NOVEDADES_EJERCICIOS_2026-10-05.md), con Programación 2.4/2.5, [SVM](03_ML_5072/soluzioak/SVM/README.md), Elastic P13/P15–P17 y [Kafka caso 5](07_Kafka/soluzioak/kafka_aurreratua_connect/caso5/README.md).

### Big Data: ingeniería y Elastic/Kibana

| Bloque | Enunciado | Resolución / guía |
|---|---|---|
| Introducción, 7V y roles | [Ejercicios 01_01](05_BigData_Ingeniaritza/materialak/Ariketak_01_01_big_data_sarrera.md) | [Respuestas](05_BigData_Ingeniaritza/soluzioak/01_Big_Data_Sarrera/Ariketak_01_01_Big_Data_Sarrera_Ebazpena.md) |
| Ingeniería, ETL/ELT y formatos | [Ejercicios 01_02](05_BigData_Ingeniaritza/materialak/Ariketak_01_02_datuen_ingeniaritza.md) | [Respuestas](05_BigData_Ingeniaritza/soluzioak/02_Datuen_Ingeniaritza/Ariketak_01_02_Datuen_Ingeniaritza_Ebazpena.md) y [guía Faker](05_BigData_Ingeniaritza/soluzioak/02_Datuen_Ingeniaritza/README.md) |
| Elastic, P1–P17 | [PDF Elastic Stack](05_BigData_Ingeniaritza/materialak/02_elastic_stack.pdf) | [Guía de prácticas](05_BigData_Ingeniaritza/soluzioak/03_Elastic_Stack/README.md) → [resolución](05_BigData_Ingeniaritza/soluzioak/03_Elastic_Stack/Ebazpena_Elastic_Praktikak.md) → [dashboards y evidencias](05_BigData_Ingeniaritza/soluzioak/03_Elastic_Stack/dashboards/README.md) |

### NiFi: casos 1 a 7

Los enunciados 1–4 están en la [guía inicial](<06_NiFi/materialak/GIDA Apache NiFi instalazioa eta kasu praktikoak 1-2-3-4.pdf>);
los casos 5–7, en la [guía avanzada](<06_NiFi/materialak/Apache NiFi kasu praktikoak (5-6-7).pdf>).
Cada enlace abre el README del caso: desde allí llegas al flow JSON, datos,
configuración, pruebas y límites. [Mapa completo de archivos NiFi](06_NiFi/soluzioak/README.md).

| Caso / identificador | Abre esta guía |
|---|---|
| 1 / DF1.1 · Mover archivos y conflictos | [Caso 1](06_NiFi/soluzioak/01_Fitxategiak_Mugitu_Gatazkak/README.md) |
| 2 / DF1.2 · Filtrar CSV | [Caso 2 y sus tres variantes](06_NiFi/soluzioak/02_CSV_Datuak_Iragazi/README.md) |
| 3 / DF1.3 · Atributos y linaje | [Caso 3](06_NiFi/soluzioak/03_Atributuak_eta_Linajea/README.md) |
| 4 / DF1.4 · HTTP a MongoDB | [Caso 4](06_NiFi/soluzioak/04_HTTP_Ingesta_eta_MongoDB/README.md) |
| 5 / DF2.1 · CSV a JSON | [Caso 5](06_NiFi/soluzioak/05_CSV_JSON_ConvertRecord_DF2.1/README.md) |
| 6 / DF2.2 · MariaDB a MongoDB | [Caso 6 y su laboratorio](06_NiFi/soluzioak/06_MariaDB_MongoDB_Laborategia_DF2.2/README.md) |
| 7 / DF2.3 · AEMET y Medallion | [Caso 7, AEMET original y variante Open-Meteo verificada](06_NiFi/soluzioak/07_AEMET_Datu_Lakua_Medallion_DF2.3/README.md) |

Un flow JSON disponible no demuestra que se haya ejecutado con éxito. Antes de
importarlo, lee el estado y las instrucciones del caso concreto.

### Kafka: básico y avanzado

Empieza por la [guía de Kafka](07_Kafka/soluzioak/README.md) para elegir broker,
producer y consumer. Después usa la fila correspondiente:

| Serie | Enunciado | Resolución |
|---|---|---|
| Básico: topics, particiones y offsets | [PDF Kafka básico](07_Kafka/materialak/01_03_ApacheKafka.pdf) | [Primeros ejercicios](07_Kafka/soluzioak/ariketa_kontsola_topic_partizio_offset.md) y [serie 5–11](07_Kafka/soluzioak/ariketa_kontsola_5_11_erreplika_gako_taldeak_offset.md) |
| Avanzado: segundo caso, clúster y consumidores | [PDF Kafka avanzado](07_Kafka/materialak/01_04_ApacheKafka_aurreratua.pdf) | [Resolución del caso 2](07_Kafka/soluzioak/kafka_aurreratua_2_kasua/Ebazpena_2_Kasua.md); scripts y registro de ejecución en esa carpeta. |
| Avanzado: caso 3, Bronze/Silver/Gold | Mismo PDF avanzado, pp. 18–37 | [Scripts, guía y evidencia](07_Kafka/soluzioak/kafka_aurreratua_3_kasua/README.md): probado en Kafka/Mongo con fixture y API Open-Meteo real; el-tiempo.net original sigue pendiente por HTTP 405. |
| Avanzado: Kafka Connect | Mismo PDF avanzado | [Resolución Connect](07_Kafka/soluzioak/kafka_aurreratua_connect/Ebazpena_Connect.md); configuración SQL/source/sink y registro en esa carpeta. |
| Avanzado: caso 5, MySQL → Connect → MongoDB | Mismo PDF avanzado, pp. 56–69 | [Receta del caso 5](07_Kafka/soluzioak/kafka_aurreratua_connect/caso5/README.md); SQL exacto, Streaming y verificación tras reinicio. Registro secuencial por REST ante bloqueo del comando literal. |

### Si una ruta o una versión te confunde

`materialak` significa **materiales/enunciados**; `soluzioak`, **soluciones**;
`ariketak`, **ejercicios**; `ebazpena`, **resolución**. `data/` o `datos/` guarda
entradas; en NiFi, `sarrera/` es entrada e `irteera/`, salida.

Los originales docentes permanecen en `materialak/` porque la sincronización
Moodle/Drive los actualiza. Las guías enlazan esos originales con sus soluciones.
Las carpetas de compatibilidad de la raíz son symlinks al mismo contenido;
usa las rutas de asignatura de esta guía para evitar confundirte con duplicados.
`_archivo_legacy/` contiene versiones históricas, no una segunda lista de tareas.

En GitHub pulsa el enlace de la tabla; para volver, usa el botón Atrás del
navegador. En local, abre el README principal y sigue sus enlaces. Los comandos
siguientes parten de la **raíz del repositorio**:

```bash
# Entrar al bloque de lenguajes y ver guía, notebook y script
cd 04_Programazioa_5073/soluzioak/01_Lengoaiak_Ariketak
ls
# Volver al README principal: tres niveles hasta la raíz
cd ../../..
```

Si buscas una pregunta concreta, usa Ctrl+F en el notebook/Markdown con su
número y parte del enunciado. Si no aparece, comprueba la edición en la tabla
antes de abrir una copia antigua. Para una actividad todavía sin solución,
consulta su fila en la [auditoría](00_Transversal/AUDITORIA_EJERCICIOS.md).

## Puesta en marcha

Para descargar y leer el material basta con Git. Desde el directorio donde
quieras guardar el repositorio:

```bash
git clone https://github.com/tears-mysthrala/aabd-bigdata.git
cd aabd-bigdata
```

Para ejecutar una práctica, consulta primero su README. Los siguientes comandos
parten de la raíz del repositorio y requieren las herramientas indicadas abajo:

```bash
# 1. Preparar el entorno del proyecto CNC Guard
(cd 01_Erronka1_CNC_Guard/proyecto_cnc_guard && uv sync)

# 2. Práctica ML 5072
01_Erronka1_CNC_Guard/proyecto_cnc_guard/.venv/bin/python \
  03_ML_5072/soluzioak/5072_ML_praktika.py

# 3. Kafka: seguir la guía del módulo y usar un broker de laboratorio aislado
#    07_Kafka/soluzioak/README.md

# 4. Lab NiFi + MariaDB + MongoDB (con infra ya arriba)
#    06_NiFi/soluzioak/06_MariaDB_MongoDB_Laborategia_DF2.2/README.md
#    Revisar .env.example y configurar secretos locales antes de desplegar.
```

El proyecto CNC Guard usa Python 3.13 y [`uv`](https://docs.astral.sh/uv/).
Los laboratorios de servicios requieren Docker y Compose; las dependencias
adicionales se indican en sus guías. No necesitas levantar todos los servicios
para estudiar o ejecutar un ejercicio de Python. No uses `chmod 666` sobre el
socket de Docker. Si ejecutas Jupyter, limítalo a `127.0.0.1` con token.

## NotebookLM

Cuaderno sincronizado con fuentes y artefactos de estudio
(`00_Transversal/notebooklm/`): guía, flashcards, quiz, mapa mental, podcast y vídeo.
Tras `notebooklm login`, las novedades se suben con
`00_Transversal/notebooklm/SUBIR_NOVEDADES.sh`.

## Contribuir y seguridad

- Para añadir soluciones: [CONTRIBUTING.md](CONTRIBUTING.md).
- Para avisar de vulnerabilidades o secretos filtrados: [SECURITY.md](SECURITY.md).
- GitHub Actions valida las PR; no hay CI ni despliegues en cada push.

## Material nuevo resuelto · 7 de octubre de 2026

- [AA: seis actividades de seguridad, privacidad y EIA](02_AA_Ereduak_5071/soluzioak/Segurtasuna_Pribatasuna_2026-10-07/README.md).
- [Programación: ampliación Pipeline/API](04_Programazioa_5073/soluzioak/08_Moodle_2026-10-07/README.md).
- [Series temporales: respuestas y práctica Pandas](06_NiFi/soluzioak/08_Denbora_Serieak/README.md).

Kafka no añade ejercicios en la edición de hoy: el diff textual del PDF elimina una línea de comprobación del arranque. Se conserva la [solución y evidencia del caso 5](07_Kafka/soluzioak/kafka_aurreratua_connect/caso5/README.md). Los cambios de outputs/metadata en cuadernos previos no representan ejercicios nuevos.

- [Elastic: Compose de apoyo incorporado a las 14:01](05_BigData_Ingeniaritza/soluzioak/03_Elastic_Stack/novedades_2026-10-07.md), sin ejercicio adicional. Se integran las fuentes del último snapshot de hoy y se verifican sus 79 archivos con SHA-256; los tres modelos de apoyo remotos no se cargan. El PDF de series temporales actualizado no cambia su texto.

## Novedades y pruebas del 8 de octubre

[Informe de ejercicios y validación](00_Transversal/validaciones_2026-10-08/README.md): Boosting y Elastic Stack P18–P22, 92 pruebas finales, ejecución de las series de Programación y lista explícita de requisitos humanos o externos pendientes.

## Novedades y pruebas del 9 de octubre

[Informe actualizado](00_Transversal/validaciones_2026-10-09/README.md): series temporales adaptadas a los 19 pasos, contraste del cuaderno 3 con las soluciones docentes, 115 pruebas locales y guía de examen sincronizada. Ciclo real con 83 archivos verificados y cero fuentes pendientes; los requisitos humanos y externos siguen identificados.

- [Guía visual de 20 modelos: clasificación, regresión y Boosting](03_ML_5072/soluzioak/Guia_Visual_Modelos/README.md), con galería offline, datos reproducibles y los 14 gráficos originales conservados.
