# Compose docente nuevo — 7 de octubre

El [Compose original](../../materialak/compose.yaml) incorporado a las 14:01 es material de apoyo para Elasticsearch/Kibana 9.5.4; no añade un enunciado nuevo. Conservamos la [resolución existente](README.md) y sus evidencias históricas, sin declararlas ejecuciones de hoy.

El original publica puertos en todas las interfaces y desactiva autenticación. Para el laboratorio se usa el [Compose de soluzioak](compose.yaml), que conserva las mismas imágenes y restringe 9200/5601 a `127.0.0.1`, con memoria documentada. No arrancar directamente la copia de materialak en una red compartida.

Comprobación de hoy desde esta carpeta:

```bash
docker compose config --format json
```

Se han verificado las dos imágenes y que los dos puertos tienen `host_ip=127.0.0.1`. Es validación de configuración; no se han iniciado servicios ni modificado volúmenes durante esta tarea. Antes de iniciar, revisar puertos y contenedores existentes; el Compose tiene nombres fijos. La receta no acredita autenticación, TLS ni seguridad de producción. No se usa `down -v` ni se borra evidencia anterior.
