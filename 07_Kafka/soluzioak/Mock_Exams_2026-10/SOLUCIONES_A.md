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
Reentrega de 5 no entra otra vez. ID dedup persistente, aislamiento por estación,
estado de lote recuperable e ID determinista de agregado. Crash tras publicar
Gold antes de commit puede republicar agregado: destino idempotente o
transacción Kafka con offsets si todo está en Kafka y consumidores adecuados;
MongoDB/ficheros requieren estrategia propia, no quedan cubiertos automáticamente.
Lote puede tardar indefinidamente; ventana corresponde a tiempo e implica
watermarks/late events y política de cierre según implementación. API caída:
registrar respuesta, backoff acotado, no sustituir fuente sin marcarla; fixture
prueba transformación. Puntos 0.75/0.5/0.75/0.5.

## 5 — 1.5 puntos

Source lee externo y produce; sink consume y escribe. Worker ejecuta Connect,
connector configura integración, tasks unidades de trabajo (cantidad posible
depende del conector). Serializer convierte objetos de cliente a bytes;
converter conecta formato Kafka y representación Connect, revisar schemas.enabled
y contrato. Plugin debe existir en worker; comprobar estado del connector y
cada task, offsets y logs. Prueba: fichero sintético 10 IDs, leer topic y destino,
comparar IDs/conteo/contenido; reinicio controlado y volver a comprobar repetición
y commits. Un JSON aceptado por REST o RUNNING no prueba llegada al destino.
No reportar esta prueba como ejecutada. 0.5 por apartado.
