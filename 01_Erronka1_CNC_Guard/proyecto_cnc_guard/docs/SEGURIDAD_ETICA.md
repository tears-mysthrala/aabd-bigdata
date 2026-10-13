# Seguridad, privacidad y riesgos de CNC Guard

Prototipo de mantenimiento sintético: NO controla actuadores de la CNC, NO
es un componente de seguridad ni se utiliza para una parada de emergencia.

| Riesgo | Control y evidencia |
|---|---|
| Telemetría corrupta | validación de tipos/rangos, hash, cuarentena, pruebas |
| Replay/duplicados | event_id estable, índice por ID, probar replay |
| Envenenamiento/leakage | source hashes, holdout temporal, train independiente |
| API no disponible | /health, fail closed, retry acotado y DLQ |
| Acceso no autorizado | bind 127.0.0.1 en local, autenticación/TLS al salir |
| Sesgo o errores diagnósticos | matrices FP/FN, revisión humana, trazabilidad |
| Privacidad laboral | no recolectar operadores, minimizar, justificar retención |
| Recuperación ante caída | backups, restauración, simulación y evidencias reales |

SHA-256 aislado no prueba autenticidad si el atacante puede alterar datos
y hash simultáneamente. Para integridad real, autenticar productor, transporte
y consumidores y controlar accesos y firmas donde aplique.

El Reglamento UE 2024/1689 (AI Act), consolidado con cambios de julio de
2026, exige clasificar el sistema por USO PREVISTO, no simplemente por
utilizar ML en una máquina. Un módulo de eficiencia no es automáticamente
componente de seguridad. Si una función defectuosa puede poner en peligro
la salud/seguridad o forma parte de un producto sujeto a conformidad
especial, reevaluar alcance, obligaciones y roles jurídicos.

Fuentes:
https://eur-lex.europa.eu/eli/reg/2024/1689/spa
https://eur-lex.europa.eu/eli/reg/2026/1744/oj

La telemetría de máquina puede convertirse en dato personal si se vincula
a un operador o turno identificable. El proyecto actualmente usa datos
sintéticos; para datos reales habría que evaluar base jurídica, retención,
evaluación de riesgos y transparencia laboral. No automatizar decisiones
sobre trabajadores.

Para el laboratorio, los templates ES usan 0 réplicas deliberadamente;
eso NO aporta continuidad tras caída del único nodo. Para producción
se necesitan réplica, monitorización, restauración y tests reales.
