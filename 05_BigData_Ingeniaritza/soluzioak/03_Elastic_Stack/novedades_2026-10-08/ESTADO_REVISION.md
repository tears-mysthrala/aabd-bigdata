# Revisión de Moodle — 2026-10-08

- Checkout inicial: `integration/moodle-sync-2026-10-06`, detrás de su remoto en dos commits. Conservados sus cambios preexistentes; no se ejecutó stash, reset ni checkout sobre ellos.
- Base integrada consultada: `origin/master`, `f370965` (PR #16 integrada según historial Git remoto).
- Snapshot nuevo: `origin/moodle-sync/master/2026-10-08`, `4c2fe5b88f67`, todavía distinto de master en tres archivos: manifiesto, cuaderno del tema 3 y PDF Elastic Stack.
- Servicio real de las 09:01 CEST: salida 0, 13 secciones, 74 actividades, 0 errores, 0 fuentes inaccesibles. Timer activo. No se inició otro ciclo ni se cambiaron credenciales.
- Manifiesto local: 79 archivos con SHA-256 coincidente, verificados de nuevo. Misma lista de 11 tareas que master; ninguna tarea de entrega nueva. Una actividad adicional respecto al recuento histórico no implica otra tarea pendiente.
- Cuaderno tema 3: añadidos ejemplos curl de salud/predicción, uso de `.env`/`load_dotenv` y ajustes de texto/metadata. No añade un enunciado de ejercicio respecto a la base comparada.
- Elastic Stack: cinco ejercicios nuevos P18–P22. Respuestas y pipelines en este directorio. En P20 el pattern original sin anclaje puede coincidir parcialmente, omitiendo la fecha. La primera prueba detectó que HTTPDATE exige offset; se sustituyó por captura explícita de fecha sin zona. Primeros registros conservados en `evidencias/primer_intento/`.
- Las soluciones del 7 de octubre ya figuran en master: seguridad/privacidad, Pipeline/API, series temporales y Kafka. No se presentan sus evidencias históricas como ejecuciones de hoy.
- Trabajo inicial separado en la rama `feat/elastic-p18-p22-2026-10-08`. El trabajo actual está consolidado en el checkout principal; desde la raíz del repositorio: `cd 05_BigData_Ingeniaritza/soluzioak/03_Elastic_Stack/novedades_2026-10-08`.
- Pendientes que no se confunden con código: publicación/integración de este trabajo y cualquier entrega personal en Moodle. Propuestas del reto: IDs 63276 (13 de octubre, 14:30) y 63277 (14 de octubre, 14:30); requieren información del equipo, no se inventa.

## Cierre de la ampliación

Trabajo actual en `feat/ejercicios-moodle-2026-10-08`, dentro del checkout principal. El checkout separado anterior conserva su estado previo. El ciclo de las 11:02 verificó 77 actividades y no añadió novedades respecto a las 10:02. Snapshot `92752dc40fb0`; se incorporaron dos PDF Boosting. Grok Debugger P18/P20 y seis líneas P20/P21 ejecutados, Compose P20 ejecutado y cuatro negativos de P22 verificados. Servicios GUI detenidos. [Informe conjunto](../../../../00_Transversal/validaciones_2026-10-08/README.md).
