# Revisión de trabajos tras recuperar la descarga · 9 de octubre

Se revisan las fuentes añadidas/modificadas respecto a `f370965` (integración
anterior) y el ciclo automático de las **10:00–10:02 CEST**. La guía de examen
había quedado descargada, sin una solución asociada: esa cobertura era incompleta.
El usuario ha confirmado que Moodle 64153 es el mock al que se refería.

| Fuente | Requisitos y estado de la solución |
| --- | --- |
| [Guía de examen 64153](../04_Programazioa_5073/materialak/Moodle_page_64153.md) | **Completado para preparación**: cinco preguntas justificadas y práctica propia que recorre las seis habilidades. [Enunciado y solución](../04_Programazioa_5073/soluzioak/09_Mock_Azterketa_64153/README.md). La guía no incluye las 30 preguntas reales ni un CSV específico: no se inventan. |
| [Series temporales](../06_NiFi/materialak/02_Denbora_Serieak.pdf) | La práctica principal de 19 pasos ya estaba adaptada. El PDF recibido a las 10:02 pasa de 38 a 41 páginas y añade **dos retos y cinco preguntas de repaso**, ahora [resueltos y ejecutados](../06_NiFi/soluzioak/08_Denbora_Serieak/retos_adicionales.ipynb). |
| [Cuaderno 3 de soluciones docentes](../04_Programazioa_5073/materialak/3_SOLUZIOAK_URLa.ipynb) | Comparado con la solución propia: GridSearch, explicación de métricas, parámetros, Pydantic y contrato de probabilidad corregidos y ejecutados. [Contraste](../04_Programazioa_5073/soluzioak/07_Moodle_2026-10-06/CONTRASTE_DOCENTE_2026-10-09.md). Se conserva la fuente docente. |
| [Cuaderno 3 de ejemplos](../04_Programazioa_5073/materialak/3_Adibide_koadernoa_URLa.ipynb) | Actualización de apoyo API/Streamlit revisada; limitaciones de relleno de variables y comandos documentadas. Las variantes propias están en [Frameworks](../04_Programazioa_5073/soluzioak/05_Frameworkak_PDF_Ariketak/README.md) y [Pipeline/API](../04_Programazioa_5073/soluzioak/08_Moodle_2026-10-07/README.md). No se atribuyen los outputs docentes a nuestra ejecución. |
| Dos PDF de Boosting | Cuatro ejemplos Python y tres manuales cubiertos por [solución ejecutada](../03_ML_5072/soluzioak/Boosting/README.md), incluidas comparaciones/limitaciones y prueba de gamma=150. No añaden una rúbrica de entrega separada. |
| PDF Elastic Stack | P18–P22 cuentan con [solución y evidencias reales](../05_BigData_Ingeniaritza/soluzioak/03_Elastic_Stack/novedades_2026-10-08/README.md). La validación sigue rechazando eventos incorrectos con `python -O`. No se confunde revalidar los logs con una nueva ejecución del stack. |
| Registros MOODLE_URLs de Programación/ML | Son índices de fuentes, no ejercicios adicionales. El identificador del vídeo se recuperó en el ciclo fresco de las 09:14–09:16. |

El notebook de nueve modelos en una tienda ficticia fue descargado el **29 de
septiembre**, antes del arreglo reciente: no es el mock confirmado ni un trabajo
nuevo de esta revisión. Se conserva como apoyo; esta revisión no certifica su
benchmark de 300.000 clientes ni la interacción del slider. La nueva galería
visual tampoco sustituye esa ejecución.

## Verificación y límites

El manifiesto cubre **80 actividades y 83 archivos**, con cero errores o fuentes
pendientes de descarga. Se comprobaron los 83 SHA-256 contra el contenido local;
snapshot del ciclo de las 10:02 registrado en
[descargas_recuperadas.json](validaciones_2026-10-09/descargas_recuperadas.json).
«Sin fuentes pendientes» describe la descarga, no la resolución de todos los
ejercicios ni una entrega realizada en Moodle.

Esta revisión añade **13 pruebas aprobadas**: 11 del mock y dos de alertas
temporales. Se ejecutaron los dos scripts y sus notebooks, con cero errores y
AST equivalente; se inspeccionó el gráfico de confusión. Ruff pasó y las
auditorías de ambos entornos no detectaron vulnerabilidades conocidas.
Se conservan las **115 pruebas del cierre anterior** como evidencia histórica,
sin afirmar que todas se hayan repetido localmente en esta revisión.

El mock utiliza el CSV sintético anterior: 100 filas, 96 válidas y solo cinco
errores. Reserva una máquina completa para test: TN=26, FP=11, FN=2, TP=1.
Recall=1/3, precisión=1/12: resultado débil, explicado, sin buscar una semilla o
umbral que lo mejore artificialmente. No demuestra un detector real de averías.
La guía describe un examen sin asistentes; esta solución sirve para prepararlo.

Series sigue pendiente de `sentsorea.csv` docente. La variante sintética tiene
un pico de 65 °C y ningún episodio de tres medidas consecutivas; no permite
diagnosticar averías ni demostrar estacionalidad diaria con tres horas. Continúan
los requisitos humanos, cuentas externas y datasets ausentes del
[informe anterior](validaciones_2026-10-09/README.md). No se realizan entregas.
