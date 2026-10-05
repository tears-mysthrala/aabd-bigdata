# Qué se pide entregar en Moodle, excepto Erronka 1 — 2026-10-05

Última comprobación de las ocho tareas: **2026-10-05 11:51:46 CEST**.

Revisión autenticada del [curso AABD ETHAZI](https://elearning20.hezkuntza.net/012053/course/view.php?id=535), con la sesión de Chromium ya abierta. Se revisaron las doce secciones distintas de la sección 3: **83 actividades contando etiquetas, 66 con enlace y ocho tareas**. La exclusión corresponde al proyecto CNC Guard, sus contratos y propuestas; se incluyen los ejercicios independientes de las asignaturas, aunque sus etiquetas de bloque digan «1. ERRONKA».

Se abrieron por GET las páginas de tarea y sus formularios. Se leyeron enunciados, adjuntos, fechas y restricciones; no se guardaron formularios ni se enviaron trabajos. Los requisitos y hashes locales están en [el inventario JSON](REQUISITOS_ENTREGAS_MOODLE_2026-10-05.json). Este informe recoge requisitos y preparación local; el estado personal de las entregas no se incorpora al repositorio.

## Resultado de la revisión

Hay **cuatro tareas cuyo ejercicio está escrito únicamente en la página Moodle**, **una con plantillas adjuntas** y **tres con introducción vacía**. En las ocho, el formulario ofrece **entrega de archivos**, no un editor de texto online. «Enunciado escrito como texto» no equivale a «respuesta que se pega como texto».

Los formularios muestran **50 MB por archivo y un máximo de 20 archivos**. No muestran una lista de extensiones exigidas; la configuración observada contiene `accepted_types: []`. Ninguna de las ocho páginas muestra fecha límite: las fechas visibles son de **apertura**, no vencimientos. Son las condiciones visibles para esta cuenta en esta comprobación; no se infieren instrucciones orales ni una rúbrica oculta.

| Tarea | Dónde está la consigna | Qué se pide o qué se conoce | Artefactos locales y conclusión |
|---|---|---|---|
| [Interpretación de datos, 63638](https://elearning20.hezkuntza.net/012053/mod/assign/view.php?id=63638) | Texto sin adjuntos | Trabajo individual en Orange: elegir dataset, representar un gráfico, interpretarlo y concluir. **PDF con Introducción, Desarrollo con capturas y Conclusiones**. | [PDF Iris alternativo](../03_ML_5072/soluzioak/Interpretacion_Datos/Interpretacion_Datos_Orange.pdf), [guía y capturas reales](../03_ML_5072/soluzioak/Interpretacion_Datos/README.md). También existe [AI4I](../03_ML_5072/materialak/AI4I_Orange_txostena.pdf), cuyo contenido y figuras se han leído. No se acredita la procedencia GUI de sus imágenes por la mera presencia de figuras. |
| [Regresión lineal, 63319](https://elearning20.hezkuntza.net/012053/mod/assign/view.php?id=63319) | Texto sin adjuntos | Usar Orange y un dataset concreto; explicar selección, aplicar regresión lineal, extraer/analizar salidas y concluir sobre datos/modelo. | [PDF Auto MPG](../03_ML_5072/soluzioak/Orange_Erregresio_Lineala_Entregagarria.pdf), [workflow](../03_ML_5072/soluzioak/Orange_Erregresio_Lineala.ows), [datos](../03_ML_5072/soluzioak/datos/auto_mpg/README.md). El PDF tiene los cuatro apartados. Moodle no exige explícitamente PDF ni capturas para esta tarea. |
| [Regresión logística, 63320](https://elearning20.hezkuntza.net/012053/mod/assign/view.php?id=63320) | Texto sin adjuntos | La misma estructura, aplicando regresión logística en Orange. | [PDF WDBC](../03_ML_5072/soluzioak/Orange_Regresion_Logistica_Entregable.pdf), [workflow](../03_ML_5072/soluzioak/Orange_Regresion_Logistica.ows), [datos](../03_ML_5072/soluzioak/datos/breast_cancer_wisconsin/README.md). El PDF cubre selección, aplicación, salidas y conclusiones. Candidato de entrega documental. |
| [KNN, 63321](https://elearning20.hezkuntza.net/012053/mod/assign/view.php?id=63321) | Texto sin adjuntos | La misma estructura, aplicando KNN en Orange. | [PDF Iris KNN](../03_ML_5072/soluzioak/Orange_KNN_Iris.pdf), [workflow](../03_ML_5072/soluzioak/Orange_KNN_Iris.ows), [guía](../03_ML_5072/soluzioak/Orange_KNN_Iris.md). El PDF cubre la consigna. La ejecución documentada es API Orange; sus figuras no se presentan como capturas GUI, que aquí no se exigen expresamente. |
| [Jupyter LogReg vs KNN, 63325](https://elearning20.hezkuntza.net/012053/mod/assign/view.php?id=63325) | Dos plantillas adjuntas | Notebook Iris con dos medidas del sépalo: completar carga, LogReg `max_iter=200`, KNN `k=3`, fronteras lado a lado y reflexión. Completar el informe con accuracies y respuestas. | [Notebook ejecutado](../03_ML_5072/soluzioak/Iris_LogReg_KNN/iris_logreg_knn.ipynb), [informe](../03_ML_5072/soluzioak/Iris_LogReg_KNN/txostena_beteta.md), [figura](../03_ML_5072/soluzioak/Iris_LogReg_KNN/erabaki_mugak.png). Preparar esos tres juntos; el informe también enlaza código y README, que conviene acompañar o adaptar antes de entregar. |
| [Árbol de decisión, 63544](https://elearning20.hezkuntza.net/012053/mod/assign/view.php?id=63544) | Introducción vacía y sin adjuntos | Existe la tarea y permite subir archivos; **no publica dataset, formato ni rúbrica**. El PDF de teoría muestra ejemplos sklearn de clasificación Iris y regresión Diabetes. | [Informe conjunto Heart Disease](../03_ML_5072/soluzioak/Orange_Data_Mining_Entregagarria.pdf) y [resolución](../03_ML_5072/soluzioak/Heart_Disease_Evaluacion.md). Candidato basado en otro dataset; no se afirma que sea la entrega exigida ni que reproduzca literalmente el PDF de teoría. |
| [Random Forest, 63386](https://elearning20.hezkuntza.net/012053/mod/assign/view.php?id=63386) | Introducción vacía y sin adjuntos | Igual limitación: no publica consigna ni formato. El PDF de teoría incluye ejemplos sklearn sobre datos sintéticos. | El mismo informe Heart Disease compara RF y Árbol. Candidato conjunto; faltan los requisitos concretos del docente para declararlo definitivo. El workflow GUI tiene ajustes distintos del script ejecutado. |
| [SVM, 63380](https://elearning20.hezkuntza.net/012053/mod/assign/view.php?id=63380) | Introducción vacía y sin adjuntos | La tarea acepta archivos, pero no exige explícitamente Orange, PDF, un dataset concreto o una extensión. | [Notebook SVC/SVR ejecutado](../03_ML_5072/soluzioak/SVM/svm_adibideak.ipynb) y [guía](../03_ML_5072/soluzioak/SVM/README.md): ejemplos literales del PDF más extensiones declaradas. Candidato educativo; falta una consigna para cerrar la entrega. |

## Traducción de las instrucciones escritas en Moodle

### Interpretación de datos

Usando Orange, elegir un dataset —o descargarlo— y representarlo en un gráfico. Interpretar lo que aparece y extraer conclusiones. Entregar un **documento PDF con Introducción, Desarrollo con capturas de pantalla y Conclusiones**. Es un ejercicio individual.

### Lineal, logística y KNN

Las tres páginas repiten la misma estructura: aplicar el modelo correspondiente con Orange Data Mining a un dataset concreto; explicar los datos elegidos, aplicar el modelo, obtener y analizar las salidas, y sacar conclusiones sobre los datos y el modelo. El nombre de la tarea determina qué algoritmo se aplica. No se añade un requisito de PDF o capturas que el texto no establece.

Un PDF razonado es una forma adecuada de presentar estos cuatro puntos; se puede acompañar de workflow y datos. Si se entrega un `.ows`, conservar las rutas relativas del dataset en un paquete o explicar cómo seleccionarlo. Un workflow aislado no contiene necesariamente los datos ni las conclusiones.

### Jupyter: lectura de las plantillas

Los dos adjuntos actuales coinciden byte a byte con las copias locales:

- [Notebook docente](../03_ML_5072/materialak/ikaskuntza_gainbegiratua_ikaslea.ipynb): 13 celdas; apartados 1–6.
- [Plantilla del informe](../03_ML_5072/materialak/txostena_ikaslea.md): objetivo, tabla de accuracies, gráfico y tres respuestas sobre setosa, forma de las fronteras y riesgo de overfitting con k pequeño.

El notebook resuelto tiene seis celdas de código ejecutadas y cero salidas de error. Su reflexión responde también al efecto esperado de k=1 y k=50. La pregunta es hipotética: el enunciado no obliga a ejecutar esos dos experimentos. La accuracy está identificada como **entrenamiento**, no test. No se sustituye este ejercicio por el PDF Orange KNN, que usa cuatro atributos y CV.

El Markdown resuelto referencia `erabaki_mugak.png`; si se sube solo el `.md`, faltará la figura. También contiene enlaces de reproducción a `iris_logreg_knn.py` y `README.md`: conservar el conjunto de archivos o preparar una versión autónoma. El formulario admite suficientes archivos; no hace falta convertir automáticamente todos los trabajos en un único PDF.

## Otros módulos y ejercicios

| Sección | Elementos visibles, sin etiquetas | Destino de entrega observado |
|---|---|---|
| Orokorra | 1 recurso | Ninguna tarea de entrega |
| AA Ereduak | 6 recursos y 2 carpetas | Ninguna tarea de entrega |
| Ikaskuntza Automatikorako Sistemak | 12 recursos y 8 tareas | Las ocho tareas de la tabla |
| AA Programazioa | 7 recursos, 13 enlaces y 1 carpeta | Ninguna tarea de entrega |
| BD Sistemak | 6 recursos | Ninguna tarea de entrega |
| BD Aplikatua | 10 recursos | Ninguna tarea de entrega |
| Erronka 0, Erronka 2, Azterketak y Azkenak | Sin tareas ni enlaces nuevos de entrega; etiquetas donde corresponde | Ninguno observado |

Los PDFs/notebooks de Programación, Elastic, NiFi y Kafka contienen ejercicios, pero en este curso no se observó una actividad independiente para subir cada uno. Tener una práctica resuelta no demuestra que exista una entrega separada. La ausencia de portal visible tampoco descarta instrucciones dadas en clase u otro canal.

## Preparación realizada después de la revisión

La tabla anterior conserva los artefactos encontrados durante la consulta. Después se prepararon [siete conjuntos autónomos](../03_ML_5072/soluzioak/Entregas_Moodle_2026-10-05/README.md): AI4I, Logística, KNN, Jupyter, Árbol, Random Forest y SVM. Cada práctica Orange tiene ahora un informe individual con capturas nativas y sus datos, flujo y scripts. Jupyter dispone de notebook ejecutado, informe autónomo, imagen y copia PDF.

Por indicación del usuario se recrearon Árbol, Random Forest y SVM siguiendo la estructura de las tareas con consigna publicada. Sus README declaran el supuesto; sigue sin haber una rúbrica docente visible para contrastarlos. Esta decisión permite preparar trabajos completos sin atribuir instrucciones nuevas al profesor.

Los [archivos para subir, separados por tarea](../03_ML_5072/soluzioak/Entregas_Moodle_2026-10-05/para_subir/README.md) conservan rutas relativas y verificaciones de integridad. La preparación local no acredita envío ni evaluación. Los originales se mantienen, y antes de modificar una entrega existente se debe contrastar su contenido en Moodle.

La revisión y esta preparación no modificaron configuraciones de sincronización ni entregas guardadas. El estado personal se contrastó aparte y no se deduce de la presencia de un PDF local.
