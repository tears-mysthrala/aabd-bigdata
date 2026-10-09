# Simulacros basados en la materia disponible — octubre de 2026

Preparados el **9 de octubre de 2026** a partir de fuentes locales docentes.
Un modelo completo por asignatura/bloque, con soluciones separadas. Están en
castellano; las referencias conservan nombres y terminología originales en euskera.
No se han consultado exámenes privados ni se predicen preguntas oficiales.

## Elegir simulacro

NiFi y Kafka se presentan separados por su extensión como bloques de Big Data
aplicado; CNC Guard es un reto transversal, no una asignatura adicional.

| Asignatura o bloque | Tiempo propuesto | Enunciado | Soluciones y rúbrica |
|---|---:|---|---|
| Reto integrado CNC Guard | 120 min | [Modelo A](../../01_Erronka1_CNC_Guard/materialak/Mock_Exams_2026-10/EXAMEN_A.md) | [Corrección](../../01_Erronka1_CNC_Guard/soluzioak/Mock_Exams_2026-10/SOLUCIONES_A.md) |
| 5071 — Modelos de inteligencia artificial | 110 min | [Modelo A](../../02_AA_Ereduak_5071/materialak/Mock_Exams_2026-10/EXAMEN_A.md) | [Corrección](../../02_AA_Ereduak_5071/soluzioak/Mock_Exams_2026-10/SOLUCIONES_A.md) |
| 5072 — Machine Learning | 120 min | [Modelo A](../../03_ML_5072/materialak/Mock_Exams_2026-10/EXAMEN_A.md) | [Corrección](../../03_ML_5072/soluzioak/Mock_Exams_2026-10/SOLUCIONES_A.md) |
| 5073 — Programación para IA | 150 min | [Modelo A](../../04_Programazioa_5073/materialak/Mock_Exams_2026-10/EXAMEN_A.md) | [Corrección](../../04_Programazioa_5073/soluzioak/Mock_Exams_2026-10/SOLUCIONES_A.md) |
| Big Data e ingeniería de datos | 120 min | [Modelo A](../../05_BigData_Ingeniaritza/materialak/Mock_Exams_2026-10/EXAMEN_A.md) | [Corrección](../../05_BigData_Ingeniaritza/soluzioak/Mock_Exams_2026-10/SOLUCIONES_A.md) |
| NiFi y series temporales | 120 min | [Modelo A](../../06_NiFi/materialak/Mock_Exams_2026-10/EXAMEN_A.md) | [Corrección](../../06_NiFi/soluzioak/Mock_Exams_2026-10/SOLUCIONES_A.md) |
| Kafka básico y avanzado | 110 min | [Modelo A](../../07_Kafka/materialak/Mock_Exams_2026-10/EXAMEN_A.md) | [Corrección](../../07_Kafka/soluzioak/Mock_Exams_2026-10/SOLUCIONES_A.md) |

## Cómo hacerlos

1. Abre únicamente el enunciado. Prepara papel, temporizador y material permitido.
2. Respeta tiempos; registra dudas y deja visibles cálculos y justificaciones.
3. En prácticas con código conserva salidas propias: si no puedes ejecutar, marca
   «preparado sin ejecutar», no inventes métricas ni capturas.
4. Abre después la solución. Anota puntos por apartado y una causa por error:
   concepto, lectura, cálculo, implementación o interpretación.
5. Repasa la fuente enlazada de los apartados fallados y repite con datos nuevos.

Todos puntúan sobre 10; los baremos y tiempos son propuestos. Solo Programación
toma el **formato docente documentado** de 30 test (3 puntos) + práctica (7 puntos),
sin Internet/IA y con PDFs locales en la práctica. La fórmula concreta de
penalización del test es propuesta: la guía local no proporciona cuantía.
Para los demás no se conoce aquí un formato oficial por asignatura.

El alcance es **materia disponible**, no certificación de qué se ha impartido ya
ni cobertura de todo el currículo del curso. Cada enunciado enlaza sus fuentes;
la [matriz de cobertura](COBERTURA.md) explica decisiones y límites.

## Datos y ejecución

Programación incluye [CSV nuevo sintético](../../04_Programazioa_5073/data/mock_exams_2026_10/refrigeracion.csv)
y [procedencia/esquema](../../04_Programazioa_5073/data/mock_exams_2026_10/README.md).
ML usa Iris incluido en sklearn. Otros casos usan datos pequeños dentro del
propio enunciado. No hay cuentas, llamadas API ni servicios obligatorios.
Las soluciones de arquitectura/Connect/NiFi no prueban servicios ejecutados.

[Comprobaciones locales del paquete](VALIDACION.md).
