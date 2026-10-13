# Sincronización de trabajo pendiente — 13 de octubre de 2026

## Cambios recuperados

- Correcciones docentes de los siete simulacros del commit `5af3827`. PR #18
  se fusionó en `feat/ejercicios-moodle-2026-10-08` después de que PR #17
  integrase esa base en master: las correcciones no habían llegado a master.
  Se integra la rama sin restaurar fuentes Moodle antiguas.
- Planificación de 27 tareas del commit local `1dc990f`, documentada como
  snapshot histórico con la fuente y commit originales. Su arquitectura
  previa requiere adaptación del equipo antes de implementar las tareas.
- Registro de B-taldea como submódulo, fijado a `b05abf06f9b881e57b5ef4f6f565c9c82bf6ac98`.
- Actualización pypdf 6.19.0 de la rama de Dependabot de PR #22.
- Comprobador de simulacros incorporado al job `tests` del CI de PR.

## Trabajo que ya estaba integrado

Elastic P18–P22 está en master mediante `63da0a9` y `115f2dc`, con mejoras,
regresiones y evidencias posteriores al worktree independiente. Los 25 archivos
sin seguimiento y el README modificado de ese worktree son versiones antiguas
de rutas ya publicadas; no deben copiarse sobre la versión actual.

La rama `review/moodle-entregas-2026-10-05` conserva tres commits locales.
Las siete entregas y los archivos de portabilidad ya están en master. Las
diferencias restantes son fuentes/snapshots antiguos y código/documentación
con mejoras posteriores. No se fusiona esa rama completa.

Los dos stashes anteriores se conservan intactos. El respaldo del 8 de octubre
contiene 21 rutas modificadas y 102 rutas adicionales, todas presentes en
master: 14 de las modificadas y 77 de las adicionales coinciden byte a byte.
El resto conserva versiones anteriores de sincronización, notebooks, NiFi,
Elastic y Kafka. El segundo stash contiene el manifiesto Moodle antiguo y
diagnóstico adicional del escáner. No se aplican ni se descartan respaldos.
Las ramas locales y worktrees históricos se conservan para revisión posterior.

## Validación local de la integración

- 55 tests de sincronización Moodle y verificación Elastic: correctos.
- Comprobador: 7 modelos, 64 apartados, 37 fuentes, 201 enlaces, 6 bloques
  Python parseados; CSV de 322 filas y 308 válidas. La fuente NiFi modificada
  se contrastó antes de renovar su hash; véase la validación del paquete.
- Ruff check/format del comprobador y git diff --check: correctos.
- Gitleaks sobre commits nuevos respecto a origin/master: sin hallazgos.
- uv sync --frozen del exportador y pip-audit de sus ocho dependencias
  fijadas: sin vulnerabilidades conocidas.
- pypdf 6.19.0 lee los PDF español/euskera: 33 páginas con títulos esperados
  en cada uno. Los PPTX conservan 33 diapositivas. No se regeneraron exports.
- Plan JSON: 27 IDs únicos, dependencias existentes y fechas ordenadas.

Estos resultados no acreditan entregas Moodle, funcionamiento industrial ni
actualización del tablero del equipo. El resultado de CI y el merge remoto
se consultan en el PR de integración; no se deducen de estos checks locales.
