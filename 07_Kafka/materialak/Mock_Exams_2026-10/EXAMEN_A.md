# Simulacro A — Kafka básico y avanzado

Elaboración propia, 9 de octubre de 2026. Basado en la materia local disponible;
no es un examen oficial ni una predicción de preguntas del profesorado.
Duración propuesta: **110 minutos**. Nota máxima: **10 puntos**.
Los tiempos, reparto de puntos y condiciones son de autoestudio, salvo el formato
3 + 7 de Programación documentado en su guía docente.

## Condiciones y entrega

Resuelve primero sin abrir la [solución y rúbrica](../../soluzioak/Mock_Exams_2026-10/SOLUCIONES_A.md).
Teoría sin apuntes; práctica con copias locales de los apuntes, sin Internet ni IA.
Calculadora básica permitida en cálculos. Entrega respuestas razonadas y, donde
se pida código, notebook o script con salidas y explicación. No basta nombrar una
herramienta: justifica su elección. Los casos y números nuevos son sintéticos.
No necesitas levantar servicios para los apartados de diseño o traza.

## Materia de referencia

- [01_03_ApacheKafka.pdf](../01_03_ApacheKafka.pdf)
- [01_04_ApacheKafka_aurreratua.pdf](../01_04_ApacheKafka_aurreratua.pdf)

## 1. Conceptos y claves (2 puntos; 20 min)

Define topic, partición, offset y consumer group (0.75). Explica orden dentro
de una partición frente a orden global y qué aporta key=makina_id (0.5).
Distingue broker/leader/réplica/ISR (0.5). Explica por qué bootstrap no contiene
necesariamente todos los brokers y el papel del listener anunciado (0.25).

## 2. Particiones y grupos (2 puntos; 20 min)

Topic con 3 particiones y RF=2 sobre 3 brokers. Cuatro consumidores del mismo
grupo están activos. ¿Cuántos pueden leer particiones simultáneamente y qué pasa
con el cuarto? (0.5). Python y NiFi deben recibir ambos todos los mensajes:
¿qué grupos configurarías y por qué? (0.5). Consumer confirmó offset 8 como
**siguiente a leer** y procesó mensaje 8, pero cae antes de confirmar 9. Indica
qué repetirá al arrancar y el riesgo al escribir en MongoDB (0.5).
Explica cuándo auto_offset_reset='earliest' actúa y cuándo no (0.5).

## 3. Disponibilidad y diagnóstico (2 puntos; 20 min)

Partición: leader B1, replicas=[B1,B2], ISR=[B1,B2]. min.insync.replicas=2;
producer acks='all'. Cae B2. ¿Se aceptan nuevas escrituras? Justifica (0.75).
Después cae B1: ¿puede B3 convertirse en leader de esta partición sin más? (0.5).
Explica por qué RF=3 no es posible con 2 brokers y por qué RF no aumenta el número
de particiones útiles para consumidores (0.5). Propón una comprobación de describe
que diferencie réplica asignada de ISR (0.25).

## 4. Diseño Bronze/Silver/Gold (2.5 puntos; 30 min)

Bronze recibe once mensajes válidos para una sola estación, con temperaturas
1,2,...,11 °C, event_id únicos; se reentrega el de temperatura 5. Silver conserva
estación, timestamp, temperatura y event_id. Gold agrupa lotes de diez eventos
únicos. Define roles de capas y grupos para fichero/MongoDB/Gold independientes
(0.75); calcula count/media/máximo del primer lote y destino del resto (0.5);
diseña deduplicación y explica fallo entre salida y commit, sin prometer exactly-once
solo por usar Kafka (0.75); compara lote de diez eventos con ventana temporal
por estación y tratamiento de API caída (0.5).

## 5. Kafka Connect y verificación (1.5 puntos; 20 min)

Se requiere fichero → Kafka → otro fichero. Elige source/sink y distingue
worker, connector y task (0.5). Describe serializers de un producer frente a
converters de Connect, plugin y estado de tasks a verificar (0.5).
Define una prueba local de diez registros, reinicio y control de duplicados,
distinguiendo configuración preparada de ejecución verificada (0.5).
No levantes ni reinicies servicios para este examen escrito.
