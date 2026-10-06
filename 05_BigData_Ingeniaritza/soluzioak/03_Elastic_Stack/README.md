# Elastic Stack: cómo usar las prácticas P1–P17

El [enunciado](../../materialak/02_elastic_stack.pdf) se resuelve en
[Ebazpena_Elastic_Praktikak.md](Ebazpena_Elastic_Praktikak.md). Elasticsearch
guarda e indexa documentos; Kibana permite consultarlos y visualizarlos.
No necesitas ejecutar todo el stack para leer y razonar las consultas.

## Qué corresponde a cada entrega

| Prácticas | Qué haces | Qué demuestra el resultado |
|---|---|---|
| P1–P4 y adicionales | Crear `produktuak`, cargar cuatro productos, inspeccionar mapping y ejecutar Query DSL. | Los conteos y documentos devueltos coinciden con cada filtro; `text` y `keyword` tienen usos distintos. |
| P5 | Data View, Discover y KQL. | Columnas visibles, filtros guardados y coincidencias esperadas. KQL filtra documentos; no es el mismo lenguaje que Query DSL. |
| P6–P7 | Lens y dashboards de productos/ventas. | Agregación correcta (`count`, suma o media), ejes y filtros interactivos coherentes. `count` de ventas no equivale a suma de unidades. |
| P8 | ILM e Index Template. | La política está configurada y el template se aplica a un índice nuevo. No demuestra el borrado tras 90 días ni migración física entre nodos. |
| P9–P12 | Elegir ingesta/Beats y diseñar el recorrido de logs. | Interpretación de componentes y outputs. |
| P13 | Apache → Filebeat → Elasticsearch → Kibana. | Peticiones reales, volumen compartido y correspondencia exacta entre log y `message`. |
| P14–P17 | stdin, Grok (incluidas variantes), Date y Mutate. | Eventos de Logstash real, fecha del evento, tipos numéricos y limpieza. |

El PDF actualizado tiene 75 páginas. La antigua P13 de stdin pasa a **P14**;
la antigua P14 de Grok pasa a **P15**. La guía completa de las novedades,
sus preguntas y los verificadores están en
[novedades_2026-10-05/](novedades_2026-10-05/README.md).

## Preparación y efectos de los comandos

Desde la raíz, entra con
`cd 05_BigData_Ingeniaritza/soluzioak/03_Elastic_Stack`.
El laboratorio utiliza Docker/Compose; los scripts REST necesitan Bash, curl y
Python 3. Lee [compose.yaml](compose.yaml) antes de crear el laboratorio y
utiliza los puertos de **tu** instancia. Las direcciones de los registros son
las usadas en esas ejecuciones, no una garantía de que estén activas hoy.

`elastic_praktikak.sh` ejecuta P1–P4 y consultas adicionales, pero primero
**elimina y recrea `produktuak`**. `elastic_praktika_5_8.sh` y los generadores
de dashboards también modifican el laboratorio; sigue sus instrucciones en
[la guía de entrega](dashboards/README.md). Repetir esas operaciones puede
reemplazar trabajo propio: úsalas en una instancia de prácticas dedicada.

## Lectura y comprobación de resultados

En [el registro de P1–P4](exekuzioa_2026-09-28.md) se muestran respuestas REST.
En [el registro de Kibana](exekuzioa_2026-10-01.md) se explican las
comprobaciones GUI/Inspector de P5–P8 y del Grok básico (entonces P14, ahora P15). Las imágenes y el NDJSON entregable
están en [dashboards/](dashboards/README.md).

Para reproducir, anota versión y URL del laboratorio, ejecuta la práctica y
compara las respuestas con sus criterios. En un dashboard revisa tanto el dato
del Inspector como el efecto de un filtro y su retirada. Importar un NDJSON
sin abrir sus paneles no prueba que todas las visualizaciones funcionen.
