# Soluciones y rúbrica — Reto integrado CNC Guard, simulacro A

[Volver al examen](../../materialak/Mock_Exams_2026-10/EXAMEN_A.md).
Corrección propuesta, no baremo docente. Se admiten alternativas coherentes con
los requisitos. Concede crédito parcial por razonamiento correcto aunque haya
un error aritmético posterior; no cuentes dos veces el mismo mérito.
Los valores calculados son respuestas de casos sintéticos, no resultados de planta.

## 1 — 1.5 puntos

Ejemplo: detectar fallo en las próximas 24 h, con recall y presupuesto de falsas
alarmas evaluados en un holdout. Correctivo interviene tras fallo; predictivo usa
señales previas. Indicadores: horas de parada evitadas y coste de inspecciones.
La etiqueta debe corresponder al horizonte. Datos sintéticos no prueban patrones
reales, transferibilidad ni costes evitados. Requiere evaluación prospectiva,
revisión experta y procedimiento de actuación autorizado. Puntúa los tres
subapartados con 0.5 cada uno.

## 2 — 2 puntos

Intervalos desde día 0: A 0–2, B 2–5, C 2–6, D 5–7, E 7–10, F 10–11.
Camino A–B–D–E–F, **11 días**; C puede acabar en 7, holgura **1 día**.
Retrasar C un día no retrasa F; dos días sí lo retrasan uno, con el resto igual.
Con una persona las 15 jornadas de trabajo deben serializarse; una secuencia
válida es A,B,C,D,E,F y termina en día 15. La ruta crítica del modelo sin
restricción de recursos no basta para resolver ese calendario. Rúbrica según
los cuatro importes del enunciado.

## 3 — 2 puntos

Sensor genera; Kafka amortigua/transmite eventos; NiFi enruta y valida; histórico
conserva originales y limpios; modelo produce score; visualización muestra
alertas para revisión. Aceptar otras arquitecturas con funciones claras.
Campos: event_id, makina_id, timestamp UTC, temperatura °C, vibración con unidad,
quality. Deduplicar por identificador, registrar rechazos y huecos; mantener
versión de reglas/modelo y procedencia. Roles del contrato: coordinador organiza
pasos y controla entregas; secretario registra acuerdos y conserva documentos;
portavoz comunica decisiones del equipo. Explicar tareas de dos de ellos.
No afirmar latencia ni uptime sin medir.

## 4 — 2 puntos

R1=min(0.7,0.4)=**0.4**, R2=**0.3**. Fuzzificación → inferencia/agregación →
defuzzificación. Sin funciones de pertenencia de salida y dominio no existe
centroide determinado: no basta promediar etiquetas. Sistema experto usa reglas
explícitas; fuzzy permite grados; anomalías detecta rareza, que no equivale a
fallo. En el híbrido, la regla experta decide que se necesita refrigeración y
el controlador fuzzy gradúa su intensidad; no se exige una regla de fusión de
scores de modelos distintos. 0.5 por cada apartado.

## 5 — 2.5 puntos

N=1000. Recall=30/50=**0.60**; precisión=30/130=**0.2308**;
accuracy=880/1000=**0.88**. Coste FN=20×2×1200=48.000 €;
FP=100×40=4.000 €; total **52.000 €**, bajo las hipótesis dadas.
No es ahorro: falta coste del baseline y de implantación.
Para nuevas máquinas, separar grupos de máquinas; para futuro, corte temporal.
Seleccionar umbral/modelo en validación y dejar test final cerrado. Si el objetivo
combina grupos y tiempo, diseñar ambos límites. Informe: precisión baja implica
muchas inspecciones; recall pierde 40% de fallos; comparar baseline y recoger
más datos reales antes de automatizar. Evidencias individuales: commits propios,
registro de decisiones o pruebas realizadas, identificados sin atribuir trabajo
ajeno. Puntos: 0.75/0.5/0.5/0.5/0.25.
