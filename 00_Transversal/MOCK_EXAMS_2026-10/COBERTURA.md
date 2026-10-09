# Cobertura y trazabilidad docente

[Índice de simulacros](README.md). Revisión del PR #18 el 9/10/2026.

Cada apartado evaluado se vincula a un pasaje concreto del material obtenido del
curso. Las páginas son posiciones físicas del PDF, empezando por 1; pueden
diferir de la numeración impresa. Los cuadernos se identifican por ejercicio.
El manifiesto conserva las rutas y SHA-256 de las fuentes revisadas.

Los contextos, CSV y cifras nuevos son variantes sintéticas para aplicar esas
habilidades. Los tiempos y rúbricas son de autoestudio. La guía Moodle 64153
aporta el formato 30 test / 3 puntos + práctica / 7 puntos; no cuantifica la
penalización. Los apoyos entre módulos se indican, sin incorporar teoría externa.

La revisión del contenido es docente y manual, contrastando el texto de PDFs y
cuadernos. El comprobador valida integridad, navegación y estructura; no prueba
por sí solo adecuación conceptual ni qué se ha impartido en clase. Un modelo
muestra ejercicios de la materia; no sustituye todos los ejercicios del curso.

## Correcciones de alcance

- Programación: se sustituye la pregunta sobre normas de herramientas del repositorio por
  la finalidad de entornos virtuales; se retiran balanced accuracy y la fórmula
  inventada de penalización. Las respuestas correctas se distribuyen entre las
  cuatro letras (8/8/7/7), evitando la concentración anterior en D.

- AA: se evalúan las tres fases fuzzy explicadas en clase, sin exigir Mamdani,
  integrales de centroide ni formalización de privacidad diferencial.

- CNC: el híbrido experto/fuzzy se apoya en 03.4 y los roles son los del contrato;
  la arquitectura y las métricas enlazan las fuentes de los módulos implicados.

- ML: se añade la fuente de Ridge/Lasso y el apoyo de Programación para MAE/R²,
  ColumnTransformer y GridSearchCV; se conserva la metodología documentada.

- Big Data: se distingue el ciclo de ingeniería (cinco fases) del proceso de
  Data Science (seis). ILM sigue la práctica 8; no se exige rollover/data streams.

- NiFi: se reemplaza el fallo HTTP 405 de una validación local por InvokeHTTP y
  Bronze del curso; se usa MergeContent del caso NiFi y se añade el gráfico e
  interpretación requeridos en series. Energía se limita a kWh de intervalos.

- Kafka: se conserva idempotencia conceptual y semánticas de entrega; se retiran
  watermarks, eventos tardíos y recuperación de estado/transacciones como requisito
  de implementación. Se recupera la comparación Python/NiFi del caso práctico y Connect sigue el
  caso MySQL/Kafka/MongoDB realmente incluido en el PDF.


## cnc

Reto integrado CNC Guard.

| Apartado | Materia evaluada | Fuente y pasaje |
|---|---|---|

| 1 | Objetivos, mantenimiento y límites del piloto | [1Erronka_ikaslearen_txostena.docx.pdf](<../../01_Erronka1_CNC_Guard/materialak/1Erronka_ikaslearen_txostena.docx.pdf>) — p. 2; objetivos técnicos, pp. 3–7 |

| 2 | Dependencias, PERT/Gantt y coste de retrasos | [patata tortila - planifikazioa eta kostuak lantzekoAA 2026-2027.md](<../../01_Erronka1_CNC_Guard/materialak/patata tortila - planifikazioa eta kostuak lantzekoAA 2026-2027.md>) — Ariketa: PERT, GANTT y preguntas sobre tareas que no pueden retrasarse |

| 3 | Arquitectura de datos y roles del contrato | [Ariketak_01_02_datuen_ingeniaritza.md](<../../05_BigData_Ingeniaritza/materialak/Ariketak_01_02_datuen_ingeniaritza.md>) — Datu baten bidaia; Kasu praktikoa: Smart Factory<br>[01_03_ApacheKafka.pdf](<../../07_Kafka/materialak/01_03_ApacheKafka.pdf>) — pp. 16–20: producer, broker, topic y consumer<br>[01_01_ApacheNifi.pdf](<../../06_NiFi/materialak/01_01_ApacheNifi.pdf>) — pp. 10–13: FlowFile, atributos y provenance<br>[1Erronka_ikaslearen_txostena.docx.pdf](<../../01_Erronka1_CNC_Guard/materialak/1Erronka_ikaslearen_txostena.docx.pdf>) — p. 9: coordinador, secretario y portavoz |

| 4 | Reglas, grados de pertenencia y sistema híbrido | [5071-IE1-Logika_Lausoa.md](<../../02_AA_Ereduak_5071/materialak/5071-IE1-Logika_Lausoa.md>) — 03.2, 03.3 (AND=min) y 03.4 (SA + Logika Lausoa)<br>[5072_2_01_Erregresio_Lineala.pdf](<../../03_ML_5072/materialak/5072_2_01_Erregresio_Lineala.pdf>) — p. 6: aprendizaje supervisado y no supervisado |

| 5 | Métricas, coste, evaluación y defensa | [5072_3_Balidazio_Metodologia.pdf](<../../03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf>) — pp. 3–8: separación, leakage, grupos, matriz y métricas<br>[1Erronka_ikaslearen_txostena.docx.pdf](<../../01_Erronka1_CNC_Guard/materialak/1Erronka_ikaslearen_txostena.docx.pdf>) — p. 2: coste de parada; pp. 8 y 11: evaluación individual y grupal<br>[ANEXO1-Eus.md](<../../01_Erronka1_CNC_Guard/materialak/ANEXO1-Eus.md>) — roles y compromisos del contrato de equipo |


## aa

5071 — Modelos de inteligencia artificial.

| Apartado | Materia evaluada | Fuente y pasaje |
|---|---|---|

| 1 | IA, ML, DL, Turing y sistemas expertos | [5071-IE1-Sarrera_Kontzeptuala.md](<../../02_AA_Ereduak_5071/materialak/5071-IE1-Sarrera_Kontzeptuala.md>) — 01.1, 01.3–01.6: definición, Turing, paradigmas, jerarquía y AA débil/general<br>[5072_2_01_Erregresio_Lineala.pdf](<../../03_ML_5072/materialak/5072_2_01_Erregresio_Lineala.pdf>) — p. 6: selección supervisada/no supervisada; apoyo del módulo 5072 |

| 2 | Sistema experto y tres fases fuzzy | [5071-IE1-Sarrera_Kontzeptuala.md](<../../02_AA_Ereduak_5071/materialak/5071-IE1-Sarrera_Kontzeptuala.md>) — 01.4: AA simbólica, base de conocimiento y motor de inferencia<br>[5071-IE1-Logika_Lausoa.md](<../../02_AA_Ereduak_5071/materialak/5071-IE1-Logika_Lausoa.md>) — 03.1–03.3: grados, fases y ejemplo AND=min; operadores del caso facilitados |

| 3 | COMPAS, FPR y sesgos por grupos | [2.2_compas_historikoa_soluzioa.ipynb](<../../02_AA_Ereduak_5071/materialak/Alborapenak/2.2_compas_historikoa_soluzioa.ipynb>) — Ariketa 2.2; metrikak_taldekoak y discusión accuracy/alborapena<br>[E1-Ereduak-Etika_eta_legea.pdf](<../../02_AA_Ereduak_5071/materialak/E1-Ereduak-Etika_eta_legea.pdf>) — pp. 5–13: fuentes de sesgo y COMPAS |

| 4 | Prompt injection, security/privacy y membership inference | [1.1_prompt_injection_diseinua_soluzioa.ipynb](<../../02_AA_Ereduak_5071/materialak/1.1_prompt_injection_diseinua_soluzioa.ipynb>) — amenaza, filtro y límites de la defensa<br>[E1-Ereduak-Etika_eta_legea.pdf](<../../02_AA_Ereduak_5071/materialak/E1-Ereduak-Etika_eta_legea.pdf>) — pp. 42–50: inyección, membership inference, introducción a DP y security/privacy |

| 5 | Finalidad, principios normativos, PbD e impacto | [5071-IE6-Marko_legala.md](<../../02_AA_Ereduak_5071/materialak/5071-IE6-Marko_legala.md>) — marco legal, niveles de riesgo y preguntas de auditoría<br>[3.1_privacy_by_design_auditoria_soluzioa.ipynb](<../../02_AA_Ereduak_5071/materialak/3.1_privacy_by_design_auditoria_soluzioa.ipynb>) — principios de Cavoukian y propuestas de rediseño<br>[5.1_eia_aplikatu_soluzioa.ipynb](<../../02_AA_Ereduak_5071/materialak/5.1_eia_aplikatu_soluzioa.ipynb>) — evaluación de impacto: afectados, riesgos y mitigación |


## ml

5072 — Machine Learning.

| Apartado | Materia evaluada | Fuente y pasaje |
|---|---|---|

| 1 | Nulos, categorías, leakage y validación | [5072_1_Datua_eta_Aurreprozesamenua.pdf](<../../03_ML_5072/materialak/5072_1_Datua_eta_Aurreprozesamenua.pdf>) — pp. 2–9: tipos, nulos, codificación y escalado<br>[5072_3_Balidazio_Metodologia.pdf](<../../03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf>) — pp. 3–6: train/validation/test, leakage y Group K-Fold<br>[5073_3_Programazioa.pdf](<../../04_Programazioa_5073/materialak/5073_3_Programazioa.pdf>) — pp. 14–16: implementación de Pipeline/ColumnTransformer; apoyo del módulo 5073 |

| 2 | Regresión, errores, regularización, KNN/SVM/árbol | [5072_2_Ikasketa_Gainbegiratua.pdf](<../../03_ML_5072/materialak/5072_2_Ikasketa_Gainbegiratua.pdf>) — pp. 2–9: MSE, Ridge/Lasso, logística, k y pruning<br>[5072_2_05_SVM.pdf](<../../03_ML_5072/materialak/5072_2_05_SVM.pdf>) — p. 5: soft margin y C<br>[5073_3_Programazioa.pdf](<../../04_Programazioa_5073/materialak/5073_3_Programazioa.pdf>) — pp. 12–13: MAE, MSE y R²; apoyo del módulo 5073 |

| 3 | Matriz, precision/recall/F1, ROC y multiclase | [5072_3_Balidazio_Metodologia.pdf](<../../03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf>) — pp. 7–10: matriz, métricas, macro/weighted y ROC-AUC<br>[5072_2_02_Erregresio_Logistikoa.pdf](<../../03_ML_5072/materialak/5072_2_02_Erregresio_Logistikoa.pdf>) — p. 4: probabilidad y umbral<br>[5072_3_Balidazio_Metodologia.pdf](<../../03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf>) — p. 3: selección en validation y evaluación final en test |

| 4 | Bagging/Random Forest y boosting | [5072_2_06_Random_Forest.pdf](<../../03_ML_5072/materialak/5072_2_06_Random_Forest.pdf>) — pp. 2–5: bagging, selección de features y ensembles<br>[5072_2_07_Boosting.pdf](<../../03_ML_5072/materialak/5072_2_07_Boosting.pdf>) — pp. 2–9: AdaBoost, Gradient Boosting y XGBoost<br>[5072_3_Balidazio_Metodologia.pdf](<../../03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf>) — p. 11: brecha train/validation y overfitting |

| 5 | Iris, pipelines, CV de k y límites 2D | [5072_2_02_Erregresio_Logistikoa.pdf](<../../03_ML_5072/materialak/5072_2_02_Erregresio_Logistikoa.pdf>) — p. 9: Iris con dos features y gráfico de frontera<br>[5072_2_03_KNN.pdf](<../../03_ML_5072/materialak/5072_2_03_KNN.pdf>) — pp. 2–5: vecinos, k y límites<br>[5072_3_Balidazio_Metodologia.pdf](<../../03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf>) — pp. 3–6: separación y Stratified K-Fold<br>[5073_3_Programazioa.pdf](<../../04_Programazioa_5073/materialak/5073_3_Programazioa.pdf>) — pp. 14–17: Pipeline y GridSearchCV; apoyo de código del módulo 5073 |


## programacion

5073 — Programación para IA.

| Apartado | Materia evaluada | Fuente y pasaje |
|---|---|---|

| T1 | ¿Qué combinación describe mejor el uso de Python y Java en la materia? | [5073_1_Lengoaiak.pdf](<../../04_Programazioa_5073/materialak/5073_1_Lengoaiak.pdf>) — pp. 7–9: Python y Java |

| T2 | ¿Qué hace MCP en un sistema de agentes? | [5073_1_Lengoaiak.pdf](<../../04_Programazioa_5073/materialak/5073_1_Lengoaiak.pdf>) — pp. 36–37: MCP<br>[Moodle_page_64153.md](<../../04_Programazioa_5073/materialak/Moodle_page_64153.md>) — segunda pregunta de ejemplo |

| T3 | ¿Cuál es el resultado de [x*x for x in [1,2,3] if x>1]? | [5073_1_Lengoaiak.pdf](<../../04_Programazioa_5073/materialak/5073_1_Lengoaiak.pdf>) — pp. 44–45: list comprehension |

| T4 | Para convertir una cadena JSON en un diccionario Python se usa: | [5073_1_Lengoaiak.pdf](<../../04_Programazioa_5073/materialak/5073_1_Lengoaiak.pdf>) — p. 49: JSON |

| T5 | ¿Qué conviene hacer con un pickle de origen desconocido? | [5073_1_Lengoaiak.pdf](<../../04_Programazioa_5073/materialak/5073_1_Lengoaiak.pdf>) — pp. 50–51: Pickle y advertencia de seguridad |

| T6 | ¿Qué distingue una rama de Git de un entorno virtual? | [5073_1_Lengoaiak.pdf](<../../04_Programazioa_5073/materialak/5073_1_Lengoaiak.pdf>) — pp. 21–23: entornos; pp. 52–56: Git |

| T7 | ¿Para qué sirve un entorno virtual de Python? | [5073_1_Lengoaiak.pdf](<../../04_Programazioa_5073/materialak/5073_1_Lengoaiak.pdf>) — pp. 21–23: finalidad y aislamiento de entornos virtuales |

| T8 | Un array de 12 elementos puede hacerse matriz 3×4 con: | [5073_2_Datu_Zientzia.pdf](<../../04_Programazioa_5073/materialak/5073_2_Datu_Zientzia.pdf>) — pp. 6–7: reshape |

| T9 | ¿Qué selecciona arr[arr > 5]? | [5073_2_Datu_Zientzia.pdf](<../../04_Programazioa_5073/materialak/5073_2_Datu_Zientzia.pdf>) — pp. 9–11: máscaras booleanas |

| T10 | Para dos condiciones sobre columnas Pandas se emplea normalmente: | [5073_2_Datu_Zientzia.pdf](<../../04_Programazioa_5073/materialak/5073_2_Datu_Zientzia.pdf>) — pp. 14–15: filtros y operadores Pandas |

| T11 | ¿Qué hace dropna() con sus valores por defecto sobre un DataFrame? | [5073_2_Datu_Zientzia.pdf](<../../04_Programazioa_5073/materialak/5073_2_Datu_Zientzia.pdf>) — pp. 18–20: dropna<br>[Moodle_page_64153.md](<../../04_Programazioa_5073/materialak/Moodle_page_64153.md>) — cuarta pregunta de ejemplo |

| T12 | ¿Qué instrucción modifica valores por una condición de forma explícita? | [5073_2_Datu_Zientzia.pdf](<../../04_Programazioa_5073/materialak/5073_2_Datu_Zientzia.pdf>) — pp. 14–15: selección y loc |

| T13 | ¿Qué son Figure y Axes en Matplotlib? | [5073_2_Datu_Zientzia.pdf](<../../04_Programazioa_5073/materialak/5073_2_Datu_Zientzia.pdf>) — pp. 25–27: Figure/Axes<br>[Moodle_page_64153.md](<../../04_Programazioa_5073/materialak/Moodle_page_64153.md>) — tercera pregunta de ejemplo |

| T14 | Para comparar temperatura por cámara, ¿qué gráfico ayuda? | [5073_2_Datu_Zientzia.pdf](<../../04_Programazioa_5073/materialak/5073_2_Datu_Zientzia.pdf>) — pp. 28–30: boxplot y distribución |

| T15 | ¿Dónde se ajusta StandardScaler para evaluar un holdout? | [5073_3_Programazioa.pdf](<../../04_Programazioa_5073/materialak/5073_3_Programazioa.pdf>) — pp. 3–5: escalado train/test |

| T16 | ¿Qué código separa correctamente el target? | [5073_3_Programazioa.pdf](<../../04_Programazioa_5073/materialak/5073_3_Programazioa.pdf>) — pp. 3–4: separar X e y |

| T17 | Una categoría nominal sin orden se suele codificar con: | [5073_3_Programazioa.pdf](<../../04_Programazioa_5073/materialak/5073_3_Programazioa.pdf>) — pp. 6–8: OneHot y Ordinal |

| T18 | ¿Para qué sirve Pipeline en sklearn? | [5073_3_Programazioa.pdf](<../../04_Programazioa_5073/materialak/5073_3_Programazioa.pdf>) — pp. 14–16: Pipeline y CV |

| T19 | ¿Cuál es una imputación razonable de stock con outliers? | [5073_2_Datu_Zientzia.pdf](<../../04_Programazioa_5073/materialak/5073_2_Datu_Zientzia.pdf>) — pp. 18–19: mediana<br>[5073_3_Programazioa.pdf](<../../04_Programazioa_5073/materialak/5073_3_Programazioa.pdf>) — pp. 7–8: imputación en train |

| T20 | ¿Qué significa class_weight="balanced"? | [Moodle_page_64153.md](<../../04_Programazioa_5073/materialak/Moodle_page_64153.md>) — checklist: Klaseen Desoreka Kudeatzea<br>[3_Ariketa_koadernoa_URLa.ipynb](<../../04_Programazioa_5073/materialak/3_Ariketa_koadernoa_URLa.ipynb>) — ejercicios 3.3–3.4: class_weight balanced |

| T21 | ¿Dónde debe aplicarse SMOTE durante selección con CV? | [3_Ariketa_koadernoa_URLa.ipynb](<../../04_Programazioa_5073/materialak/3_Ariketa_koadernoa_URLa.ipynb>) — ejercicios 3.5–3.6: SMOTE solo en train<br>[5072_3_Balidazio_Metodologia.pdf](<../../03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf>) — p. 4: augmentation y leakage; apoyo del módulo 5072 |

| T22 | Recall de la clase positiva es: | [5073_3_Programazioa.pdf](<../../04_Programazioa_5073/materialak/5073_3_Programazioa.pdf>) — pp. 10–12: recall |

| T23 | Precision de la clase positiva es: | [5073_3_Programazioa.pdf](<../../04_Programazioa_5073/materialak/5073_3_Programazioa.pdf>) — pp. 10–12: precision |

| T24 | Si fallo tiene prevalencia 1%, predecir siempre no fallo produce: | [5073_3_Programazioa.pdf](<../../04_Programazioa_5073/materialak/5073_3_Programazioa.pdf>) — pp. 11–12: desbalance y accuracy |

| T25 | En confusion_matrix con labels=[0,1], ¿qué representa [1,0]? | [5073_3_Programazioa.pdf](<../../04_Programazioa_5073/materialak/5073_3_Programazioa.pdf>) — pp. 10–12: matriz de confusión |

| T26 | Para elegir un umbral se debe usar: | [5073_3_Programazioa.pdf](<../../04_Programazioa_5073/materialak/5073_3_Programazioa.pdf>) — pp. 18–19: umbral<br>[5072_3_Balidazio_Metodologia.pdf](<../../03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf>) — p. 3: test final no se usa para seleccionar parámetros; apoyo del módulo 5072 |

| T27 | GridSearchCV debe recibir: | [5073_3_Programazioa.pdf](<../../04_Programazioa_5073/materialak/5073_3_Programazioa.pdf>) — pp. 16–18: GridSearchCV y scoring |

| T28 | Al publicar una API de inferencia, el modelo suele cargarse: | [5073_3_Programazioa.pdf](<../../04_Programazioa_5073/materialak/5073_3_Programazioa.pdf>) — pp. 30–33: carga al arrancar<br>[Moodle_page_64153.md](<../../04_Programazioa_5073/materialak/Moodle_page_64153.md>) — quinta pregunta de ejemplo |

| T29 | BaseModel y field_validator se usan para: | [5073_3_Programazioa.pdf](<../../04_Programazioa_5073/materialak/5073_3_Programazioa.pdf>) — pp. 29–30: BaseModel y field_validator<br>[Moodle_page_64153.md](<../../04_Programazioa_5073/materialak/Moodle_page_64153.md>) — checklist: API Eskemak |

| T30 | Una entrada de inferencia válida debe: | [5073_3_Programazioa.pdf](<../../04_Programazioa_5073/materialak/5073_3_Programazioa.pdf>) — pp. 14–15: inferencia con el pipeline; pp. 29–30: esquema de entrada |

| P1 | Inspección, list comprehension y limpieza Pandas | [Moodle_page_64153.md](<../../04_Programazioa_5073/materialak/Moodle_page_64153.md>) — checklist: Python Oinarriak y Pandas Iragazkiak<br>[5073_2_Datu_Zientzia.pdf](<../../04_Programazioa_5073/materialak/5073_2_Datu_Zientzia.pdf>) — pp. 18–20: nulos, rangos y duplicados |

| P2 | Split facilitado, Pipeline y class_weight | [Moodle_page_64153.md](<../../04_Programazioa_5073/materialak/Moodle_page_64153.md>) — checklist: ML Pipeline-en Eraikuntza y Klaseen Desoreka Kudeatzea<br>[5073_3_Programazioa.pdf](<../../04_Programazioa_5073/materialak/5073_3_Programazioa.pdf>) — pp. 14–16: Pipeline<br>[3_Ariketa_koadernoa_URLa.ipynb](<../../04_Programazioa_5073/materialak/3_Ariketa_koadernoa_URLa.ipynb>) — ejercicios 3.3–3.4: class_weight balanced<br>[5072_3_Balidazio_Metodologia.pdf](<../../03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf>) — pp. 4–6: sujeto/grupo y leakage; apoyo del módulo 5072 |

| P3 | Métricas, classification_report e interpretación | [Moodle_page_64153.md](<../../04_Programazioa_5073/materialak/Moodle_page_64153.md>) — checklist: Metriken Interpretazioa<br>[5073_3_Programazioa.pdf](<../../04_Programazioa_5073/materialak/5073_3_Programazioa.pdf>) — pp. 10–12: accuracy, precision, recall, F1 y matriz |

| P4 | BaseModel, field_validator e inferencia | [Moodle_page_64153.md](<../../04_Programazioa_5073/materialak/Moodle_page_64153.md>) — checklist: API Eskemak<br>[5073_3_Programazioa.pdf](<../../04_Programazioa_5073/materialak/5073_3_Programazioa.pdf>) — pp. 14–15: orden de inferencia; pp. 29–30: esquema y validación |


## bigdata

Big Data e ingeniería de datos.

| Apartado | Materia evaluada | Fuente y pasaje |
|---|---|---|

| 1 | 7 V, analítica y OLTP/OLAP | [01_01_big_data_sarrera.pdf](<../../05_BigData_Ingeniaritza/materialak/01_01_big_data_sarrera.pdf>) — pp. 5–16: 7 V (Viability), analítica y OLTP/OLAP<br>[Ariketak_01_01_big_data_sarrera.md](<../../05_BigData_Ingeniaritza/materialak/Ariketak_01_01_big_data_sarrera.md>) — 7 V-ak kasu errealetan; Analitika motak; OLTP ala OLAP |

| 2 | Ciclo de ingeniería, hardware, abstracciones y ETL/ELT | [Ariketak_01_02_datuen_ingeniaritza.md](<../../05_BigData_Ingeniaritza/materialak/Ariketak_01_02_datuen_ingeniaritza.md>) — Datuen bizi-zikloa (cinco fases); Hardware fisikoa; Smart Factory; ETL ala ELT?<br>[01_02_datuen_ingeniaritza.pdf](<../../05_BigData_Ingeniaritza/materialak/01_02_datuen_ingeniaritza.pdf>) — pp. 5–9 y 19–28: ciclo, HDD/SSD/RAM, cache y ETL/ELT |

| 3 | ETL de ventas, formatos y Faker | [Ariketak_01_02_datuen_ingeniaritza.md](<../../05_BigData_Ingeniaritza/materialak/Ariketak_01_02_datuen_ingeniaritza.md>) — ETL prozesua diseinatu; Zein formatu aukeratuko zenuke?; Faker-ekin lehen dataset-a; Zer egiten du seed-ak?; CSV JSON |

| 4 | Mapping, consultas, agregaciones y Kibana | [02_elastic_stack.pdf](<../../05_BigData_Ingeniaritza/materialak/02_elastic_stack.pdf>) — pp. 14–20, 24–29 y 31–41: mapping, shards, filtros, agregaciones y Lens |

| 5 | Stack, Grok e ILM | [02_elastic_stack.pdf](<../../05_BigData_Ingeniaritza/materialak/02_elastic_stack.pdf>) — pp. 3–8: componentes; pp. 42–44: ILM y práctica 8; pp. 62–67: Grok y conversión |


## nifi

NiFi y series temporales.

| Apartado | Materia evaluada | Fuente y pasaje |
|---|---|---|

| 1 | FlowFile, conexiones, servicios y provenance | [01_01_ApacheNifi.pdf](<../../06_NiFi/materialak/01_01_ApacheNifi.pdf>) — pp. 10–13 y 24: atributos, colas, back pressure, provenance y Reader/Writer |

| 2 | CSV/JSON, ConvertRecord, QueryRecord y destinos | [01_02_ApacheNifi_aurreratua.pdf](<../../06_NiFi/materialak/01_02_ApacheNifi_aurreratua.pdf>) — pp. 18–21: ConvertRecord, Reader/Writer y UpdateAttribute<br>[GIDA Apache NiFi instalazioa eta kasu praktikoak 1-2-3-4.pdf](<../../06_NiFi/materialak/GIDA Apache NiFi instalazioa eta kasu praktikoak 1-2-3-4.pdf>) — pp. 13–26: CSV, QueryRecord y comprobación del recorrido |

| 3 | MariaDB/MongoDB y capas HTTP/Bronze/Silver/Gold | [01_02_ApacheNifi_aurreratua.pdf](<../../06_NiFi/materialak/01_02_ApacheNifi_aurreratua.pdf>) — pp. 29–34: DBCP, ExecuteSQLRecord, SplitText, PutMongo; pp. 38–50: InvokeHTTP, capas, MergeContent y QueryRecord<br>[Apache NiFi kasu praktikoak (5-6-7).pdf](<../../06_NiFi/materialak/Apache NiFi kasu praktikoak (5-6-7).pdf>) — pp. 25–34: caso 7 de capas y comprobación de salidas |

| 4 | Tiempo, resample, interpolación, rolling, alerta y gráfico | [02_Denbora_Serieak.pdf](<../../06_NiFi/materialak/02_Denbora_Serieak.pdf>) — pp. 25–36: Pandas y práctica (incluidos gráfico e interpretación); p. 37: tres lecturas consecutivas |

| 5 | Volumen, pérdida de picos y agregaciones | [02_Denbora_Serieak.pdf](<../../06_NiFi/materialak/02_Denbora_Serieak.pdf>) — p. 23: 20 máquinas, dos sensores y volumen; p. 38: max/min/conteo/kWh de intervalo |


## kafka

Kafka básico y avanzado.

| Apartado | Materia evaluada | Fuente y pasaje |
|---|---|---|

| 1 | Topic, particiones, key, broker y bootstrap | [01_03_ApacheKafka.pdf](<../../07_Kafka/materialak/01_03_ApacheKafka.pdf>) — pp. 16–20, 27–28, 33 y 37: conceptos, bootstrap, ISR y key<br>[01_04_ApacheKafka_aurreratua.pdf](<../../07_Kafka/materialak/01_04_ApacheKafka_aurreratua.pdf>) — pp. 8–16: describe, key y listener interno |

| 2 | Grupos, paralelismo, offsets y reentrega | [01_03_ApacheKafka.pdf](<../../07_Kafka/materialak/01_03_ApacheKafka.pdf>) — pp. 42–49: particiones por grupo, consumer config, commits y semánticas<br>[01_04_ApacheKafka_aurreratua.pdf](<../../07_Kafka/materialak/01_04_ApacheKafka_aurreratua.pdf>) — pp. 17 y 34: grupos diferentes para Python/NiFi y destinos independientes |

| 3 | RF, ISR, leader y acks | [01_03_ApacheKafka.pdf](<../../07_Kafka/materialak/01_03_ApacheKafka.pdf>) — pp. 32–33 y 37: replicación, leader/ISR, min.insync.replicas y acks<br>[01_04_ApacheKafka_aurreratua.pdf](<../../07_Kafka/materialak/01_04_ApacheKafka_aurreratua.pdf>) — pp. 8–9: RF, describe, Replicas e ISR |

| 4 | Capas, lotes, semánticas y equivalente Python/NiFi | [01_04_ApacheKafka_aurreratua.pdf](<../../07_Kafka/materialak/01_04_ApacheKafka_aurreratua.pdf>) — pp. 23–37: capas, tres grupos y diez mensajes; pp. 39–45: EvaluateJsonPath, MergeRecord y QueryRecord<br>[01_03_ApacheKafka.pdf](<../../07_Kafka/materialak/01_03_ApacheKafka.pdf>) — pp. 48–49: commits, duplicados e idempotencia conceptual |

| 5 | Connect, source/sink, worker/task y comprobación | [01_04_ApacheKafka_aurreratua.pdf](<../../07_Kafka/materialak/01_04_ApacheKafka_aurreratua.pdf>) — pp. 47–54: componentes, converters y estado; pp. 56–69: caso 5 MySQL → Kafka → MongoDB y prueba con registros nuevos |
