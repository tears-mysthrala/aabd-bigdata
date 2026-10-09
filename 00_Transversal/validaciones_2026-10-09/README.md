# Ejercicios y sincronización — 9 de octubre de 2026

Comparación y pendientes iniciales: [revisión del día](../REVISION_MOODLE_2026-10-09.md). Este informe actualiza aquel diagnóstico después de implementar y ejecutar los cambios.

## Cambios y comprobaciones

- [Series temporales](../../06_NiFi/soluzioak/08_Denbora_Serieak/README.md): los 19 pasos de la nueva edición, script y notebook ejecutados sin errores. Datos sintéticos explícitos, 61 registros en el intervalo inclusivo solicitado, media 22.587 °C, tres NaN y un pico deliberado de 65 °C; se conservan los originales y el rolling se calcula sobre la interpolación temporal. Cálculo de almacenamiento y reflexiones junto al código. Gráfico inspeccionado visualmente.
- [Cuaderno 3 de Programación](../../04_Programazioa_5073/soluzioak/07_Moodle_2026-10-06/README.md): contrastado con SOLUZIOAK, ejecutado como notebook y script equivalente; comparación de splits Wine, interpretación de métricas, GridSearch con escalado por fold y balanced accuracy, significado de probabilidad de clase 1 y rechazo de entradas no finitas. Entorno aislado uv con lock y auditoría sin vulnerabilidades conocidas detectadas. CSV/pickle propios generados se mantienen locales e ignorados.
- API docente 3.5: tres pruebas nuevas con modelo creado en el test. Token ausente/incorrecto o configuración ausente → 401; token válido → predicción 200; entrada incompleta → 422. Esto verifica acceso al endpoint, no robustez clínica, carga sostenida ni despliegue remoto.
- [Guía de examen](../../04_Programazioa_5073/materialak/Moodle_page_64153.md): texto docente sincronizado y verificado con SHA-256. El soporte de `mod/page` excluye envoltorios autenticados y deja pendientes páginas con medios, tablas o adjuntos sin copiar. Doce regresiones nuevas, incluidas cobertura completa/parcial e idempotencia de un ciclo simulado.
- CI de PR: incorpora las regresiones nuevas y la ejecución del cuaderno 3 y Boosting con dependencias bloqueadas; checks de Ruff sin mutación. YAML solo valida PRs, no despliega al publicar una rama.

## Evidencia actual

[Tests](tests.json): **115 pasados** — Moodle/publicación 54, API 11, CNC 18, estructura Frameworks 2, CSV 3, Kafka mock 1, Medallion 12, tears_style 5, Faker 1, Boosting 3, galería 4 y validación Elastic optimizada 1. `tears_style` es trabajo previo local: se ha probado, pero no se incluye en el commit. El aviso deprecado Starlette/httpx sigue visible.

Ruff check y format --check, compilación Python y diff --check correctos. Se verificó equivalencia AST del código de cada pareja notebook/script modificada y ausencia de outputs de error; se aplicó la limpieza de metadata/rutas locales antes de publicar.

Primer ciclo del día: terminado a las 08:37 CEST con `Result=success`, `ExecMainStatus=0`, **80 actividades, 83 archivos, 0 errores y 0 fuentes pendientes**. Los 83 SHA-256 coinciden. Snapshot publicado y comprobado por `git ls-remote`: `moodle-sync/master/2026-10-09`, `d51ae97904abb9e2fe3b0e9ecd8b49e9c8b73066`. La publicación del snapshot no equivale a integración en master.

No se han hecho entregas en Moodle ni se atribuyen resultados del profesor a ejecuciones propias. El CSV de sensores docente sigue ausente. Los pendientes humanos, credenciales, datos externos y evidencias GUI históricas del [informe del día 8](../validaciones_2026-10-08/README.md) conservan sus límites; estas pruebas no los cierran.

## Cierre de revisión y ayuda visual

Se añaden tres regresiones de URL/escritura atómica Moodle, cuatro de la galería y una que exige rechazar eventos inválidos aun con `python -O`: total local 115. Se regenera Boosting con gamma=150, que distingue las escalas de ganancia 108/216. Se elimina una predicción duplicada y se ejecuta de nuevo el cuaderno 3. Los errores del material docente se conservan y contrastan en una guía de erratas. La galería de 20 modelos conserva los 14 originales y añade datos, parámetros, métricas recalculadas y pruebas de separación train/test.

El login fue rechazado a las 09:00; se pausó el temporizador. Tras confirmar el usuario que podía entrar sin cambio de contraseña, un único ciclo fresco de 09:14 a 09:16 terminó correctamente (80 actividades, 83 hashes coincidentes, cero errores o fuentes pendientes). Se reactivó el temporizador. No se atribuye una causa demostrada al rechazo anterior. Snapshot y SHA en `moodle.json`; integración por PR #17.

[Revisión posterior de descargas y mock de examen](../REVISION_DESCARGAS_RECUPERADAS_2026-10-09.md): 13 pruebas adicionales, cinco preguntas justificadas, checklist práctico cubierto y retos nuevos del PDF de series de las 10:02.
