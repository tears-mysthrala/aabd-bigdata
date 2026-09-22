# Estado de validación de la plantilla

Fecha: 18 de septiembre de 2026. Esta nota se refiere exclusivamente a los archivos del paquete de setup.

## Comprobaciones realizadas

| Comprobación | Resultado y alcance |
|---|---|
| Sintaxis de Python | Cinco archivos analizados con `ast.parse`, sin errores. |
| Manifiesto y configuración | `pyproject.toml` y `config/resources.toml` leídos con `tomllib`, sin errores. El lock se resolvió con uv 0.12.15. |
| Notebook auxiliar | Validación `nbformat` y análisis de sintaxis de todas las celdas de código. Sin ejecuciones ni salidas prefabricadas. |
| Pruebas de rutas y recursos | `3 passed` con `uv run --locked pytest -q`. |
| Bootstrap | Probado en copia temporal: preparación sin pin, inicialización con el parche del intérprete de prueba y rechazo de una segunda inicialización sin sobrescribir el pin. |
| Ruff | `ruff check` y `ruff format --check` pasan sobre `src`, `scripts` y `tests`. |
| Smoke test integral | Pasa con CPython 3.13.13: importaciones, Parquet, DuckDB, modelos, gráfico y persistencia del modelo generado por el script. |
| Ejecución del notebook auxiliar | `nbformat.validate` pasa y `jupyter nbconvert --execute` completa las 8 celdas con el kernel `cnc-guard`. |
| Contenido entregado | `.venv`, cachés y datos industriales no se versionan; `.python-version`, `uv.lock` y `docs/uv-version.txt` se generan para compartir la referencia. |

Para estas comprobaciones se utilizó Linux x86-64, CPython 3.13.13 y uv 0.12.15. La instalación editable del paquete se realizó mediante `uv sync --locked --managed-python`.

## Pendiente de ejecutar por el equipo

No se han probado Windows, macOS, ARM64, extras opcionales, auditoría de vulnerabilidades, exportaciones SBOM o conexión a una máquina. Tampoco se ha validado el notebook final del reto, que aún no está incluido.

El lock actual debe conservarse y compartirse como referencia. Cada equipo debe ejecutar las pruebas del documento con su plataforma. Los tamaños, tiempos y cuotas del documento son estimaciones y puntos de partida; se sustituirán por mediciones de los equipos.

La prueba de instalación no acredita validez predictiva, cumplimiento normativo completo ni seguridad de una integración industrial.
