# Planificación CNC Guard — snapshot del 13 de octubre

[project_plan.json](project_plan.json) conserva el inventario de 27 tareas,
fechas propuestas, dependencias y referencias al tablero del equipo B-taldea.
No ejecuta acciones ni actualiza issues, hitos o el proyecto remoto. Los estados
son los guardados al preparar el archivo, no una consulta en tiempo real.

## Procedencia y límite de vigencia

El campo `source_sha256` corresponde a `contenido.json` del commit
`ace74b2e9abbe9fe3a00fad8797a34f6fec72c4a`, indicado en `source_commit`.
La presentación cambió después: la arquitectura vigente es
**Kafka → NiFi → FastAPI → Elasticsearch/Kibana**, descrita en
[la trazabilidad actual](../Presentacion_Tecnologias/TRAZABILIDAD.md).

Este archivo conserva la planificación anterior como referencia histórica.
En particular, CG13–CG16 todavía describen topics/grupos y un consumidor
de inferencia de la propuesta previa; requieren adaptación antes de usarse
como plan de implementación actual. No se cambia el hash para atribuir esas
tareas a una fuente distinta ni se modifican silenciosamente las tareas remotas.
Fechas, responsables y alcance deben ser revisados por el equipo.

## Repositorio del equipo

El submódulo [B-taldea](../../B-taldea) fija el commit
`b05abf06f9b881e57b5ef4f6f565c9c82bf6ac98`. Desde la raíz:

```bash
git submodule update --init 01_Erronka1_CNC_Guard/B-taldea
```

La actualización descarga ese commit concreto; no actualiza el tablero ni
las ramas remotas. El snapshot JSON puede leerse sin inicializar el submódulo.
