# Revisión documental de ejercicios — 2026-10-01

Esta revisión mejora las soluciones existentes para estudiarlas sin explicaciones
externas. Incluye los siete módulos, prácticas complementarias, soluciones
guardadas en `materialak/`, y orientación del archivo antiguo. Los symlinks y
parejas `.py/.ipynb` no cuentan como ejercicios distintos. La
[auditoría de cobertura](AUDITORIA_EJERCICIOS.md) identifica los enunciados y
entregas; este documento registra claridad, uso y límites de la documentación.

**Se ha revisado documentación y código para describir su comportamiento; no
se han vuelto a ejecutar todos los ejercicios o laboratorios.** Las mejoras
no certifican corrección técnica exhaustiva ni convierten una plantilla o código
preparado en una entrega realizada. Los cambios previos del árbol de trabajo
se han conservado.

## Cobertura y cambios

| Familia revisada | Hallazgo documental y resultado | Entrada para estudiar |
|---|---|---|
| CNC Guard: prototipo, resumen y anexos | El resumen mezclaba objetivos y componentes propuestos con el prototipo. Se distingue Mamdani/Isolation Forest implementados de LSTM/RAG/conectores propuestos y se explican límites de datos sintéticos. Las plantillas ya identifican campos humanos pendientes. | [Guía de soluciones](../01_Erronka1_CNC_Guard/soluzioak/README.md) y [proyecto ejecutable](../01_Erronka1_CNC_Guard/proyecto_cnc_guard/README.md). |
| PERT/Gantt de tortilla | La solución ya desarrolla supuestos, precedencias, tablas y respuestas. Se añade un recorrido para comprobar el camino crítico y recursos. | [Solución](../01_Erronka1_CNC_Guard/soluzioak/Patata_Tortila_PERT_Gantt_Ebazpena.md). |
| 5071: IE1, ética, IE6 y presentación | Respuestas extensas con hipótesis y fuentes. Se añade orden de lectura/comprobación y se corrige la afirmación de PPTX ausente: el archivo existe. No se renuevan fuentes jurídicas ni se inventa entrega personal. | [Guía 5071](../02_AA_Ereduak_5071/soluzioak/README.md). |
| COMPAS en `materialak/` | La versión actual descarga por HTTPS y usa umbral 7; no coincide con la descripción antigua de CSV local/umbral 5. Se añade contexto junto al notebook y guía de métricas, denominadores y límites. **Resultados pendientes de reconciliar.** | [Guía COMPAS](../02_AA_Ereduak_5071/materialak/Alborapenak/README.md). |
| AI Act, notebook de tabla | El título «SOLUZIOA» no significa tabla rellenada. Se dirige al desarrollo de IE6 y se deja visible su carácter incompleto. | [Guía 5071](../02_AA_Ereduak_5071/soluzioak/README.md). |
| ML básico sobre CNC | Solo había una celda de texto para seis bloques de código. Se explican entradas, preprocesamiento, baseline, MSE/R², desbalance y F1 junto a cada bloque y en los comentarios del `.py`. Se corrige el comentario que negaba los NaN. | [Notebook](../03_ML_5072/soluzioak/5072_ML_praktika.ipynb) y [guía ML](../03_ML_5072/soluzioak/README.md). |
| Orange: Auto MPG, Heart Disease y WDBC | Se añade entorno independiente de CNC, forma de abrir File/workflows, salidas regeneradas, métricas/unidades y distinción ajuste completo/CV. Las guías de datos conservan procedencia y metodología. | [Guía ML](../03_ML_5072/soluzioak/README.md), [Auto MPG](../03_ML_5072/soluzioak/datos/auto_mpg/README.md), [WDBC](../03_ML_5072/soluzioak/datos/breast_cancer_wisconsin/README.md). |
| Iris LogReg/KNN 2D | Falta de guía y accuracy presentada sin indicar entrenamiento. Nueva guía de datos, ejecución, PNG y fronteras; el informe declara que train=evaluación y no compara generalización. | [Guía Iris 2D](../03_ML_5072/soluzioak/Iris_LogReg_KNN/README.md). |
| Iris KNN en Orange | Se explican cuatro features, File, CV y matriz. El CSV de predicciones tiene **90/150 etiquetas reales desalineadas** respecto a sus medidas; la guía marca las cifras como pendientes de reconciliación. | [Informe y advertencia sobre resultados](../03_ML_5072/soluzioak/Orange_KNN_Iris.md). |
| Programación: cuaderno de lenguajes | No había README y el código tenía sobre todo enunciados/asserts. Se añaden guía de entradas/salidas y explicación de **cada uno de los 25 ejercicios** en notebook y `.py`. Se documenta `uv --clear`, staging Git y pickle propio. | [Guía del bloque 01](../04_Programazioa_5073/soluzioak/01_Lengoaiak_Ariketak/README.md). |
| Programación: cuaderno de datos | No había README ni explicación del método por ejercicio. Se añaden **25 explicaciones** en ambos formatos, preparación y lectura de gráficos. Se aclara que hay 9 múltiplos de 3 tras introducir cuatro ceros y que no se exporta CSV limpio/PNG. | [Guía del bloque 02](../04_Programazioa_5073/soluzioak/02_Datu_Zientzia_Ariketak/README.md). |
| PDF de lenguajes y variantes | La guía presuponía `.venv` y describía dependencias mínimas como versiones exactas. Se añade preparación desde raíz, efectos reales, límites de Git/equipo y criterios de comprobación. La narrativa de ejercicios ya estaba desarrollada. | [Guía del bloque 03](../04_Programazioa_5073/soluzioak/03_Lengoaiak_PDF_Ariketak/README.md). |
| PDF de datos, CSV nuevo, notas y variantes | Se añaden entorno, entradas/salidas por variante, recurso `tips` local, importación con efectos, DVC temporal, coste y límites del benchmark y correlación. Tres notebooks auxiliares reciben contexto de uso; se documenta el fallback absoluto de CSV. | [Guía del bloque 04](../04_Programazioa_5073/soluzioak/04_Datu_Zientzia_PDF_Ariketak/README.md). |
| PDF de frameworks: 26 ejercicios | Se amplía cada explicación en el notebook y comentarios junto a sus funciones. La guía distingue funciones calculadoras de funciones que devuelven instrucciones; las llamadas externas comentadas no acreditan ejecución. | [Guía del bloque 05](../04_Programazioa_5073/soluzioak/05_Frameworkak_PDF_Ariketak/README.md). |
| Cuaderno ML/API y ampliaciones Drive | El README omitía imbalanced-learn/Matplotlib y afirmaba igualdad completa `.py/.ipynb`. Se documentan los 25 ejercicios base, SMOTE/PR/umbral/GridSearch y request 6.1 que solo están en el script, con IDs reutilizados. Se amplía narrativa del notebook. | [Guía del bloque 06](../04_Programazioa_5073/soluzioak/06_Programazioa_Ariketak/README.md). |
| Git 4.2, 10M y cuadernos fuente de Drive | Nueva guía Git y enlaces desde programación a datasets/experimento incremental. Los cuadernos descargados conservan el texto docente y convenciones de Colab; se orienta a las guías locales según variante. | [Mapa de programación](../04_Programazioa_5073/soluzioak/README.md). |
| Big Data: 7V, ingeniería, Faker | Las respuestas ya desarrollan razonamientos. Nueva entrada común separa respuestas escritas de generadores; la guía Faker explica seed, esquema y archivos sobrescritos. | [Guía de ingeniería](../05_BigData_Ingeniaritza/soluzioak/README.md). |
| Elastic P1–P14 y Kibana | Nueva guía de recorrido, requisitos, efectos de recrear índices, métricas de paneles y comprobación de Inspector/filtros. Se enlazan las entregas y registros ya existentes sin presentarlos como nueva ejecución. | [Guía Elastic](../05_BigData_Ingeniaritza/soluzioak/03_Elastic_Stack/README.md). |
| NiFi: siete casos y once flows | Las guías ya contienen topología/configuración; se añaden vocabulario, secuencia y criterios de aceptación por caso. Casos 3, 5 y 6 reciben pasos de comprobación complementarios. Se distinguen simulación, conectividad y ejecución de flujo. | [Guía NiFi](../06_NiFi/soluzioak/README.md). |
| Kafka: consola, Python, clúster y Connect | Se añaden enlaces a 5–11/casos avanzados, conceptos necesarios para interpretar offsets/ACK/grupos y criterios del recorrido extremo a extremo. La guía conserva el requisito de broker aislado. | [Guía Kafka](../07_Kafka/soluzioak/README.md). |
| Archivo y symlinks | Orientación explícita a rutas actuales; las copias conservadas no reciben soluciones duplicadas ni se presentan como versiones recomendadas. | [Archivo histórico](../_archivo_legacy/README.md). |

## Incidencias que la documentación no resuelve por sí sola

1. **Iris Orange — incorrecto el emparejamiento del export:** la entrada Iris
   contiene las 150 medidas y etiquetas correctas; al contrastar cada fila del
   CSV de predicciones con Iris de scikit-learn, 90 `iris_real` no corresponden
   a sus features. No basta con que matriz y suma de `acierto` coincidan.
   Hace falta regenerar el export y reconciliar métricas, informe/PDF y workflow.
   En esta revisión no se alteran los datos/artefactos previos.
2. **COMPAS — dudoso/no validado:** umbral/fuente del código actual difieren de
   la auditoría anterior. Recalcular y contrastar tabla, filtros, outputs y
   conclusiones antes de entregar; las cifras preescritas no son resultados nuevos.
3. **Notebooks con `__file__` — limitación de ejecución:** ML básico y PDF de
   datos tienen rutas propias de script; las guías indican usar el `.py` o
   adaptar la ruta al kernel. Añadir texto no corrige esa incompatibilidad.
4. **Versiones de programación — incompleto el espejo ejecutable:** el notebook
   base del tema 3 no contiene las ampliaciones del `.py`; se documenta la
   diferencia. Un futuro sincronizador debe conservar texto y evitar colisiones
   de IDs entre ediciones.
5. **Laboratorios/APIs — no validados de nuevo:** NiFi/AEMET conserva pendientes
   de mapeo/runtime; Kafka, Elastic y APIs mantienen sus límites y registros
   históricos. Esta revisión no crea evidencia industrial, GUI, cloud ni de equipo.

## Verificación de los cambios documentales

Se contrasta el árbol final con una instantánea tomada antes de editar:

- Árbol sintáctico (`ast.parse`/`ast.dump`) de los `.py` modificados: cambios
  de comentarios, sin alterar instrucciones ejecutables.
- Celdas de código, salidas y `execution_count` de notebooks modificados:
  conservados respecto al inicio de esta revisión.
- Validación estructural `nbformat` y exportación HTML sin ejecución para
  comprobar que la narrativa añadida se renderiza.
- Destinos de enlaces Markdown locales en documentos modificados/nuevos.
- `git diff --check` para formato del diff.

**Resultado observado:** 9 notebooks válidos y 9 exportaciones HTML con la
narrativa añadida presente; 745 enlaces locales con destinos existentes;
`git diff --check` sin errores. Cuatro `.py` han cambiado únicamente en
comentarios; código, outputs y contadores de las nueve parejas notebook
modificadas se conservan frente a la instantánea inicial. La exportación
comprueba el texto renderizado, no una nueva inspección visual de los gráficos.

Las pruebas de resultados son las descritas en cada práctica. No se ejecutan
notebooks que sobrescriban datos, scripts de laboratorios ni llamadas externas
solo para comprobar una mejora de texto. Los PNG/PDF derivados conservan su
versión anterior: lee las correcciones y límites de sus guías junto a ellos.

## Cómo mantener una solución autoexplicativa

[CONTRIBUTING.md](../CONTRIBUTING.md) incorpora el criterio: enunciado/variante,
objetivo, datos, preparación desde una carpeta explícita, razonamiento junto
al código, salidas, comprobación e interpretación, y límites/evidencia.
Una guía debe describir lo que hace **su versión actual**, en lugar de depender
de un entorno local previo o de explicaciones conservadas solo en conversación.

## Comprobaciones para publicación

La preparación de la PR verifica el contenido del índice Git en una copia
aislada: nueve notebooks válidos, enlaces locales sin destinos ausentes y
sintaxis Python correcta. Gitleaks no detecta secretos en el parche.
El script ampliado de Programación se ejecutó en esa copia: SMOTE en train
equilibró 1434/1434 ejemplos; recall RF pasó de 0.7317 a 0.8293 al bajar el
umbral a 0.30. Esta ejecución del script no valida las celdas del notebook
ni los workflows Orange o el estado actual de los servicios externos.
