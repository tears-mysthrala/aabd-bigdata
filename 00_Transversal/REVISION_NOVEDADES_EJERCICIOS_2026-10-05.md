# Revisión de sincronización y novedades — 2026-10-05

Comparación con el ciclo del **2026-10-02 08:07**, commit `4560307`, usado en
la revisión anterior. Horas locales: Europe/Madrid (CEST). La primera parte
recoge la revisión inicial; el trabajo posterior autorizado se documenta al final.
No se realizaron entregas personales en Moodle.

## Resultado vigente del trabajo autorizado

| Bloque | Estado y acceso |
|---|---|
| Moodle | Ciclo programado de 11:00 correcto: 72 actividades/11 tareas/68 hashes. Timer activo; login intermitente en comprobación manual posterior, detenido tras un intento. [Evidencia](EVIDENCIAS_MOODLE_2026-10-05.json). |
| Publicación de material | Seis archivos publicados en rama de revisión; master y commits locales ajenos preservados. Integración mediante PR pendiente. |
| Programación 2.4/2.5 | [Corregida y ejecutada](../04_Programazioa_5073/soluzioak/04_Datu_Zientzia_PDF_Ariketak/README.md), con tres regresiones. Incidencia de CSV originales documentada. |
| SVM | [Ejemplos y notebook ejecutados](../03_ML_5072/soluzioak/SVM/README.md). Tarea Moodle confirmada, introducción vacía y sin plazo visible; consigna/rúbrica pendiente. |
| Elastic | [P13, variantes P15, P16 y P17 ejecutadas](../05_BigData_Ingeniaritza/soluzioak/03_Elastic_Stack/novedades_2026-10-05/README.md), con GUI y salidas reales. Numeración corregida. |
| Kafka caso 5 | [Receta ejecutada](../07_Kafka/soluzioak/kafka_aurreratua_connect/caso5/README.md): inicial 3→Streaming 4→reinicio 4, sin replay. Worker 7.8.0 como variante explícita ante deadlock de 7.7.1. |

Las soluciones son artefactos locales; no se realizaron entregas personales en
Moodle. El detalle siguiente conserva también los fallos y el estado inicial.

## Últimos ciclos y publicación

| Ciclo | Resultado observado |
|---|---|
| 02/10 09:00 | CSV nuevos para Programación 2.4/2.5; cambios en el notebook de soluciones y Kafka. Push verificado. |
| 02/10 10:00 | Cambio en el notebook de ejemplos de Programación. Push verificado. |
| 02/10 11:00 | SVM nuevo; actividades 70→72, tareas 10→11, recursos 43→44. Push verificado. |
| 02/10 12:00 | Sin cambios. |
| 02/10 13:00 | Actualización del PDF de Kafka. Push verificado (`07106a4`). |
| 02/10 14:00 | Sin cambios. |
| 05/10 08:07–08:10 | Seis archivos modificados/descargados, incluido el manifiesto. Commit local `d967f11`; **push rechazado**. |
| 05/10 09:00–09:03 | Tres intentos de login fallidos, recuperación posterior. Cobertura completa según el sincronizador; sin cambios de archivos. Servicio termina con código 0. |

El timer está habilitado y activo, con ejecución horaria. El manifiesto del
05/10 registra **13 secciones, 72 actividades, 11 tareas, 0 errores y 0 fuentes
pendientes**. Se contrastaron los **68 archivos con SHA-256: todos coinciden**.
Estos valores prueban integridad de las copias y cobertura declarada de recursos;
no prueban resolución, ejecución o entrega de ejercicios.

El journal del ciclo de las 08:07 contiene `GH006`: `master` está protegida y
exige pull request. `git ls-remote --heads origin master` devuelve
`07106a4692223e8be875174becbc7c66ea023321`; el HEAD local es
`d967f11ca26e117f6289d95825ea3aab6c3e1f38`, un commit pendiente de publicación.
El ciclo posterior sin cambios **no reintenta ese push**, según el código de
`scripts/moodle_sync.py`. Su resultado exitoso no resuelve la publicación fallida.

## Ejercicios nuevos o ampliados — estado antes de realizarlos

| Material | Novedad y trabajo pendiente |
|---|---|
| [Elastic Stack](../05_BigData_Ingeniaritza/materialak/02_elastic_stack.pdf), 61→75 páginas | **P13 nueva** (pp. 51–60): Apache→Filebeat→Elasticsearch→Kibana, Compose, volumen compartido, al menos diez peticiones HTTP, inspección de logs/Discover y preguntas. No está cubierta por la solución actual. |
| Elastic, **P15**, pp. 65–66 | El antiguo P14 pasa a P15. La base de Grok ya está resuelta, pero faltan dos variantes: usuario al final del log y fecha `2026-10-04` al principio. |
| Elastic, **P16**, p. 70 | **Nueva**: Grok+Date, extraer campos del log y convertir la fecha original en `@timestamp`. Falta solución específica. |
| Elastic, **P17**, pp. 71–72 | **Nueva**: entrada JSON, convertir `status_code`/`bytes` a enteros, renombrar `request`→`uri` y eliminar `message`. Falta solución específica. |
| [Kafka avanzado](../07_Kafka/materialak/01_04_ApacheKafka_aurreratua.pdf), 52→73 páginas | **Caso 5 nuevo**, pp. 56–69: Compose/Dockerfile, MySQL→Kafka Connect→MongoDB, configuración de ambos conectores, comprobación `RUNNING`, inserción dinámica `Streaming` y nueve preguntas. La [solución anterior de Connect](../07_Kafka/soluzioak/kafka_aurreratua_connect/Ebazpena_Connect.md) sirve de base, pero falta ajustarla al entorno nuevo, destino `iabd.categories` y consignas exactas. No equivale a repetir desde cero la lógica ya existente. |
| [Programación: notebook de soluciones](../04_Programazioa_5073/materialak/2_SOLUZIOAK_URLa.ipynb), 91→98 celdas | Añade un bloque extra 2.4/2.5. Hay [soluciones locales](../04_Programazioa_5073/soluzioak/04_Datu_Zientzia_PDF_Ariketak/README.md) anteriores, pero 2.4 usa ocho filas de ejemplo y calcula el máximo individual en lugar del máximo agregado por ciudad/categoría. Hay que reconciliar 2.4 con el CSV docente de 30 filas y 2.5 con las nuevas tablas/concat. |
| [SVM](../03_ML_5072/materialak/5072_2_05_SVM.pdf), 10 páginas, recibido el 02/10 11:00 | Material nuevo de teoría y ejemplos `SVC`/`SVR` con escalado (p. 9). No se encontró solución específica local; el PDF no establece una entrega separada. No debe contarse como tarea obligatoria nueva sin confirmar Moodle. |

La numeración anterior de Elastic necesita actualización: **P13 antiguo
(Logstash stdin)→P14**, **P14 antiguo (Grok)→P15**. No son dos ejercicios nuevos.
La guía local sigue titulada P1–P14 y su auditoría conserva esa numeración.

## Incidencias de datos y cambios sin trabajo nuevo

- Los tres CSV recibidos para 2.4/2.5 tienen exactamente el mismo SHA-256:
  `salmentak.csv`, `bezeroak.csv` y `hiriak.csv`. Todos contienen 30 filas con
  columnas `hiria,kategoria,produktua,salmenta`. Los dos de 2.5 no cumplen
  los esquemas de clientes/ciudades del enunciado. Falta contrastar la fuente;
  no se corrigieron ni sustituyeron los originales.
- En ese CSV, la venta individual máxima es Donostia/Arropa, **456 €**;
  la combinación agregada máxima es Gasteiz/Janaria, **1.417 €**. Esto demuestra
  por qué la selección actual mediante `idxmax()` sobre filas no cumple 2.4.
- El notebook `3_Adibide_koadernoa_URLa.ipynb` mantiene 84 celdas. La comparación
  de fuentes solo muestra dos líneas vacías nuevas después de `joblib.dump`.
  No se detecta un ejercicio adicional.
- La programación general del curso cambia de nombre a
  `Programazioa_AA_2_2026-2027.docx.pdf`. Es documentación curricular;
  no se incluye en el recuento de nuevos ejercicios prácticos.

## Límite de la consulta inicial de Moodle

El aumento de tareas **10→11** está confirmado por los manifiestos. El
sincronizador cuenta tareas y descarga sus adjuntos, pero no conserva un
inventario de títulos, texto del enunciado o plazos de las tareas sin adjuntos.
Una consulta adicional de lectura, usando su autenticación existente, no
consiguió confirmar sesión en cuatro intentos. No se imprimieron credenciales,
cookies ni HTML de sesión. Por tanto, **nombre, enunciado y plazo de esa tarea
adicional siguen sin verificar**; tampoco se consultaron entregas personales.

## Orden de trabajo sugerido

1. Confirmar la tarea adicional en Moodle y sus plazos cuando vuelva a funcionar el acceso.
2. Completar Elastic P13, las variantes P15, P16 y P17; corregir su numeración documental.
3. Adaptar Kafka Connect al caso 5 aprovechando el trabajo existente.
4. Reconciliar Programación 2.4/2.5 y aclarar los CSV duplicados de 2.5.
5. Ajustar la publicación automática a la política de PR de `master`, sin debilitar la protección.

La revisión inicial solo añadió este informe local, sin cambiar soluciones,
credenciales o configuración y sin publicar. El usuario autorizó después
realizar el trabajo necesario y usar su navegador autenticado.


## Trabajo posterior autorizado — 05/10/2026

### Moodle: tarea identificada y cobertura real

La sesión autorizada de Chromium permitió confirmar la tarea
[SVM - Ariketa](https://elearning20.hezkuntza.net/012053/mod/assign/view.php?id=63380).
Tiene el enunciado vacío y no adjunta archivos. Las fechas generales solo
muestran apertura el 11/09/2026 a las 00:00; no hay fecha límite visible.
La tarea sí existe, pero sus requisitos adicionales no están publicados.

Un ciclo real posterior con `--no-publish --browser-cdp` terminó a las 10:23:
13 secciones, 72 actividades, 11 tareas, cero errores y cero fuentes pendientes.
Los 68 hashes siguen coincidiendo. El manifiesto ahora conserva título, URL,
sección, texto del enunciado y fechas generales de las once tareas;
no incluye entregas personales ni calificaciones. Las propuestas de CNC Guard
muestran fecha general de entrega **20/10/2026 14:30**; no se realizaron ni
modificaron esas entregas.

El intento manual previo de login autónomo falló cinco veces. Esto no queda
oculto como una sincronización correcta: se usó la sesión autorizada para
completar esta comprobación. El ciclo horario de las 10:00 había sido exitoso;
no se cambiaron las credenciales ni se promete haber eliminado los reintentos.

### Programación 2.4/2.5 y SVM

- [Guía de Programación actualizada](../04_Programazioa_5073/soluzioak/04_Datu_Zientzia_PDF_Ariketak/README.md): funciones existentes corregidas con módulo compartido y variantes anteriores conservadas.
- El CSV de 30 filas coincide exactamente con la generación docente: máximo agregado Gasteiz/Janaria **1.417 €**, máximo individual Donostia/Arropa **456 €**, total **7.873 €**. No se incluyen los totales marginales como candidatos al máximo.
- Los CSV originales de 2.5 permanecen intactos y se documenta su esquema incompatible. Las tablas embebidas exactas del notebook docente producen inner **4×6**, left **5×6** (Amaia conservada sin ciudad) y concat **6 filas / 705 €**.
- Script y notebook nuevo se ejecutaron completos. Del notebook principal (37 celdas) se ejecutaron solo las dos celdas de código modificadas; también se actualizaron sus dos celdas Markdown explicativas. Las otras 33 celdas se conservaron exactamente. Tres regresiones pasan, incluida la que fallaba con el máximo individual.
- [Guía y notebook SVM](../03_ML_5072/soluzioak/SVM/README.md): ejemplos exactos del PDF ejecutados, SVC accuracy de entrenamiento **1,0** y SVR R² de entrenamiento **0,576086**. La extensión explícita de Iris obtiene accuracy test **0,933333**. SVR OOF R² **−0,443113**, peor que el baseline de media **−0,176541**; se separa entrenamiento de generalización.
- SVM está preparado como ejercicio educativo y candidato de entrega; no acredita una entrega ni requisitos que el docente aún no haya especificado.

### Reparación de publicación

El nuevo [publicador](scripts/moodle_publish.py) construye un snapshot desde la
rama remota base con un índice temporal y únicamente archivos gestionados.
Comprueba cambios pendientes incluso si no hubo descargas nuevas y publica
en una rama de revisión. No escribe directamente en `master`, no fuerza push,
no publica los commits ajenos de HEAD y no modifica el índice o la rama local.
La integración sigue requiriendo PR y revisión.

Las regresiones usan un remoto Git real de laboratorio con `master` protegida:
conservan trabajo local staged/unstaged, excluyen commits ajenos, recuperan
un push fallido sin descarga nueva, reutilizan snapshots y rechazan escapes,
enlaces o archivos ausentes. La preparación contra el remoto real también
conservó HEAD e índice; [evidencia](EVIDENCIAS_MOODLE_2026-10-05.json).
Las guías y CI de PR incluyen las comprobaciones nuevas; no se añadieron
workflows de despliegue ni CI por cada push.

### Elastic P13, P15, P16 y P17

La [guía actualizada](../05_BigData_Ingeniaritza/soluzioak/03_Elastic_Stack/novedades_2026-10-05/README.md)
y el [registro de ejecución](../05_BigData_Ingeniaritza/soluzioak/03_Elastic_Stack/novedades_2026-10-05/exekuzioa_2026-10-05.md)
conservan configuración, preguntas, salidas, capturas y verificadores:

- **P13:** quince peticiones HTTP reales; 8 respuestas 200, 6 respuestas 404 y una 304. Los logs Apache/Filebeat coinciden y ES conserva exactamente los quince `message` de la tanda. Discover mostró Documents(15), códigos y el detalle `message` de un documento.
- **P15:** ambas variantes probadas en Grok Debugger GUI y Logstash real. Usuario y fecha extraídos; IP inválida produce `_grokparsefailure`.
- **P16:** fecha original convertida a `2026-09-30T08:30:45.000Z`; zona Europe/Madrid como hipótesis explícita. Fecha 31/Sep produce `_dateparsefailure`; estructura incorrecta, `_grokparsefailure`.
- **P17:** `status_code=500` y `bytes=1234` son enteros; `request` pasa a `uri`; `message` desaparece. `event.original` conserva el JSON fuente, límite explicado.
- Numeración corregida en guías: stdin es ahora P14 y Grok P15. CustomLog idempotente comprobado con reinicio real de Apache: una directiva.

Se usó Elastic 9.5.4, frente a 9.1.4 del PDF, y Linux/Bash en lugar de
Windows/PowerShell. El laboratorio aislado y su navegador están detenidos;
los tres volúmenes se conservan. Ruff, compilación, Compose, Bash, enlaces y
verificadores de las salidas/snapshots pasan. Reverificar evidencia guardada
tras formatear no se presenta como una ejecución nueva de los servicios.

### Publicación real y autenticación horaria: resultados separados

El ciclo completo con la sesión autorizada de Chromium terminó el 05/10 a
las **10:42:24**, con 13 secciones, 72 actividades y cero errores/fuentes
pendientes. Publicó el material pendiente en la rama
[`moodle-sync/master/2026-10-05-fa68cd398f35`](https://github.com/tears-mysthrala/aabd-bigdata/tree/moodle-sync/master/2026-10-05-fa68cd398f35).
El remoto confirma el commit `e063f65d3d67`; tiene como padre `07106a4` y
solo seis archivos gestionados cambiados. No incorpora los commits ajenos del
HEAD local ni las soluciones nuevas. **Integración en master pendiente de PR.**

La prueba normal del servicio (10:34:48–10:37:32) falló sus cinco intentos
antes de descargar, al no confirmar sesión. Un diagnóstico con el mismo
EnvironmentFile del servicio comprobó que Chromium seguía en el formulario
con error de login. Ni todas las cookies ni las filtradas por Moodle daban
sesión válida: no se atribuye a la selección de cookies ni a la publicación.
No se imprimieron valores sensibles, se cambiaron credenciales o se exportó
la sesión de Chromium. **La autenticación autónoma del servicio sigue sin
resolver.** El timer permanece habilitado; un timer activo no demuestra que
su próximo login vaya a funcionar.

### Recuperación tras desbloqueo — resultado vigente

El diagnóstico posterior mostró el aviso explícito **«Your account is locked»**.
Se pausó el timer sin deshabilitarlo para evitar nuevos intentos. El usuario
confirmó el desbloqueo mediante el enlace recibido de Moodle; no se le pidió
la contraseña ni el enlace. Los reintentos previos pudieron contribuir al bloqueo.

Se añadió detección de avisos conocidos de cuenta bloqueada/login inválido:
el ciclo se detiene ante el primer rechazo explícito, con mensaje fijo y sin
copiar datos de la página. Los errores transitorios de red conservan sus
reintentos. Ocho regresiones verifican clasificación sin secretos, publicación sin descargas, un solo
intento ante bloqueo y recuperación tras timeout.

**El ciclo normal de 10:49:17–10:51:28 terminó `Result=success`,
`ExecMainStatus=0`, con login al primer intento**, 13 secciones, 72 actividades
y cero errores/fuentes pendientes. Reutilizó el mismo commit de la rama remota;
no volvió a subir otro snapshot. El timer quedó **enabled/active**, reactivado
solo después de verificar este resultado. Las credenciales no se cambiaron.
Este ciclo prueba recuperación actual, no ausencia de futuras caducidades o bloqueos.

Las 25 pruebas rápidas (publicación, login, agregación, Kafka mock y Git)
y las 18 del proyecto CNC Guard pasan. Los blobs de los seis archivos publicados
coinciden con el árbol local y los hashes del manifiesto. Las soluciones de
este lote siguen siendo trabajo local, separado de la rama de material.

### Kafka avanzado: caso 5

La [receta del caso 5](../07_Kafka/soluzioak/kafka_aurreratua_connect/caso5/README.md)
conserva SQL exacto, Dockerfile, Compose, configuraciones, nueve respuestas,
registrador REST y verificador de solo lectura. En el proyecto fresco
`aabd-kafka-connect-20261005-v78`, las tres capturas pasan **once comprobaciones**
cada una: filas completas SQL/topic/Mongo iguales, esquema correcto, source y
sink con sus tareas RUNNING, offsets persistentes y ningún OOM.

| Etapa | MySQL / mensajes Kafka / MongoDB |
|---|---|
| Inicial | 3 / 3 / 3: Football, Basketball, Running |
| Inserción Streaming | 4 / 4 / 4, incluye category_id=4 |
| Cierre normal y reinicio del worker | 4 / 4 / 4, topic sin replay y offsets conservados |

El comando literal del PDF reprodujo un deadlock con Connect7.7.1; el registro
secuencial REST también falló al reiniciar y cambiar el timeout no lo resolvió.
Los diagnósticos fallidos se conservan. El patrón coincide con
[KAFKA-16051](https://issues.apache.org/jira/browse/KAFKA-16051), corregido upstream
en Kafka3.8. La receta final usa **solo el worker CP7.8.0** como variante explícita;
[Confluent confirma su base Kafka3.8](https://docs.confluent.io/platform/7.8/release-notes/index.html).
Broker7.7.1, JDBC10.8.9, Mongo connector1.13.0 y SQL/destino permanecen iguales.
Con el worker corregido ambos registros REST devolvieron HTTP201.
No se afirma ejecución satisfactoria del comando original ni exactly-once.

### Últimos ciclos después de recuperar la cuenta

El timer ejecutó automáticamente el ciclo **11:00:00–11:01:54**: éxito al
primer login, cobertura completa y mismo snapshot remoto reutilizado. Una
comprobación manual adicional **11:03:19–11:03:28** recibió un rechazo explícito
de login; el nuevo guard detuvo el ciclo en un único intento, sin repetirlo.
Esto muestra que **el login es intermitente** aunque las credenciales no hayan
cambiado; no se atribuye a una causa no demostrada ni se presenta toda la
autenticación horaria como solucionada. El acceso mediante la sesión autorizada
sigue siendo una alternativa manual. El timer conserva su periodicidad horaria
con los rechazos explícitos limitados a un intento por ciclo.

El ciclo manual de 11:07:20–11:09:07 con la sesión autorizada terminó con
**cero archivos cambiados**, cobertura completa y ningún commit/push. Se corrigió
el aviso repetido: el material pendiente en el HEAD local ya no se mezcla con
las descargas reales del ciclo. La comparación para publicar sigue siendo
independiente, incluso sin novedades; su regresión forma parte de las 25 pruebas.

Kafka confirma que el hash del archivo de offsets se conserva tras reinicio;
el jstack final no muestra deadlock. Ambos proyectos Kafka quedaron detenidos,
con sus ocho volúmenes conservados. [Registro final](../07_Kafka/soluzioak/kafka_aurreratua_connect/caso5/EXEKUZIOA_2026-10-05.md).

### Entrega local revisable

La rama local `review/moodle-novedades-2026-10-05` recoge el código, las
resoluciones, los materiales y las evidencias de este lote sobre la base remota.
No se ha publicado esta rama ni creado una PR. Los cambios previos ajenos y los
archivos de navegación que ya estaban modificados se conservan en el árbol de
trabajo original y quedan fuera del commit aislado. En la copia limpia pasaron
25 pruebas rápidas, 18 de CNC Guard, Ruff (52 archivos) y compilación.
