# Soluciones y rúbrica — Kafka básico y avanzado, simulacro A

[Volver al examen](../../materialak/Mock_Exams_2026-10/EXAMEN_A.md).
Corrección propuesta, no baremo docente. Se admiten alternativas coherentes con
los requisitos. Concede crédito parcial por razonamiento correcto aunque haya
un error aritmético posterior; no cuentes dos veces el mismo mérito.
Los valores calculados son respuestas de casos sintéticos, no resultados de planta.

## 1 — 2 puntos

Topic es stream lógico; particiones lo distribuyen; offset identifica posición
por partición; grupo coordina consumidores y offsets. Orden garantizado por
partición, no entre particiones. Una clave estable suele llevar la misma máquina
a una partición con particionado estable, pero cambios en particiones o
particionador pueden modificarlo. Broker aloja; leader sirve partición;
replicas copian; ISR subconjunto sincronizado. Bootstrap obtiene metadata;
listeners anunciados deben ser alcanzables desde contexto host/contenedor.
Rúbrica 0.75/0.5/0.5/0.25.

## 2 — 2 puntos

Tres consumidores como máximo con asignación clásica: cuarto sin partición;
no duplica capacidad de este topic. Python/NiFi grupos distintos para cada uno
leer todo; mismo grupo reparte. Offset confirmado 8 implica repetir **mensaje 8**;
MongoDB puede duplicar efecto: usar ID único/upsert y compromiso tras efecto
persistido, sin asumir atomicidad entre sistemas. earliest solo si no hay offset
válido almacenado para esa partición/grupo; no rebobina un grupo con commits
válidos. 0.5 por apartado.

## 3 — 2 puntos

Con ISR reducida a B1, **se rechazan escrituras** con acks=all y min ISR 2;
RF=2 no basta para seguir escribiendo bajo esa política tras perder una réplica.
B3 no tiene réplica asignada de esta partición: no es elegible sin reasignar y
recuperar datos; no afirmar disponibilidad por contar brokers vivos.
RF limitado por brokers distintos disponibles para asignación; replicación copia
particiones, no da particiones extra al grupo. describe muestra Leader, Replicas
asignadas, ISR actual; observar salida tras fallo con timeout y errores, no
inventar una prueba de caída. 0.75/0.5/0.5/0.25.

## 4 — 2.5 puntos

Bronze raw reprocessable; Silver validado; Gold agregado. Grupos independientes
silver-file, silver-db, silver-gold. Primer lote IDs de temperaturas 1..10:
**count=10, media=5.5, max=10**; temperatura 11 pendiente de próximo lote.
Reentrega de 5 no entra otra vez si se reconoce su event_id. Confirmar antes de
procesar puede perder el efecto si se cae después (at-most-once); confirmar
después permite repetirlo si se cae antes del commit (at-least-once). Reconocer
el ID evita contar dos veces; no se exige implementar almacenamiento de estado
ni transacciones distribuidas. Kafka no garantiza automáticamente exactly-once
para MongoDB o ficheros.
Python selecciona campos y agrega un lote de diez con Pandas. NiFi selecciona
campos con EvaluateJsonPath, reconstruye Silver, agrupa con MergeRecord y
agrega con QueryRecord. Ambos persiguen Bronze/Silver/Gold; cambian las
herramientas. Puntos 0.75/0.5/0.75/0.5.

## 5 — 1.5 puntos

JDBC source lee MySQL y produce en Kafka; MongoDB sink consume y escribe en
MongoDB. En el caso docente se detectan nuevos category_id con mode=incrementing.
Worker ejecuta Connect,
connector configura integración, tasks unidades de trabajo (cantidad posible
depende del conector). Serializer convierte objetos de cliente a bytes;
converter conecta formato Kafka y representación Connect; mantener formatos
compatibles. Plugin debe existir en worker; comprobar estado del connector y
cada task, offsets y logs. Prueba: añadir un registro nuevo a categories con un
category_id creciente, observar el topic y buscar el documento en MongoDB;
comparar ID/contenido. Repetir con otro registro distingue avance de una copia
inicial. Un JSON aceptado por REST o RUNNING no prueba llegada al destino.
No reportar esta prueba como ejecutada. 0.5 por apartado.
