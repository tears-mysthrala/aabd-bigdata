# Especificación: auditoría y resolución de ejercicios AABD

Fecha: 2026-09-24

Estado: propuesta aprobada en conversación; pendiente de revisión escrita

## Objetivo

Revisar los materiales del repo que contienen una tarea, ejercicio o entregable y producir los resultados que falten. Cubrir asignaturas activas, rutas de compatibilidad y `_archivo_legacy/`, sin duplicar soluciones cuando una copia archivada tenga el mismo enunciado que una solución vigente.

La auditoría debe dejar claro qué se revisó, qué ya estaba resuelto, qué se completa, qué evidencia lo verifica y qué depende de datos personales o del equipo de estudiantes.

## Fuentes de alcance

- Carpetas vigentes `01_Erronka1_CNC_Guard/` a `07_Kafka/`, sus materiales y soluciones.
- Materiales transversales solo cuando planteen una tarea o entregable explícito.
- `_archivo_legacy/` y symlinks de compatibilidad. Los symlinks son referencias a sus destinos; no se cuentan como copias independientes.
- Los cambios locales ya presentes, incluidos el material legal 5071, el apunte de regresión lineal, el CSV de Ariketa 2.3 y la actualización del enunciado 05/Ingeniería de Datos, son fuentes de trabajo y deben permanecer intactos.

No se tratarán como ejercicios autónomos las diapositivas de teoría, ejemplos resueltos, recursos de referencia, resultados ya existentes ni carpetas de dependencias/caché. Se registrarán como cubiertos o fuera del alcance de tareas.

## Entregables

1. `00_Transversal/AUDITORIA_EJERCICIOS.md`: matriz de fuente, actividad, estado inicial, resultado, ubicación y verificación. Debe distinguir `resuelto`, `parcial`, `pendiente`, `duplicado de otra fuente` y `requiere datos humanos`.
2. Soluciones que falten en las carpetas `soluzioak/` canónicas, siguiendo los formatos del curso.
3. Resultados de tareas exclusivas del legado bajo `_archivo_legacy/soluzioak/`; las copias duplicadas apuntarán a su resultado canónico en la matriz, sin modificar ni mover los archivos de origen.
4. Referencias desde los README/índices de cada asignatura a los nuevos resultados.

## Brechas detectadas en el inventario inicial

- `01_Erronka1_CNC_Guard`: falta resolver el ejercicio de planificación PERT/Gantt de la empresa de tortilla. Las plantillas de equipo/anexos requieren nombres, funciones y decisiones reales; se dejarán como campos editables y se indicará qué datos faltan.
- `02_AA_Ereduak_5071`: hay solución para COMPAS, pero falta una resolución ordenada de los casos GDPR/AI Act y del proyecto integrador. El proyecto se preparará como ejemplo educativo hipotético del sector de educación, con informe técnico, transparencia para personas usuarias, protocolo interno y material para exposición. No se presentará como asesoramiento ni certificación de cumplimiento.
- `03_ML_5072`: la práctica actual cubre EDA, preprocesamiento, regresión y clasificación. Cotejarla con el material añadido de regresión y crear solo los ejercicios o resultados que realmente falten.
- `04_Programazioa_5073`: las soluciones actuales parecen cubrir los cuadernos de ejercicios. Verificar cada versión activa y sus equivalentes archivadas; en particular, contrastar el resultado de limpieza 2.3 con `data/mock_datuak/Ariketa 2.3/datu_zikinak.csv` y documentar cualquier diferencia.
- `05_BigData_Ingeniaritza`: la resolución de 01_01 existe. El enunciado actualizado de 01_02 incorpora preguntas de formato, orientación por filas/columnas, generación Faker de 100 y 10.000 filas, semillas y CSV→JSON que aún no aparecen en la resolución. Completar respuestas y producir código/datos reproducibles cuando el enunciado lo exige.
- `06_NiFi`: cotejar las siete prácticas con sus flujos, scripts, datos y resultados actuales; añadir solo la evidencia que falte.
- `07_Kafka`: completar/documentar las cinco prácticas de consola sobre topics, producer/consumer, offsets y particiones. Las operaciones se limitarán al broker local del laboratorio y se verificarán con estado observable.
- `legacy`: comparar cada enunciado o cuaderno archivado con los actuales. Resolver solo contenido único no cubierto; mantener el archivo original sin alteraciones.

La matriz final podrá añadir o cerrar brechas al inspeccionar todos los enunciados; esta lista no sustituye ese cotejo.

## Diseño de soluciones

- Mantener los originales de clase sin cambios. Añadir respuestas y artefactos en `soluzioak/`, cerca de la asignatura o caso al que pertenecen.
- Redactar documentos docentes principalmente en euskera, igual que los materiales; usar castellano para notas operativas cuando mejore su legibilidad. Código, rutas, resultados y nombres seguirán las convenciones de cada módulo.
- Para ejercicios analíticos, usar Markdown con respuestas numeradas que sigan el orden del enunciado.
- Para ejercicios de programación, conservar el patrón `.py` ejecutable y `.ipynb` si corresponde, junto con datos pequeños de salida o comandos de generación. No añadir dependencias globales; usar entornos ya declarados o documentar una dependencia aislada del módulo.
- Para prácticas de infraestructura, incluir configuración/flujo y evidencia reproducible, sin versionar credenciales, tokens ni datos privados.
- Las actividades individuales o grupales que requieran una elección subjetiva tendrán una respuesta modelo identificada como ejemplo. Los campos que dependan de nombres, firmas, composición real del grupo o decisiones personales quedarán en blanco con una explicación.

## Investigación legal

Las afirmaciones sobre GDPR, AI Act, aplicación temporal, clasificación de riesgo y sanciones se verificarán contra fuentes primarias vigentes (EUR-Lex y autoridades públicas, incluida AEPD cuando proceda). El informe explicará sus hipótesis y fecha de consulta, separará obligaciones legales de recomendaciones didácticas y evitará declarar que una empresa o sistema cumple la normativa.

## Verificación

- Cotejar cada ejercicio marcado como completado con su enunciado y registrar el vínculo en la matriz.
- Ejecutar soluciones Python con el entorno del repo, comprobando condiciones explícitas como número de filas, columnas, tipos, semillas y archivos generados.
- Validar JSON/CSV/Parquet y notebooks; verificar los JSON de flujos y los resultados de las prácticas NiFi/Kafka contra el estado esperado del laboratorio.
- Revisar que enlaces y rutas de los nuevos documentos existen, y que ningún secreto o salida local sensible se incluya en los artefactos.
- Mantener una separación visible entre resultados ejecutados, resultados simulados y ejemplos de respuesta.

## Supuestos y límites

- Para el proyecto legal integrador se usará un caso hipotético de predicción del rendimiento y propuesta de grupos escolares, alineado con el material. Es una solución modelo y no representa a una empresa real.
- No se inventarán identidades, firmas, composición de equipos ni preferencias personales.
- La revisión incluye tareas explícitas del legado, pero no reescribe, reubica ni moderniza archivos archivados que no requieran una respuesta.
- No se modificarán servicios externos ni se publicarán cambios. Las pruebas de infraestructura, si hacen falta, quedarán confinadas a los servicios locales de laboratorio descritos por el repo.
