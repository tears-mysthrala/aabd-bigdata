# Entrega de Kibana — prácticas 5–8 y 14

Revisada contra el PDF actual de **61 páginas**, el 1 de octubre de 2026.
[Respuestas completas](../Ebazpena_Elastic_Praktikak.md),
[verificación real](../exekuzioa_2026-10-01.md).

## Abrir el trabajo que ya está hecho

El laboratorio actual usa Elasticsearch en `127.0.0.1:19200` y Kibana en
`127.0.0.1:15601`. Los contenedores ya estaban activos; se han conservado.

- [Discover: todos los productos](http://localhost:15601/app/discover#/view/aabd-p5-0).
- [Discover: Informatika](http://localhost:15601/app/discover#/view/aabd-p5-1).
- [Discover: precio > 100](http://localhost:15601/app/discover#/view/aabd-p5-2).
- [Discover: Informatika AND precio < 500](http://localhost:15601/app/discover#/view/aabd-p5-3).
- [Discover: NOT Papergintza](http://localhost:15601/app/discover#/view/aabd-p5-4).
- [Dashboard de productos: 2 paneles Lens](http://localhost:15601/app/dashboards#/view/aabd-28ab1f59255f6d99).
- [Dashboard de ventas: 5 paneles Lens](http://localhost:15601/app/dashboards#/view/aabd-1fab5517b75a73ff).
- [Política web-logs-policy](http://localhost:15601/app/management/data/index_lifecycle_management/policies/edit/web-logs-policy).
- [Grok Debugger](http://localhost:15601/app/dev_tools#/grokdebugger).

## Reproducir en otro laboratorio

Desde `03_Elastic_Stack/`:

```bash
docker compose up -d
# Esperar a que ES y Kibana estén disponibles.
./elastic_praktika_5_8.sh
```

Para los puertos del laboratorio actual:

```bash
ES=http://127.0.0.1:19200 KB=http://127.0.0.1:15601 ./elastic_praktika_5_8.sh
```

El script utiliza Python estándar, crea índices solo si faltan, conserva y
compara íntegramente los datos existentes, crea Data Views si faltan y guarda
búsquedas y objetos Lens con ids estables. Repetirlo conserva 4/500 documentos.
Si los datos existentes son diferentes, se detiene antes de sobrescribirlos.
Los objetos del ejercicio con ids `aabd-*` sí se actualizan al repetirlo;
no se borran otros objetos ni índices. Solo acepta servicios en loopback.

## Exportación para entregar

[kibana_praktikak.ndjson](kibana_praktikak.ndjson) contiene 16 objetos:
2 dashboards, 7 Lens, 5 búsquedas Discover y 2 Data Views, con referencias.
En Kibana: **Stack Management → Saved Objects → Import**.
Importación comprobada en el espacio independiente `aabd-egiaztapena`:
16 objetos, `success: true`, sin advertencias.

Los documentos Elasticsearch y las políticas ILM no se incluyen en Saved
Objects: se reproducen con el script. El CSV original queda en
`../../../materialak/salmentak_kibana.csv`; la política y el template también
están guardados como JSON en esta carpeta. La P15 (P14 en el PDF de 61 páginas usado el 01/10) tiene el patrón y los dos
resultados en las respuestas; Grok Debugger no guarda una visualización Lens.

[La documentación de Elastic](https://www.elastic.co/docs/explore-analyze/find-and-organize/saved-objects)
describe la importación y exportación de Saved Objects;
[la configuración de ILM](https://www.elastic.co/docs/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy)
describe la relación entre política y template.

## Evidencia y límites

- [gui_verification.json](gui_verification.json): texto y resultados leídos
  de la interfaz real con el navegador de T3 Code.
- [irudiak/](irudiak/): PNG de los canvas de los gráficos reales, exportados
  desde Kibana. Son gráficos individuales, no capturas de la página completa.
- [emaitzak.json](emaitzak.json): cifras calculadas del CSV completo.
- [import_verification.json](import_verification.json): resultado de importar
  los objetos en otro espacio.
- [ilm_policy.json](ilm_policy.json) y [ilm_template.json](ilm_template.json).

El CSV se cargó mediante API, no mediante el diálogo Data Visualizer.
La herramienta de captura de página de T3 falló; no hay capturas completas.
ILM se verificó por configuración, GUI y simulación de template; no se ha
esperado 90 días ni se ha probado movimiento físico entre tiers distintos.
`sortu_dashboardak_classic.py` conserva el intento anterior como referencia
 y está deshabilitado: la solución usa Lens.
