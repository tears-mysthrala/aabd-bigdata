# Kibana: especificación para entrega CNC Guard

Estado: DISEÑADO, NO IMPORTADO ni probado con datos reales de CNC Guard.
No presentar pantallazos de otras prácticas como si fuesen del reto.

Crear data views cnc-telemetry-* y cnc-alerts-* por @timestamp.

1. Series de temperatura, vibración y presión por máquina (media y P95).
2. Probabilidad de fallo por ventana temporal: P95 y máximo claramente
   etiquetados; el máximo es útil para inspección, no una media.
3. Métricas: número de AVISO/CRITICA, número de máquinas con datos, eventos
   rechazados, porcentaje de history_available y rango temporal seleccionado.
4. Histograma/heatmap de alertas por machine_id y franja horaria.
5. Tabla de alertas CRITICA con event_id, timestamp, probabilidad y enlace
   al documento de telemetría. Verificar consistencia por event_id.
6. Filtros interactivos por máquina, fecha y nivel; capturas de KPI y casos.

Guardar export NDJSON de objetos Kibana y capturas reales del panel una vez
esté levantado. No se incluye un dashboard falsamente marcado operativo.
