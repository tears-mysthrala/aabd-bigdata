# Comprobaciones locales — 9 de octubre de 2026

[Índice](README.md). Validación de este paquete, no de entregas ni examen oficial.

## Comprobado

- Siete enunciados y siete soluciones separados; 10 puntos cada uno; suma de
  tiempos por apartado coherente. Programación: 30 preguntas/120 opciones,
  clave de 30 respuestas, teoría 3 puntos y práctica 7 puntos.
- **75 enlaces locales** de referencias y navegación verificados con resolución de rutas; revisión
  de cálculos PERT, métricas, costes, volumen, join, ventanas y lote Kafka.
- CSV sintético: 322 registros, 2 duplicados y 12 inválidos; quedan 308 registros,
  32 positivos. Separación por cámaras: train 231/24 positivos, test 77/8.
- Código de referencia de Programación extraído del Markdown y ejecutado desde
  carpeta temporal con el Python del entorno existente de la práctica Moodle
  64153. Se comprobaron limpieza, split, pipeline, métricas y validadores Pydantic.
  No se instalaron dependencias ni se sobrescribieron resultados previos.
- Código de referencia de ML, incluido el gráfico 2D, ejecutado con backend Agg
  en carpeta temporal y el entorno existente de Boosting. Dos pipelines, CV de
  KNN, matrices de test y figura; no se descargó Iris ni se tocaron servicios.

- Código Pandas del caso de NiFi ejecutado: selección inclusiva, medias/sumas
  de ventanas, interpolación, rolling y alerta en 08:03 comprobadas por asserts.
- Figura 2D de Iris revisada visualmente: paneles de LogReg/KNN, puntos de train,
  ejes con unidades y leyendas de tres clases. No se guarda en la entrada del examen.
- `git diff --check` sin errores. Se añadió navegación en `INDICE.md`; se
  conservaron cambios previos. Estas comprobaciones se realizaron antes de publicar.
  La publicación Git posterior no supone una entrega en Moodle.

SHA-256 del CSV de entrada:
`5d5ef215eb21486ad569b870518f6519ff05f415ffb58531db9942bbf9fa514b`.

Resultados de esta ejecución, útiles para contrastar pero no exigidos como
valores universales en la corrección:

| Caso | Resultado local |
|---|---|
| Programación modelo | accuracy 0.9610; balanced accuracy 0.9783; recall 1.0000; precision 0.7273; F1 0.8421 |
| Programación matriz | [[66,3],[0,8]], filas reales y columnas predichas |
| Programación siempre 0 | accuracy 0.8961; balanced accuracy 0.5; recall/F1 0 |
| Iris LogReg 4D | accuracy 0.9111; matriz [[15,0,0],[0,14,1],[0,3,12]] |
| Iris KNN 4D | accuracy 0.9333; matriz [[15,0,0],[0,15,0],[0,3,12]] |

## Límites

Resultados sintéticos; el recall perfecto en ocho positivos no valida una planta.
Las métricas dependen de datos, versiones y protocolo; conservar la frontera de
test importa más que reproducir a ciegas una cifra. La ejecución del código de
referencia no constituye la entrega del alumno. Arquitecturas, políticas ILM,
caídas de broker, conectores y flujos son respuestas propuestas: no se han
aplicado a servicios. No se ha subido nada a Moodle. La publicación e integración Git se comprueban por separado.

## Revalidación al integrar

El 9 de octubre se volvieron a comprobar los 75 enlaces y se ejecutaron de nuevo
los bloques de código revisados de Programación, ML y NiFi en carpeta temporal,
con el entorno uv existente de la práctica 64153. Se comprobaron también
las medias del scaler frente a train, ventanas, relleno y alerta de NiFi.
[Resultados actuales](REVALIDACION_INTEGRACION.json): mismos conteos, matrices
y métricas que el registro anterior; sin modificar entradas ni servicios.
