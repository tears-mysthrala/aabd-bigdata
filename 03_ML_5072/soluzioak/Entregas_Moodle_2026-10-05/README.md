# Entregas Moodle preparadas el 05/10/2026

Seis trabajos preparados individualmente, más una revisión de AI4I con capturas auténticas de Orange. Erronka1/CNC Guard queda fuera de este lote. Regresión lineal conserva su informe anterior.

| Tarea | Contenido | Carpeta autónoma |
|---|---|---|
| 63638 Interpretación | AI4I sintético: carga, gráficos, interpretación y conclusiones; PDF de cuatro páginas | [AI4I](63638_Interpretacion_AI4I/README.md) |
| 63320 Logística | WDBC, predictor `texture_mean`, normalización dentro de cada fold y evaluación de diez folds | [Logística](63320_Regresion_Logistica/README.md) |
| 63321 KNN | Iris, cuatro variables, k=3 y evaluación de diez folds | [KNN](63321_KNN/README.md) |
| 63325 Jupyter | Plantillas completadas: Iris con dos variables, notebook ejecutado, Markdown e imagen | [Jupyter](63325_Jupyter_LogReg_KNN/README.md) |
| 63544 Árbol | Iris, modelo, árbol explicativo y evaluación de diez folds | [Árbol](63544_Arbol_Decision/README.md) |
| 63386 Random Forest | Iris, 100 árboles, semilla 42 y evaluación de diez folds | [Random Forest](63386_Random_Forest/README.md) |
| 63380 SVM | Iris, kernel RBF, escalado dentro de cada fold y evaluación de diez folds | [SVM](63380_SVM/README.md) |

## Qué entregar

Los archivos están separados por ID en [para_subir/](para_subir/README.md). Cada tarea Orange tiene un PDF principal y un ZIP con flujo `.ows`, datos, capturas, salidas y reproducción. Jupyter incluye además notebook, informe Markdown e imagen directamente. El [ZIP conjunto](Trabajos_Moodle_2026-10-05.zip) sirve para trasladar todo el lote; los ZIP individuales corresponden a sus tareas respectivas.

El [manifiesto](entregas_manifest.json) registra los tamaños y SHA-256 de cada archivo. Los paquetes respetan los límites consultados de 50 MB por archivo y 20 archivos por tarea. `python3 preparar_paquetes.py` reconstruye los ZIP a partir de las siete carpetas enumeradas, sin conectar con Moodle. No incluye entornos Python, cachés ni archivos personales de autenticación.

Desde esta carpeta, `python3 verificar_paquetes.py` contrasta todos los hashes, el contenido exacto de los ZIP, los manifiestos internos y el número de páginas con Poppler. Escribe [el resultado del control](verificacion_paquetes.json); no vuelve a ejecutar modelos ni certifica por sí solo la revisión visual o el funcionamiento de una interfaz.

## Requisitos y límites

La [revisión del enunciado publicado](../../../00_Transversal/REVISION_ENTREGAS_MOODLE_SIN_ERRONKA1_2026-10-05.md) conserva la fuente y los criterios. Árbol, Random Forest y SVM tenían introducción vacía y ningún adjunto ni rúbrica visible: se adopta expresamente la estructura académica de las otras prácticas (datos, modelo, salidas, interpretación y conclusiones). No se afirma satisfacer criterios que el profesor no haya publicado.

Las capturas Orange proceden de widgets nativos mostrados y capturados con Qt. Los flujos y sus rutas relativas se comprueban por separado. La exactitud de Jupyter se mide sobre entrenamiento porque así lo plantean las plantillas; los demás clasificadores se evalúan con predicciones fuera de cada fold. No deben compararse esas cifras como si fueran el mismo experimento.

Los informes nuevos se renderizan y revisan por páginas. Cada carpeta explica cómo repetir su ejecución y qué controles se hicieron. Un PDF regenerado necesita una nueva revisión visual. Los archivos están preparados localmente: no constituyen evidencia de envío, recepción ni calificación en Moodle.
