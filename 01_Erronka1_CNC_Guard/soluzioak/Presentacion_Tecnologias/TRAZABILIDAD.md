# CNC_Guard: trazabilidad de la presentación

Revisión local: 2026-10-13. Propuesta académica; no declara despliegue, entrenamiento ni predicción industrial verificados.

## Alcance de la revisión

Se extrajeron y revisaron por bloques 100 archivos textuales de las siete carpetas `materialak`: PDF, DOCX, Markdown, HTML, Python y notebooks. Se excluyen simulacros generados. Las soluciones y README del proyecto sirven solo para reconocer el estado del prototipo. No se visitó contenido nuevo de enlaces externos Moodle/Drive: la cobertura se limita al curso descargado en este checkout. Los duplicados de formato no representan temas adicionales.

## Requisitos técnicos en rojo

El PDF contiene 34 criterios técnicos rojos en las páginas físicas 3–7. No prescribe Kafka, NiFi, un algoritmo o una base de datos concreta. Los criterios negros y el trabajo organizativo siguen siendo contexto aplicable; el rojo señala la prioridad obligatoria indicada por el usuario.

| ID | Página PDF | Texto original | Diapositiva |
|---|---:|---|---:|
| AA/IE1/a | 3 | a) Sistema adimendunen funtsezko printzipioak identifikatu ditu. | 13 |
| AA/IE1/c | 3 | c) Adimen artifizialaren ingurunean erabili beharreko oinarrizko teknikak identifikatu ditu. | 13 |
| AA/IE2/b | 3 | b) Adimen artifizialeko ereduak sailkatu ditu. | 13 |
| AA/IE2/g | 3 | g) Ereduak problemak ebazteko sistemaren inplementaziora egokitzen diren baloratu du. | 13 |
| AA/IE6/a | 3 | a) Adimen artifiziala aplikatzeak izan ditzakeen arrisku legalak eta etikoak argudiatu ditu. | 22 |
| AA/IE6/b | 3 | b) Datuen pribatutasuna errespetatzeko beharra ezagutu du. | 22 |
| ML/IE1/a | 4 | a) Adimen artifizial indartsu eta ahularen berezitasunak zehaztu ditu. | 13 |
| ML/IE1/b | 4 | b) Adimen artifizialaren eta ikaskuntza automatikoaren (Machine Learning) arteko oztopoak ezarri ditu. | 13 |
| ML/IE2/b | 4 | b) Ikaskuntza automatikoko sistemen motak eta erabilerak zehaztu ditu. | 13 |
| ML/IE2/c | 4 | c) Ikaskuntza automatikoko sistemen teknikak eta tresnak zehaztu ditu. | 13 |
| ML/IE3/c | 4 | c) Entrenamendu-fasean datuak erabili ditu eredua eraikitzeko, lortutako ezaugarri garrantzitsuak aplikatuta. | 15 |
| ML/IE3/f | 4 | f) Datu berriei buruzko iragarpenak egiteko eredua inplementatu du. | 15 |
| ML/IE4/b | 5 | b) Arazo mota horiek ebazteko erabiltzen diren gainbegiratu gabeko ikaskuntza-teknikak ezaugarritu ditu. | 16 |
| ML/IE4/c | 5 | c) Gainbegiratu gabeko ikaskuntzan erabiltzen diren algoritmoak aplikatu ditu. | 16 |
| ML/IE6/a | 5 | a) Planteatutako arazoak konpontzeko proposatutako algoritmoen egokitasuna baloratu du. | 18 |
| ML/IE6/b | 5 | b) Sistema adimendunen oinarrizko printzipio eta tekniken aplikazio praktikoa ebaluatu du. | 18 |
| Programación/IE1/b | 5 | b) Aplikazioa garatzeko programazio-lengoaia egokiena zehaztu du. | 7 |
| Programación/IE1/e | 5 | e) Informatika-programa baten egitura eta adimen artifizialaren aplikazioa garatzeko programazio-lengoaiaren oinarririk egokienak identifikatu ditu. | 7 |
| Programación/IE2/c | 5 | c) Planteatutako arazoaren arabera inplementatu nahi den eredua definitu du. | 19 |
| Programación/IE2/d | 5 | d) Adimen artifizialaren aplikazioa inplementatu du. | 19 |
| Sistemas Big Data/IE1/b | 6 | b) Datu-bolumen handietatik abiatuta, informazioa eta ezagutza automatikoki atera ditu. | 6 |
| Sistemas Big Data/IE1/c | 6 | c) Hainbat iturri eta datu mota konbinatu ditu. | 6 |
| Sistemas Big Data/IE2/a | 6 | a) Informazioa irudikatzeko tekniken hainbat liburutegi eta inplementazio sailkatu ditu. | 21 |
| Sistemas Big Data/IE2/b | 6 | b) Lortu beharreko helburuari eta datuen izaerari buruzko informazioa gurutzatu du. | 21 |
| Sistemas Big Data/IE3/a | 6 | a) Hainbat iturritatik datuak atera eta biltegiratu ditu, hainbat agertokitan tratatzeko. | 10 |
| Sistemas Big Data/IE3/d | 6 | d) Datu-bolumen handiak kudeatzeko, biltegiratzeko eta prozesatzeko sistemak modu eraginkorrean eta seguruan garatu ditu, dagoen araudia kontuan hartuta. | 10 |
| Sistemas Big Data/IE4/e | 7 | e) Datuen egitura automatikoki programatzeko eta prozesatzeko modua egiaztatu du. | 20 |
| Sistemas Big Data/IE4/f | 7 | f) Grafikoki adierazi nahi ditugun datuak bistaratzeko moduak baloratu ditu, eta, horrela, emaitzak aztertzeko eta aurkezteko zereginak erraztu ditu. | 20 |
| Big Data aplicada/IE1/b | 7 | b) Datuak irensteko prozedurak eta mekanismoak zehaztu ditu. | 8 |
| Big Data aplicada/IE1/d | 7 | d) Biltegiratutako datuak prozesatu ditu. | 8 |
| Big Data aplicada/IE3/a | 7 | a) Banatutako fitxategi-sistemetan datuen kalitateak duen garrantzia baloratu du. | 22 |
| Big Data aplicada/IE3/b | 7 | b) Datuen tratamendu-bolumena zenbat eta handiagoa izan datuen osotasunarekin lotutako arrisku handiagoa dagoela baloratu du. | 22 |
| Big Data aplicada/IE5/a | 7 | a) Egituratutako eta egituratu gabeko datu ugari hautatu ditu, BIren funtzioa indartzeko. | 12 |
| Big Data aplicada/IE5/b | 7 | b) Datuak garbitu eta eraldatu ditu, aurrez zehaztutako helburuetan oinarrituta. | 12 |

## Selección cerrada

| Función | Tecnología elegida | Razón |
|---|---|---|
| Ingesta y validación | NiFi | Integración de archivos/formatos y rutas de rechazo trabajadas en el curso |
| Transporte | Kafka | Consumo separado, retención y relectura |
| Cálculo y servicio | Python, NumPy, pandas, scikit-learn | Una preparación compartida entre entrenamiento e inferencia |
| Riesgo supervisado | Random Forest | Modelo tabular no lineal del curso |
| Revisión de anomalías | Isolation Forest | Técnica no supervisada citada en ML; no veta el aviso supervisado |
| Histórico | Parquet | Formato columnar para entrenamiento y archivo |
| Consulta del histórico | DuckDB | SQL sobre Parquet sin clúster |
| Consulta operativa | Elasticsearch | Índices y agregaciones sobre resultados |
| Panel único | Kibana | Visualización trabajada en Elastic Stack |
| Laboratorio | Docker Compose, Jupyter, Git | Servicios locales, análisis y reproducción |

No se despliegan FastAPI, Streamlit, MongoDB, MariaDB, InfluxDB, Grafana, Spark, LLM, MQTT, OPC UA ni un motor difuso en la primera versión. Regresión logística es una referencia de evaluación, no un modelo alternativo pendiente para el servicio. Las alternativas viables se limitan a la diapositiva 24.

## Decisiones iniciales de diseño

- Horizonte de fallo: 24 h, hipótesis a contrastar con mantenimiento.
- Ventanas de variables: últimos 5 min, solo datos del pasado.
- RF: 200 árboles, max_depth=12, min_samples_leaf=5, class_weight=balanced, random_state=42.
- IF: 200 árboles, max_samples=256, random_state=42.
- Umbral RF: maximizar F1 en validación como criterio académico inicial; la aceptación industrial necesita costes reales.
- Parquet: propuesta de 90 días; índice operativo: propuesta de 30 días. No son obligaciones del temario.
- Laboratorio: un broker Kafka y servicios locales; no se afirma alta disponibilidad.
- Datos reales longitudinales necesarios para validar anticipación. AI4I sirve para clasificación de estado, no para demostrar el horizonte elegido.

## Fuentes por diapositiva

### 1. CNC_Guard
Una propuesta concreta de mantenimiento predictivo

- 01_Erronka1_CNC_Guard/materialak/1Erronka_ikaslearen_txostena.docx.pdf
- 05_BigData_Ingeniaritza/materialak/01_02_datuen_ingeniaritza.pdf
- 07_Kafka/materialak/01_03_ApacheKafka.pdf
- 05_BigData_Ingeniaritza/materialak/02_elastic_stack.pdf
- 03_ML_5072/materialak/5072_2_06_Random_Forest.pdf



### 2. Objetivo y alcance
Predecir riesgo de fallo a 24 horas como hipótesis de diseño

- 01_Erronka1_CNC_Guard/materialak/1Erronka_ikaslearen_txostena.docx.pdf
- 03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf

El horizonte se propone para disponer de un turno de planificación; debe contrastarse con mantenimiento antes de usarlo en planta. Datos sintéticos/AI4I no demuestran utilidad industrial.

### 3. Qué hemos decidido
Una tecnología elegida para cada función

- 06_NiFi/materialak/01_01_ApacheNifi.pdf
- 07_Kafka/materialak/01_03_ApacheKafka.pdf
- 05_BigData_Ingeniaritza/materialak/01_02_datuen_ingeniaritza.pdf
- 05_BigData_Ingeniaritza/materialak/02_elastic_stack.pdf
- 03_ML_5072/materialak/5072_2_06_Random_Forest.pdf
- 03_ML_5072/materialak/5072_00_Sarrera.pdf

Jupyter se usa para análisis y entrenamiento; Git y Docker Compose para reproducir el laboratorio. No hay una selección pendiente de bases de datos, paneles o modelos principales.

### 4. Por qué esta combinación
Cumplir el reto con tecnologías trabajadas en el curso

- 06_NiFi/materialak/Apache NiFi kasu praktikoak (5-6-7).pdf
- 07_Kafka/materialak/01_04_ApacheKafka_aurreratua.pdf
- 03_ML_5072/materialak/5072_2_06_Random_Forest.pdf
- 03_ML_5072/materialak/5072_00_Sarrera.pdf
- 05_BigData_Ingeniaritza/materialak/01_02_datuen_ingeniaritza.pdf
- 05_BigData_Ingeniaritza/materialak/02_elastic_stack.pdf

La elección se apoya en adecuación funcional y materia docente; no se presenta Random Forest como ganador de una comparación todavía no ejecutada.

### 5. Arquitectura cerrada
El mismo recorrido para la demostración y la operación simulada

- 06_NiFi/materialak/01_01_ApacheNifi.pdf
- 07_Kafka/materialak/01_03_ApacheKafka.pdf
- 05_BigData_Ingeniaritza/materialak/01_02_datuen_ingeniaritza.pdf
- 05_BigData_Ingeniaritza/materialak/02_elastic_stack.pdf
- 04_Programazioa_5073/materialak/5073_3_Programazioa.pdf

Tres funciones de consumo independientes: archivo, inferencia y salida a Elasticsearch. El código de inferencia se comparte entre notebook y consumidor. Los conectores aún deben implementarse.

### 6. Fuentes y contrato de datos
Tres entradas fijadas para cubrir la integración

- 06_NiFi/materialak/02_Denbora_Serieak.pdf
- 06_NiFi/materialak/Apache NiFi kasu praktikoak (5-6-7).pdf
- 05_BigData_Ingeniaritza/materialak/01_02_datuen_ingeniaritza.pdf
- 05_BigData_Ingeniaritza/materialak/02_elastic_stack.pdf

Entradas de laboratorio: archivos locales. CSV de mantenimiento y logs podrán ser sintéticos para demostrar integración, pero no se usarán para afirmar capacidad industrial. No se despliega MariaDB ni MongoDB.

### 7. Python para todo el procesamiento
Un solo código de preparación e inferencia

- 04_Programazioa_5073/materialak/5073_2_Datu_Zientzia.pdf
- 04_Programazioa_5073/materialak/5073_3_Programazioa.pdf

La instalación respeta uv y el lock del repositorio; uv no se presenta como requisito del temario. No se añade API web: Kafka es el contrato entre servicios de esta propuesta.

### 8. NiFi: el flujo que construiremos
Validar antes de alimentar modelos

- 06_NiFi/materialak/01_01_ApacheNifi.pdf
- 06_NiFi/materialak/01_02_ApacheNifi_aurreratua.pdf
- 06_NiFi/materialak/Apache NiFi kasu praktikoak (5-6-7).pdf

Los nombres concretos de procesador Kafka/Record deben ajustarse a la versión instalada. Documentación primaria: https://nifi.apache.org/nifi-docs/user-guide.html .

### 9. Kafka: topics y consumidores
Cada función consume sin bloquear las demás

- 07_Kafka/materialak/01_03_ApacheKafka.pdf
- 07_Kafka/materialak/01_04_ApacheKafka_aurreratua.pdf

Laboratorio con un broker; demostrar consumo, relectura y reinicio, sin afirmar alta disponibilidad. Documentación: https://kafka.apache.org/20/documentation/ .

### 10. Parquet: histórico elegido
Conservar entrenamiento y resultados fuera del índice operativo

- 05_BigData_Ingeniaritza/materialak/01_02_datuen_ingeniaritza.pdf
- 06_NiFi/materialak/02_Denbora_Serieak.pdf

90 días es un supuesto de proyecto, no una obligación docente ni prueba de suficiencia estadística. No borrar datasets de evaluación para aplicar una retención automática en el laboratorio.

### 11. DuckDB: preparación del dataset
SQL sobre el histórico Parquet

- 05_BigData_Ingeniaritza/materialak/01_02_datuen_ingeniaritza.pdf

Fuente primaria: https://duckdb.org/docs/stable/data/parquet/overview . Spark queda solo como alternativa de escalado si las medidas lo justifican.

### 12. Preparación elegida
Ventanas de 5 minutos y etiqueta a 24 horas

- 04_Programazioa_5073/materialak/5073_2_Datu_Zientzia.pdf
- 06_NiFi/materialak/02_Denbora_Serieak.pdf
- 03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf

5 min y 24 h son decisiones iniciales de la propuesta. Si no hay timestamps longitudinales reales, usar variables del instante y etiqueta de estado, declarando que la prueba no valida este horizonte.

### 13. Tipo de IA elegido
IA débil basada en aprendizaje de datos

- 02_AA_Ereduak_5071/materialak/5071-IE1-Sarrera_Kontzeptuala.md
- 02_AA_Ereduak_5071/materialak/5071-IE1-Logika_Lausoa.md
- 03_ML_5072/materialak/5072_00_Sarrera.pdf

Se caracterizan las familias para justificar la elección. Random Forest no es un modelo conexionista; no se confunde grado de pertenencia difusa con probabilidad.

### 14. Reglas para calidad y revisión
Reglas deterministas, sin motor difuso adicional

- 02_AA_Ereduak_5071/materialak/5071-IE1-Logika_Lausoa.md
- 01_Erronka1_CNC_Guard/proyecto_cnc_guard/README.md
- 03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf

El prototipo anterior contiene Mamdani; no se incorpora al nuevo servicio. Sus resultados históricos no acreditan el rendimiento de Random Forest.

### 15. Random Forest: modelo principal
La alerta de riesgo sale de un único modelo supervisado

- 03_ML_5072/materialak/5072_2_06_Random_Forest.pdf
- 03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf

La puntuación predict_proba se trata como score de riesgo: no afirmar calibración probabilística sin evaluarla. No hay rendimiento medido en esta revisión.

### 16. Isolation Forest: detector auxiliar
Las anomalías generan revisión, no una segunda decisión de fallo

- 03_ML_5072/materialak/5072_00_Sarrera.pdf
- 03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf

Fuente: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html . Sin verdad de referencia o revisión humana, solo se verifica que puntúa rareza, no que identifica averías.

### 17. Política de alertas elegida
Dos clases de aviso, sin consenso AND

- 03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf
- 01_Erronka1_CNC_Guard/proyecto_cnc_guard/README.md
- 06_NiFi/materialak/02_Denbora_Serieak.pdf

El AND del prototipo anterior se abandona en esta propuesta porque podría vetar fallos detectados por el modelo supervisado. Las políticas de agrupación deben probarse y documentarse.

### 18. Validación que aplicaremos
Mismo problema, particiones y preparación

- 03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf
- 03_ML_5072/materialak/5072_2_02_Erregresio_Logistikoa.pdf

La logística es referencia de evaluación, no una alternativa pendiente para el servicio. El máximo F1 no es por sí solo una política industrial óptima; la aceptación de negocio necesita costes reales.

### 19. Consumidor Python: servicio de inferencia
Carga una versión del modelo y procesa eventos nuevos

- 04_Programazioa_5073/materialak/5073_3_Programazioa.pdf
- 07_Kafka/materialak/01_03_ApacheKafka.pdf
- 03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf

No se añade FastAPI: el consumidor Kafka es el servicio de esta propuesta. Se implementará y verificará antes de afirmar funcionamiento extremo a extremo.

### 20. Elasticsearch y Kibana
Una base de consulta y un único panel

- 05_BigData_Ingeniaritza/materialak/02_elastic_stack.pdf

30 días es una propuesta inicial a dimensionar. Kibana consulta Elasticsearch; no consume Kafka directamente. No se instala un segundo panel en Streamlit/Grafana.

### 21. Panel que construiremos
Cuatro preguntas para mantenimiento

- 06_NiFi/materialak/02_Denbora_Serieak.pdf
- 05_BigData_Ingeniaritza/materialak/02_elastic_stack.pdf
- 03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf

Series para evolución, barras para ranking, dispersión para relaciones, tabla para trazabilidad y matriz para errores. Se justifican los gráficos según datos y objetivo; no hay capturas ficticias.

### 22. Seguridad e integridad del diseño
Una versión local reproducible antes de cualquier conexión OT

- 02_AA_Ereduak_5071/materialak/E1-Ereduak-Etika_eta_legea.pdf
- 07_Kafka/materialak/01_04_ApacheKafka_aurreratua.pdf
- 05_BigData_Ingeniaritza/materialak/01_02_datuen_ingeniaritza.pdf
- 01_Erronka1_CNC_Guard/materialak/1Erronka_ikaslearen_txostena.docx.pdf

No conectar a maquinaria sin un diseño OT específico y autorización. La clasificación normativa es contextual; el informe analiza riesgos, no certifica cumplimiento legal.

### 23. Dimensionamiento inicial
Supuestos concretos para medir la propuesta

- 01_Erronka1_CNC_Guard/materialak/1Erronka_ikaslearen_txostena.docx.pdf
- 05_BigData_Ingeniaritza/materialak/01_02_datuen_ingeniaritza.pdf
- 06_NiFi/materialak/02_Denbora_Serieak.pdf

1 Hz, 200 bytes y 90 días son hipótesis del proyecto. No incluyen réplicas, logs de servicios ni archivos originales. Confirmar almacenamiento disponible antes de generar la carga completa.

### 24. Alternativas viables: solo si cambia la necesidad
No forman parte de la primera versión elegida

- 06_NiFi/materialak/02_Denbora_Serieak.pdf
- 05_BigData_Ingeniaritza/materialak/02_elastic_stack.pdf
- 03_ML_5072/materialak/5072_2_07_Boosting.pdf
- 05_BigData_Ingeniaritza/materialak/01_02_datuen_ingeniaritza.pdf

Alternativas resumidas en esta única diapositiva. Fuentes externas: https://docs.influxdata.com/influxdb/cloud/get-started/ ; https://opcfoundation.org/about/opc-technologies/opc-ua/ ; https://reference.opcfoundation.org/specs/OPC-10000-14/7.3.4 .

### 25. Primera entrega: datos y entrenamiento
Construir primero un modelo reproducible

- 03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf
- 03_ML_5072/materialak/5072_2_06_Random_Forest.pdf
- 03_ML_5072/materialak/5072_00_Sarrera.pdf
- 05_BigData_Ingeniaritza/materialak/01_02_datuen_ingeniaritza.pdf

Esta diapositiva define una entrega pendiente; no afirma que ya se haya entrenado o entregado nada.

### 26. Segunda entrega: recorrido completo
Demostrar recuperación y visualización

- 06_NiFi/materialak/Apache NiFi kasu praktikoak (5-6-7).pdf
- 07_Kafka/materialak/01_04_ApacheKafka_aurreratua.pdf
- 05_BigData_Ingeniaritza/materialak/02_elastic_stack.pdf

La demostración es local/simulada. No equivale a despliegue en planta, alta disponibilidad o validación de predicción a 24 horas.

### 27. Punto de partida real
Reutilizar infraestructura de análisis, cambiar el núcleo de decisión

- 01_Erronka1_CNC_Guard/proyecto_cnc_guard/README.md
- 01_Erronka1_CNC_Guard/materialak/1Erronka_ikaslearen_txostena.docx.pdf
- 03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf

Estado documentado por el README, no validación ejecutada hoy. La presentación prepara el trabajo; no modifica ni declara completado el software existente.

### 28. Plan de construcción
Tres hitos y responsables por función

- 01_Erronka1_CNC_Guard/materialak/1Erronka_ikaslearen_txostena.docx.pdf
- 03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf
- 07_Kafka/materialak/01_04_ApacheKafka_aurreratua.pdf

El enunciado da 11 semanas. El equipo debe poner nombres y fechas reales; estos roles y hitos son propuesta, no entregas Moodle realizadas.

### 29. Propuesta que defenderemos
Una arquitectura, un modelo principal y un panel

- 01_Erronka1_CNC_Guard/materialak/1Erronka_ikaslearen_txostena.docx.pdf
- 03_ML_5072/materialak/5072_2_06_Random_Forest.pdf
- 03_ML_5072/materialak/5072_00_Sarrera.pdf
- 05_BigData_Ingeniaritza/materialak/01_02_datuen_ingeniaritza.pdf
- 05_BigData_Ingeniaritza/materialak/02_elastic_stack.pdf

La propuesta está cerrada. Las alternativas del anexo no dejan decisiones abiertas en la primera versión.

### 30. Anexo · cobertura de criterios rojos
Correspondencia exacta: bloque 1 de 3

- 01_Erronka1_CNC_Guard/materialak/1Erronka_ikaslearen_txostena.docx.pdf

Referencias por número de diapositiva. La correspondencia explica cobertura del diseño, no acredita todavía el cumplimiento mediante ejecución.

### 31. Anexo · cobertura de criterios rojos
Correspondencia exacta: bloque 2 de 3

- 01_Erronka1_CNC_Guard/materialak/1Erronka_ikaslearen_txostena.docx.pdf

Referencias por número de diapositiva. La correspondencia explica cobertura del diseño, no acredita todavía el cumplimiento mediante ejecución.

### 32. Anexo · cobertura de criterios rojos
Correspondencia exacta: bloque 3 de 3

- 01_Erronka1_CNC_Guard/materialak/1Erronka_ikaslearen_txostena.docx.pdf

Referencias por número de diapositiva. La correspondencia explica cobertura del diseño, no acredita todavía el cumplimiento mediante ejecución.

### 33. Anexo · fuentes y límites
Trazabilidad de la propuesta

- 01_Erronka1_CNC_Guard/materialak/1Erronka_ikaslearen_txostena.docx.pdf

El informe TRAZABILIDAD.md contiene criterios rojos originales, mapa de tecnologías, alcance del corpus y hashes. No se descargaron contenidos nuevos de los enlaces Moodle/Drive en esta revisión.

## Fuentes primarias externas

- [NiFi User Guide](https://nifi.apache.org/nifi-docs/user-guide.html)
- [Kafka documentation](https://kafka.apache.org/20/documentation/)
- [DuckDB Parquet](https://duckdb.org/docs/stable/data/parquet/overview)
- [IsolationForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)
- [InfluxDB time-series concepts](https://docs.influxdata.com/influxdb/cloud/get-started/)
- [OPC UA](https://opcfoundation.org/about/opc-technologies/opc-ua/)
- [OPC UA PubSub MQTT](https://reference.opcfoundation.org/specs/OPC-10000-14/7.3.4)

## Entrega y uso

Abrir `CNC_Guard_Tecnologias.html` en navegador. Flechas, PageUp/PageDown o botones cambian diapositiva; N abre notas y fuentes; F activa pantalla completa. El PDF contiene el mismo contenido visible. El HTML y contenido.json conservan texto editable; no se ha generado PowerPoint porque el runtime obligatorio artifact-tool no está disponible en esta sesión.
