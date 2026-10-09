# Simulacro A — NiFi y series temporales

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

- [01_01_ApacheNifi.pdf](../01_01_ApacheNifi.pdf)
- [GIDA Apache NiFi instalazioa eta kasu praktikoak 1-2-3-4.pdf](<../GIDA Apache NiFi instalazioa eta kasu praktikoak 1-2-3-4.pdf>)
- [01_02_ApacheNifi_aurreratua.pdf](../01_02_ApacheNifi_aurreratua.pdf)
- [Apache NiFi kasu praktikoak (5-6-7).pdf](<../Apache NiFi kasu praktikoak (5-6-7).pdf>)
- [02_Denbora_Serieak.pdf](../02_Denbora_Serieak.pdf)

## 1. Modelo de flujo (2 puntos; 20 min)

Explica content/attributes de FlowFile (0.5), Processor/Connection/Relationship
y back pressure (0.5), Controller Service de Reader/Writer frente al procesador
(0.5) y provenance frente a logs de ejecución (0.5).

## 2. CSV → JSON y destinos (2.5 puntos; 30 min)

CSV sintético con cabecera `id,ciudad,precio,unidades`: fila 1 Eibar,10,2;
fila 2 Bilbao,-3,1; fila 3 Eibar,5,4. Diseña ingesta de carpeta, conversión con
ConvertRecord, validación de precio no negativo y selección de Eibar con
QueryRecord; muestra salida esperada (1). Define Reader, Writer y tipos (0.5).
Añade atributos de fuente/fecha y destino local que gestione colisión de nombre
sin sobrescritura silenciosa (0.5). Describe rutas failure/retry y cómo comprobar
conteos y contenido, sin confundir FlowFiles con registros (0.5).

## 3. Integración y medallion (2 puntos; 25 min)

Diseña MariaDB → NiFi → MongoDB: extracción SQL, conversión y escritura,
indicando connection service, control de duplicados y evidencia (0.75).
API HTTP → Bronze/Silver/Gold: funciones de capas y agregación de diez lecturas
(0.75). Si API devuelve 405, explica diagnóstico y cómo probar con fixture sin
atribuir datos simulados a la API (0.5).

## 4. Práctica de tiempo (2.5 puntos; 30 min)

Una sola máquina, UTC, una fila por minuto (vacío = NaN):

```csv
timestamp,temperatura,kwh_intervalo
2026-10-09T08:00:00Z,40,1
2026-10-09T08:01:00Z,52,1
2026-10-09T08:02:00Z,54,2
2026-10-09T08:03:00Z,56,2
2026-10-09T08:04:00Z,,1
2026-10-09T08:05:00Z,44,1
```

Escribe Pandas para parsear/ordenar índice y seleccionar 08:01–08:03 inclusivo
(0.5). Calcula media del intervalo, resample de temperatura a 5 min con ventanas
[08:00,08:05), [08:05,08:10) y suma de kWh por ventana (0.5).
Interpola temperatura por tiempo, rolling de tres lecturas con min_periods=3,
y calcula primera media válida (0.5). Detecta **inicio de episodio** de tres
lecturas originales consecutivas >50, separadas un minuto, con NaN/hueco como
ruptura; indica el instante de alerta (0.5). Explica diferencias size/count,
resample/rolling y riesgo de interpolar con futuro para predicción (0.5).

## 5. Dimensionamiento e interpretación (1 punto; 15 min)

20 máquinas envían por segundo un mensaje con temperatura y vibración. Cada
valor ocupa 100 bytes. Calcula mensajes/s, valores/s y MB decimales/día de valores
sin overhead (0.5). Explica qué ocultan medias de 10 min y cómo agregar
kWh de intervalo frente a kW o contador acumulativo (0.5).
