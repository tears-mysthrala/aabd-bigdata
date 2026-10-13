# Simulacro A — Reto integrado CNC Guard

Elaboración propia, 9 de octubre de 2026. Basado en la materia local disponible;
no es un examen oficial ni una predicción de preguntas del profesorado.
Duración propuesta: **120 minutos**. Nota máxima: **10 puntos**.
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

- [1Erronka_ikaslearen_txostena.docx.pdf](<../1Erronka_ikaslearen_txostena.docx.pdf>)
- [ANEXO1-Eus.md](<../ANEXO1-Eus.md>)
- [patata tortila - planifikazioa eta kostuak lantzekoAA 2026-2027.md](<../patata tortila - planifikazioa eta kostuak lantzekoAA 2026-2027.md>)
- [5071-IE1-Logika_Lausoa.md](<../../../02_AA_Ereduak_5071/materialak/5071-IE1-Logika_Lausoa.md>)
- [5072_2_01_Erregresio_Lineala.pdf](<../../../03_ML_5072/materialak/5072_2_01_Erregresio_Lineala.pdf>)
- [5072_3_Balidazio_Metodologia.pdf](<../../../03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf>)
- [Ariketak_01_02_datuen_ingeniaritza.md](<../../../05_BigData_Ingeniaritza/materialak/Ariketak_01_02_datuen_ingeniaritza.md>)
- [01_01_ApacheNifi.pdf](<../../../06_NiFi/materialak/01_01_ApacheNifi.pdf>)
- [01_03_ApacheKafka.pdf](<../../../07_Kafka/materialak/01_03_ApacheKafka.pdf>)

Correspondencia de cada apartado con páginas y ejercicios docentes:
[matriz de cobertura](../../../00_Transversal/MOCK_EXAMS_2026-10/COBERTURA.md#cnc).

## 1. Objetivo y alcance (1.5 puntos; 15 min)

El reto docente parte de 50 máquinas y un coste de parada de 1.200 €/hora.
Un piloto propio pretende anticipar fallos con sensores. Define: (a) objetivo
medible y ventana de anticipación (0.5); (b) mantenimiento correctivo frente a
predictivo y dos indicadores de negocio (0.5); (c) tres límites de un piloto con
datos sintéticos y una condición antes de actuar en una planta real (0.5).

## 2. Planificación PERT/Gantt (2 puntos; 20 min)

Para este caso se permiten tareas paralelas con personal suficiente:

| Tarea | Duración (días) | Predecesoras |
|---|---:|---|
| A: requisitos | 2 | — |
| B: ingesta | 3 | A |
| C: reglas expertas | 4 | A |
| D: dataset limpio | 2 | B |
| E: evaluación integrada | 3 | C, D |
| F: informe y demo | 1 | E |

Dibuja red y Gantt con inicio/fin temprano (0.75), calcula duración y camino
crítico (0.5), holgura de C (0.25) y explica qué ocurre si C se retrasa un día o
si solo hay una persona que no puede ejecutar dos tareas a la vez (0.5).

## 3. Arquitectura justificable (2 puntos; 25 min)

Diseña el recorrido sensor → ingesta → almacenamiento → modelo → alerta.
Indica papel de Kafka/NiFi, histórico y monitorización (0.75), esquema mínimo
con máquina, instante, unidades y calidad (0.5), tratamiento de duplicados/huecos
y trazabilidad (0.5), tareas de dos roles del contrato docente:
coordinador, secretario o portavoz (0.25).
No conviertas una alerta de laboratorio en una orden de parada.

## 4. Reglas y aprendizaje (2 puntos; 25 min)

Para una lectura se dan μ(temperatura alta)=0.7, μ(vibración alta)=0.4 y
μ(temperatura media)=0.3. Reglas: R1 alta AND vibración alta → riesgo alto;
R2 temperatura media → riesgo medio. Usa AND=min. Calcula activaciones (0.5),
explica las tres fases fuzzy y por qué faltan datos para un centroide numérico
(0.5), compara experto/fuzzy con detector de anomalías sin etiquetas (0.5), y
explica el sistema híbrido experto + fuzzy del apartado 03.4 de Logika Lausoa:
reglas para decidir qué hacer y control gradual para decidir cuánto (0.5).

## 5. Evaluación, coste y defensa (2.5 puntos; 35 min)

Resultados ficticios: TN=850, FP=100, FN=20, TP=30. Cada FN supone dos horas de
parada a 1.200 €/h; cada FP una inspección de 40 €. Calcula recall, precisión y
accuracy (0.75) y coste total del periodo (0.5). Propón validación para máquinas
nuevas y para meses futuros, separando selección y test (0.5). Redacta cinco
líneas para dirección con una decisión prudente (0.5). Enumera dos evidencias
individuales para la defensa sin inventar contribuciones del equipo (0.25).
