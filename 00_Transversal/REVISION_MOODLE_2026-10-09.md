# Revisión Moodle: 8 → 9 de octubre de 2026

**Actualización posterior:** se adaptaron las soluciones, se ejecutaron script/notebook y 107 pruebas, y el ciclo de las 08:37 publicó la guía con cobertura completa. Véase [validación del día 9](validaciones_2026-10-09/README.md). Las secciones siguientes conservan el diagnóstico inicial de las 08:12 para distinguir lo detectado de lo resuelto después.

Revisión local y lectura autenticada de la página 64153. Corte del sincronizador: ciclo terminado el 9 de octubre a las 08:12 CEST. Comparación con el commit local `63da0a9` y las publicaciones remotas del día 8; no se han modificado soluciones ni publicado cambios durante esta revisión.

## Estado y novedades

- Rama de trabajo: `feat/ejercicios-moodle-2026-10-08`. `origin/master` sigue en `f370965`; la resolución local `63da0a9` todavía no está integrada allí.
- Última publicación del sincronizador: `origin/moodle-sync/master/2026-10-08`, `b441fbf6732e` (ciclo de las 12:02 del día 8). A las 11:02 había 77 actividades; después 78; hoy hay 80.
- Ciclo del día 9: cero errores y una fuente manual pendiente. El servicio terminó correctamente, pero omitió commit/push por cobertura incompleta. Eso no significa que los materiales locales estén publicados.
- Los 82 ficheros registrados con SHA-256 coinciden con sus bytes locales. Las 11 actividades de tipo entrega (`assign`) no presentan cambios frente a la base comparada.

| Material | Cambio observado | Consecuencia |
| --- | --- | --- |
| ML, ID 63381 | Enlace a «15 Most Commonly Used ML Algorithms», incorporado ayer al mediodía | Referencia de estudio; no es una nueva entrega |
| Programación, ID 64542, `3_SOLUZIOAK_URLa.ipynb` | Nuevo cuaderno docente de soluciones; conserva los ejercicios numerados del cuaderno anterior y añade conclusiones y ejemplos de los apuntes | Contrastar explicaciones y ejemplos con las soluciones propias; su descarga no demuestra ejecuciones propias |
| Programación, `3_Adibide_koadernoa_URLa.ipynb` | El ejemplo Streamlit añade `seaborn` y realiza predicción y muestra probabilidades donde antes mostraba un mensaje de demostración | Revisar la nueva lógica si se utiliza este ejemplo; solo solicita cinco variables y completa las demás con medias del dataset completo |
| NiFi, ID 64556, `02_Denbora_Serieak.pdf` | Práctica industrial ampliada y organizada en 19 pasos, con comprobaciones e interpretación | Actualizar la solución anterior y verificarla contra este enunciado |
| Moodle, página ID 64153 | «AZTERKETA PRESTATZEKO GIDA» | Nueva guía de examen; actualmente bloquea la publicación automática porque el sincronizador marca las páginas como revisión manual |

## Series temporales: diferencias concretas por atender

La solución existente en `06_NiFi/soluzioak/08_Denbora_Serieak/` documenta nueve tareas Pandas de la versión anterior. Ya explica que 85.2 °C puede ser un error o un evento real y que no debe borrarse automáticamente; esa aclaración del nuevo PDF está cubierta.

Pendientes comprobados al comparar el nuevo PDF con el script:

1. Usar el intervalo solicitado **2026-10-01 08:00–09:00** y mostrar sus datos y su media. El script actual selecciona 01:00–02:00, semiabierto, y no muestra la media del intervalo. Declarar la semántica de los extremos; el ejemplo docente usa `.loc` inclusivo.
2. Mostrar la forma del dataset y el número de filas resultantes de resample, además de los asserts internos existentes.
3. Crear `tenperatura_beteta` mediante interpolación temporal y calcular `tenperatura_leundua` sobre esa columna. Actualmente interpola con `linear` y aplica rolling a la serie original antes de interpolarla. En datos regulares puede coincidir la interpolación, pero la secuencia y nombres no satisfacen literalmente el nuevo enunciado.
4. Mostrar las mediciones superiores a 50 °C de la práctica principal. El filtro actual se aplica a una tabla didáctica separada, no al dataset principal.
5. Completar explícitamente el cálculo de volumen con **100 bytes por medición**, indicando si se cuenta cada valor escalar o un mensaje por máquina y las unidades MB/MiB.
6. Responder junto a los resultados las preguntas nuevas sobre anomalías y la pérdida de picos al reducir a medias de diez minutos. Parte de la interpretación ya existe; debe vincularse a los resultados de la práctica actualizada.
7. Actualizar README, notebook y evidencias después de ejecutar la versión adaptada. Sigue sin estar disponible el `sentsorea.csv` docente: cualquier sustituto sintético debe conservar su declaración y sus límites.

El PDF contiene `sort_intex()` en una diapositiva: es una errata; corresponde `sort_index()`.

## Página 64153: contenido verificado

URL: https://elearning20.hezkuntza.net/012053/mod/page/view.php?id=64153

Guía de preparación del examen de la primera erronka: menciona convocatoria de febrero y convocatorias oficiales de junio; no anuncia un examen inmediato de octubre.

- Teoría: 3 puntos, 30 preguntas de test, penalización por respuestas incorrectas, sin apuntes ni ordenador.
- Práctica: 7 puntos, problema contextualizado y CSV sucio a resolver en Jupyter. PDF de clase disponibles en la máquina virtual; sin Internet ni asistentes LLM/IA.
- Competencias: list comprehensions, limpieza y filtros Pandas, Pipeline de scikit-learn, `class_weight='balanced'`, justificación de Recall e interpretación de classification report/confusion matrix, Pydantic `BaseModel` y `@field_validator`.
- Incluye cinco preguntas de autoevaluación y respuestas. No es una actividad de entrega nueva.

La lectura manual confirma qué contiene, pero **no modifica** el estado de cobertura del manifiesto. Para desbloquear la publicación habrá que incorporar una representación local verificable de esta fuente y su seguimiento en el sincronizador, o resolver explícitamente la política de cobertura; no eliminar la advertencia sin esa evidencia.

## Trabajo anterior que permanece pendiente

- Publicar y revisar la rama de soluciones del día 8; el commit local no equivale a merge ni a entrega en Moodle.
- Decisiones y evidencias humanas de CNC/equipo, IDE y trabajo colaborativo; no se pueden completar inventando participantes o capturas.
- Cuadernos docentes de ética aún ausentes: fairness hospital, SHAP/LIME compliance y ALTAI. Las nuevas fuentes de hoy no los sustituyen.
- Validaciones dependientes de credenciales o servicios: Gemini/RAG, AEMET, Canvas de NiFi; comparación MariaDB y benchmark repetido pendientes según el informe anterior.
- La variante Open-Meteo no acredita el proveedor original el-tiempo.net. Los artefactos Orange/SVM tampoco acreditan entregas en Moodle.

Pruebas anteriores: consultar `validaciones_2026-10-08/README.md`; sus 92 tests corresponden a la ejecución del día 8. Esta revisión verifica fuentes, diferencias y hashes; no vuelve a certificar con aquellos tests la práctica modificada hoy.
