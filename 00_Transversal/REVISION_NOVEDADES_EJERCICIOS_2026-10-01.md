# Revisión de novedades y ejercicios pendientes · 2026-10-01

Comprobación autenticada de Moodle y los recursos enlazados de Drive: **13 secciones, 70 actividades, 10 tareas de entrega, 0 errores y 0 recursos inaccesibles**. No se detectaron archivos nuevos ni hashes remotos cambiados respecto a `MOODLE_SYNC_ESTADO.json` local de hoy. El registro histórico de septiembre tenía 55 actividades: ese crecimiento ya está incorporado, no es una nueva descarga pendiente.

La comprobación se hizo en una copia temporal, con `--no-publish`, conservando los archivos locales. Se leyeron además los enunciados de las diez tareas: algunas no tienen adjuntos y no aparecen como archivos en el manifiesto. No se consultaron entregas personales ni calificaciones; **existencia de solución local no confirma entrega en Moodle**. Esta revisión comprueba cobertura y documentación, no reejecuta los ejercicios.

## Tareas Moodle fuera de CNC Guard

| Tarea y fuente | Cobertura local | Qué queda por hacer |
|---|---|---|
| [Interpretar datos, 63638](https://elearning20.hezkuntza.net/012053/mod/assign/view.php?id=63638) | Hay análisis y gráficos reutilizables en las prácticas Orange, pero no una entrega específica identificada en la auditoría. | Preparar un PDF con **Introducción, Desarrollo con capturas de pantalla y Conclusiones**, usando un dataset y una gráfica de Orange. El enunciado permite elegir dataset; la falta de dataset asignado no bloquea empezar. |
| [Regresión lineal, 63319](https://elearning20.hezkuntza.net/012053/mod/assign/view.php?id=63319) | [PDF Auto MPG](../03_ML_5072/soluzioak/Orange_Erregresio_Lineala_Entregagarria.pdf) y workflow existentes. | Revisar presentación final y comprobar entrega personal en Moodle. No se identificó una solución nueva necesaria por cambios del enunciado. |
| [Regresión logística, 63320](https://elearning20.hezkuntza.net/012053/mod/assign/view.php?id=63320) | [PDF WDBC](../03_ML_5072/soluzioak/Orange_Regresion_Logistica_Entregable.pdf) y workflow existentes. | Igual: revisión final y entrega personal, sin novedad del enunciado detectada. |
| [KNN, 63321](https://elearning20.hezkuntza.net/012053/mod/assign/view.php?id=63321) | Workflow y PDF Iris existentes. **Dudoso como entrega final**: 90 de 150 etiquetas reales del CSV de predicciones no corresponden a sus características; [detalle](../03_ML_5072/soluzioak/Orange_KNN_Iris.md). | Regenerar predicciones conservando el vínculo fila→etiqueta, recalcular métricas y actualizar PDF/gráficos a partir de esa misma ejecución. No basta con que la matriz tenga totales coherentes. |
| [LogReg vs KNN Jupyter, 63325](https://elearning20.hezkuntza.net/012053/mod/assign/view.php?id=63325) | [Script, figura e informe](../03_ML_5072/soluzioak/Iris_LogReg_KNN/README.md) existentes y ajustados al código de partida. | Hay una solución `.py`, no un notebook resuelto en esa carpeta. Preparar la versión `.ipynb` si se entrega en formato Jupyter. Sus accuracies son de entrenamiento; no presentarlas como validación cruzada. La introducción Moodle solo enlaza notebook y plantilla, sin fijar explícitamente extensión de entrega. |
| [Árbol de Decisión, 63544](https://elearning20.hezkuntza.net/012053/mod/assign/view.php?id=63544) | Omitido en la matriz anterior. El [workflow Heart Disease](../03_ML_5072/soluzioak/Orange_Bihotza_Ereduak.ows) y el script comparativo incluyen este modelo. Cobertura parcial, resultados del PDF no validados. | Reutilizar código y workflow, ejecutar y exportar resultados reales, regenerar informe. La tarea tiene introducción vacía: no atribuirle requisitos específicos adicionales. El PDF docente contiene ejemplos, no un nuevo listado numerado de ejercicios. |
| [Random Forest, 63386](https://elearning20.hezkuntza.net/012053/mod/assign/view.php?id=63386) | También omitido; mismo workflow y script Heart Disease como base. Cobertura parcial, resultados del PDF no validados. | La misma ejecución comparativa puede cubrir ambos modelos; separar conclusiones y asociarlas a cada tarea. La introducción también está vacía. No hay motivo para empezar código desde cero. |

**Hallazgo que afecta a Árbol/Random Forest:** `irudiak/sortu_irudiak.py` incluye métricas escritas a mano y construye curvas ROC mediante fórmulas (`1-(1-fpr)**exponente`), sin cargar predicciones de CV. `sortu_pdf_txostena.py` también contiene valores numéricos literales. El script `orange_bihotza_ereduak.py` calcula CV real pero imprime resultados, y no alimenta automáticamente esos generadores. Por ello el PDF existente no prueba esas cifras ni esas ROC. Hay que conectarlo con una ejecución reproducible antes de dar ambas tareas por cerradas.

## Otros pendientes ya conocidos

- **Programación:** las ampliaciones Drive de SMOTE, umbral, GridSearch y petición 6.1 ya tienen código en [06_Programazioa_Ariketak](../04_Programazioa_5073/soluzioak/06_Programazioa_Ariketak/README.md); el notebook conserva la edición anterior. Queda sincronizar la entrega notebook. Las actividades de compañeros/PR/presentación requieren evidencia real del trabajo de clase; los ejemplos no la sustituyen. Streamlit/GUI y Gemini/RAG mantienen límites de validación indicados en la auditoría.
- **AA, ética:** las referencias a notebooks 3.1, 6.1 y 12.0 siguen sin esos materiales identificados en el repositorio. Hay respuestas conceptuales, pero no cálculos verificables del notebook ausente. Acuerdos y aportaciones de compañeros se completan en clase. COMPAS necesita reconciliar resultados guardados con el código de la versión actual; [guía](../02_AA_Ereduak_5071/materialak/Alborapenak/README.md).
- **NiFi:** los casos parciales siguen necesitando evidencia runtime/GUI. En AEMET faltan configuración y mapping del payload real. Son pendientes de validación y finalización, no nuevas tareas detectadas hoy. No se modificó el stack.
- **Elastic/Kafka:** hay entregables y registros de ejecución previos para las series actualizadas; no se detectaron nuevos archivos remotos hoy. No se repitieron esas ejecuciones durante esta revisión.

## Orden de trabajo recomendado

1. Corregir la entrega **KNN Iris**, porque un artefacto presentado como resuelto contiene una desalineación concreta.
2. Cerrar **Árbol de Decisión y Random Forest** con una ejecución común y resultados trazables, reutilizando Heart Disease.
3. Preparar el **PDF de interpretación de datos** con capturas reales de Orange.
4. Completar las versiones **Jupyter** de Iris y las ampliaciones de Programación; después resolver evidencias de clase y validaciones pendientes según la planificación docente.

**CNC Guard queda aplazado por indicación del usuario, que lo sitúa dentro de una semana.** Sus tres tareas Moodle no forman parte de esta prioridad. No se ha creado una fecha nueva de entrega ni se ha avanzado el proyecto.

La comparación remota encontró tres archivos diferentes del contenido local: COMPAS y dos CSV docentes de Programación. Sus hashes remotos coinciden con el manifiesto ya existente: son diferencias locales, no actualizaciones nuevas. Se conservaron sin sobrescribirlos. La parte de horarios eliminada por privacidad no se ha recuperado.
