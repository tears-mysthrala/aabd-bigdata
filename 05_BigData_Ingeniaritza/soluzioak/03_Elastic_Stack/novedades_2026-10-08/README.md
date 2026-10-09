# Elastic Stack — prácticas P18–P22 del 8 de octubre

Enunciado: [02_elastic_stack.pdf](../../../materialak/02_elastic_stack.pdf), ampliación respecto a la versión integrada del 7 de octubre. Las respuestas siguientes cubren las cinco prácticas nuevas; las anteriores siguen en [la guía P1–P17](../README.md).

## P18. Log gordina → filter-katea

Entrada literal del PDF: `2026-10-05 10:30:45 ERROR nginx 'Connection refused' client=203.0.113.5`.

1. Extraemos `timestamp`, `maila=ERROR`, `zerbitzua=nginx`, `mezua=Connection refused` y `bezero_ip=203.0.113.5`. Conservamos `message` como línea original.
2. Orden: **Grok → Date → GeoIP opcional → Mutate opcional**. Grok crea los campos que necesitan los filtros posteriores.
3. Grok separa texto; Date establece la fecha del evento en `@timestamp`; GeoIP intenta enriquecer la dirección; Mutate permite convertir, renombrar o eliminar campos si el esquema lo exige.
4. Pattern completo, anclado para rechazar prefijos/sufijos imprevistos:

   ```text
   ^(?<timestamp>%{YEAR}-%{MONTHNUM}-%{MONTHDAY} %{TIME}) %{LOGLEVEL:maila} %{WORD:zerbitzua} '%{DATA:mezua}' client=%{IP:bezero_ip}$
   ```

   Está implementado en [p18.conf](pipelines/p18.conf). Para la comprobación solicitada en Grok Debugger, pegar el log y este pattern y comparar los cinco campos. La ejecución automatizada prueba Grok real de Logstash. Además se realizó la interacción en Grok Debugger de Kibana: [captura P18](evidencias/p18-grok.png), [snapshot](evidencias/p18-grok-snapshot.yml). Son evidencias distintas.
5. Date usa `match => ["timestamp", "yyyy-MM-dd HH:mm:ss"]` y `timezone => "Europe/Madrid"`. El enunciado no indica zona: elegimos explícitamente hora local del laboratorio. En octubre corresponde a UTC+02: `2026-10-05T08:30:45.000Z`. Si la fuente usa UTC, debe configurarse `UTC`; no se debe inferir sin documentarlo.
6. GeoIP se aplicaría a `bezero_ip`, por ejemplo `geoip { source => "bezero_ip" target => "geo" ecs_compatibility => "disabled" }`, tras disponer de una base GeoIP local válida. Podría añadir país, ciudad y coordenadas según la base. `203.0.113.5` pertenece al rango documental TEST-NET-3: **no inventamos ubicación**. No ejecutamos GeoIP ni descargamos bases en esta práctica.
7. Mutate no es imprescindible: los campos extraídos ya tienen el tipo necesario. Es útil para normalizar nombres, convertir números o retirar el campo temporal después de validar Date. Conservamos el original para auditar el parseo.
8. Documento lógico que podría indexarse:

   ```json
   {"@timestamp":"2026-10-05T08:30:45.000Z","timestamp":"2026-10-05 10:30:45","maila":"ERROR","zerbitzua":"nginx","mezua":"Connection refused","bezero_ip":"203.0.113.5","message":"2026-10-05 10:30:45 ERROR nginx 'Connection refused' client=203.0.113.5"}
   ```

   El laboratorio emite JSON por stdout; no lo envía a Elasticsearch. Logstash puede añadir campos de host, ruta y versión; el documento real queda en las evidencias.

## P19. Logstash edo Ingest Pipeline?

| Caso | Elección | Justificación |
|---|---|---|
| A. JSON ya enviado a Elasticsearch, añadir campo | Ingest Pipeline, procesador `set` | Transformación sencilla dentro del destino existente. |
| B. Recibir Filebeat, Kafka y base de datos | Logstash | Inputs distintos, coordinación de ingesta y plugins para cada fuente. |
| C. Renombrar campo de documentos destinados a Elasticsearch | Ingest Pipeline, procesador `rename` | Transformación sencilla sin incorporar un proceso externo. |
| D. Consumir Kafka, condiciones y dos destinos | Logstash | Permite condiciones y varios outputs; un ingest pipeline no distribuye a destinos externos. |

Son decisiones para los requisitos descritos; no implican que exista una única arquitectura válida ante requisitos distintos.

## P20. Pipeline akastun bat konpondu

1. **El pattern original puede coincidir parcialmente**: al no estar anclado, Grok puede encontrar `83.45.120.10 GET /api 500` dentro de la línea y omitir la fecha. Por eso una ausencia de `_grokparsefailure` no prueba que el log completo se interprete correctamente.
2. Falta capturar el prefijo `05/Oct/2026:14:32:10` y anclar la línea. Usamos:

   ```text
   ^(?<timestamp>%{MONTHDAY}/%{MONTH}/%{YEAR}:%{TIME}) %{IP:bezero_ip} %{WORD:metodoa} %{URIPATHPARAM:request} %{INT:status_code:int}$
   ```

3. Falta Date: `match => ["timestamp", "dd/MMM/yyyy:HH:mm:ss"]`, `locale => "en"` para `Oct` y zona explícita `Europe/Madrid`. El grupo nombrado captura la fecha sin offset; `HTTPDATE` estándar exige también el offset y falla con estas entradas. Date interpreta el formato capturado.
4. `status_code` debe ser entero para comparación numérica. La conversión `:int` dentro de Grok evita comparar strings; también podría hacerse con Mutate tras el parseo.
5. Antes de arrancar: pegar log/pattern en Grok Debugger. La sintaxis del pipeline se puede validar con Logstash `--config.test_and_exit`; ninguna de las dos comprobaciones sustituye ejecutar Date y revisar el evento completo.
6. [p20.conf](pipelines/p20.conf) corrige Grok/Date. Para conservar el input del ejercicio original, sustituir el bloque `file` por `beats { port => 5044 }`; el filtro no cambia. Para enviar a un Elasticsearch del laboratorio, sustituir stdout por el output autorizado y configurar su URL/autenticación. Nuestra variante ejecutable usa el archivo solicitado en el reto y stdout para comprobar eventos sin modificar índices.

### Reto: ejecutar las tres líneas

[compose.yaml](compose.yaml) monta [web.log](fixtures/web.log) y el pipeline como solo lectura; no publica puertos ni usa red. Desde esta carpeta:

```bash
docker compose -p aabd-elastic-20261008 config
docker compose -p aabd-elastic-20261008 up --abort-on-container-exit --exit-code-from logstash
```

Necesita la imagen local `docker.elastic.co/logstash/logstash:9.5.4`. `file` funciona en modo lectura, conserva el archivo y termina al acabar. El registro de archivos completados va a `/tmp` del contenedor. `sincedb_path=/dev/null` es una elección explícita de **replay docente**: cada arranque vuelve a leer todo. No usar esta política para una ingesta incremental de producción.

## P21. Log berriak prozesatu

[web_ampliado.log](fixtures/web_ampliado.log) conserva las tres líneas y añade literalmente las tres del 6 de octubre. Se reinicia Logstash con **el mismo p20.conf**, cambiando únicamente el archivo montado; `ejecutar.sh` lo hace en un contenedor independiente.

Los códigos son `500, 200, 404, 200, 401, 403`. Los errores son `/api` (500), `/produktuak` (404), `/login` del 6 de octubre (401) y `/produktuak` con DELETE (403). POST/DELETE cumplen `%{WORD}` y las rutas cumplen `%{URIPATHPARAM}`: **no hace falta cambiar el pipeline**.

La prueba vuelve a leer seis eventos por la política de replay. No demuestra lectura exclusiva de las líneas nuevas. Para eso se necesita sincedb persistente y conservar identidad del archivo; aquí no se indexan documentos ni se generan duplicados en Elasticsearch.

## P22. HTTP erroreak identifikatu

[p22.conf](pipelines/p22.conf) añade al final del filtro, tras validar Grok y Date:

```text
if "_grokparsefailure" not in [tags] and "_dateparsefailure" not in [tags] and [status_code] >= 400 {
  mutate { add_tag => ["errorea"] }
}
```

Los cuatro eventos con códigos 500, 404, 401 y 403 reciben `errorea`. Los dos eventos 200 no la reciben. 500 sí la recibe. La comparación opera sobre enteros; 4xx indica error de cliente y 5xx error del servidor. Un parseo fallido debe investigarse, no presentarse como una petición HTTP exitosa.

## Reproducción y alcance de la verificación

Desde esta carpeta, Bash, Docker y Python 3 estándar, sin dependencias Python externas:

```bash
bash ejecutar.sh
python3 verificar.py
```

El script arranca cinco contenedores aislados, con red deshabilitada y recursos limitados, y conserva los contenedores finalizados. No modifica contenedores existentes, índices ni volúmenes. Sobrescribe sus registros `evidencias/*.stdout.log`, eventos JSON y `validacion.json`; copiar esos archivos si se necesita conservar otra ejecución.

[verificar.py](verificar.py) comprueba cantidades 1/3/6/6, campos extraídos, códigos enteros, fechas UTC concretas, POST/DELETE, ausencia de fallos de Grok/Date y equivalencia exacta entre código >=400 y etiqueta. Los asserts validan las entradas del PDF; no prueban cualquier formato de log, zonas horarias distintas, ingestión Beats, GeoIP, indexación en Elasticsearch ni GUI Kibana.

## Resultado observado el 8 de octubre

Logstash 9.5.4 ejecutado realmente en cuatro contenedores: P18 un evento, P20 tres, P21 seis y P22 seis. Todos los asserts pasaron. P22 produjo cuatro etiquetas `errorea`, ninguna en los dos eventos 200. [validacion.json](evidencias/validacion.json) y los archivos `*.events.json` conservan los resultados. Compose validado con `config --quiet` y ejecutado con `compose up --abort-on-container-exit --exit-code-from logstash`: tres eventos y exit 0, [registro](evidencias/compose-p20.log). Los demás casos se ejecutaron con `docker run`. Ruff y sintaxis Bash también comprobados. Grok Debugger GUI validado para P18 y seis entradas P20/P21: [valores extraídos](evidencias/grok_gui.json), [captura P20](evidencias/p20-grok.png) y [captura P21](evidencias/p21-grok.png). Se observó también el matching parcial del pattern original.

## Casos negativos y laboratorio GUI

[invalid.log](fixtures/invalid.log) prueba prefijo inesperado, código ausente, sufijo inesperado y 31 de febrero. Los tres primeros reciben `_grokparsefailure`; la fecha imposible recibe `_dateparsefailure`; ninguno recibe `errorea`. [Eventos reales](evidencias/p22_invalid.events.json). Estos fallos esperados quedan explícitos: no se silencian ni se consideran solicitudes HTTP correctas.

Para reproducir la GUI, desde esta carpeta: `docker compose -f compose-gui.yaml -p aabd-elastic-gui-20261008 up -d --pull never`; abrir `http://127.0.0.1:15601/app/dev_tools#/grokdebugger`. La configuración usa ES/Kibana 9.5.4, puertos 19200/15601 en loopback, volumen propio y límites de memoria. Necesita unos 2 GB adicionales de memoria. Al terminar, `docker compose -f compose-gui.yaml -p aabd-elastic-gui-20261008 stop`; conserva el volumen y contenedores. Ambos servicios se detuvieron tras la prueba. Esta instancia solo se empleó como Grok Debugger; no se afirma indexación del pipeline en Elasticsearch.
