# Programación 5073: cómo estudiar y ejecutar las soluciones

[Pipeline y API · ampliación del 7 de octubre](08_Moodle_2026-10-07/README.md): modelos propios, lifespan, etiquetas/probabilidades y HTTP verificado.

Los ejercicios de los **cuadernos** y los de los **PDF** son variantes distintas:
un mismo número puede pedir otra cosa. Consulta primero el enunciado enlazado
en cada guía. Las versiones originales y las descargadas de Drive están en
[materialak/notebooks](../materialak/notebooks/) y
[materialak/](../materialak/), respectivamente;
su procedencia se registra en [MOODLE_URLs.md](../materialak/MOODLE_URLs.md).

| Bloque | Qué aprenderás | Guía y solución |
|---|---|---|
| 01 · Cuaderno de lenguajes | JSON, comprehensions, funciones, archivos y primeros comandos Git | [25 ejercicios explicados](01_Lengoaiak_Ariketak/README.md) |
| 02 · Cuaderno de datos | Arrays, máscaras, carga, limpieza y gráficos | [25 ejercicios explicados](02_Datu_Zientzia_Ariketak/README.md) |
| 03 · PDF de lenguajes | Anatomía de scripts, NIF, formatos, entornos, agentes y Git | [Guía](03_Lengoaiak_PDF_Ariketak/README.md) y [variantes del PDF](03_Lengoaiak_PDF_Ariketak/ariketa_pdf_aldaerak.md) |
| 04 · PDF de datos | NumPy, Pandas, gráficos, DVC y elección de herramientas | [Guía, datos y variantes](04_Datu_Zientzia_PDF_Ariketak/README.md) |
| 05 · PDF de frameworks | scikit-learn, Hugging Face, FastAPI, Streamlit, Gemini y RAG | [26 ejercicios y formas de ejecución](05_Frameworkak_PDF_Ariketak/README.md) |
| 06 · Cuaderno de ML/API | Desbalance, evaluación, Pipeline, persistencia y Pydantic; ampliaciones Drive | [Guía y diferencias entre versiones](06_Programazioa_Ariketak/README.md) |

## Antes de ejecutar

Los comandos de cada guía parten de **la carpeta del bloque**, tras entrar desde
la raíz del repositorio. No copies una `.venv` de otro ordenador: créala e instala
las dependencias indicadas. Si usas Jupyter, selecciona el intérprete de ese
entorno y ejecuta las celdas de arriba abajo tras reiniciar el kernel.
`NameError` suele indicar que falta ejecutar una celda anterior; `FileNotFoundError`
puede indicar una carpeta de trabajo incorrecta o un dato pendiente de obtener.

Los bloques 01, 02 y 06 escriben `data/` respecto al directorio de trabajo.
Los ejercicios de archivos regeneran ejemplos y algunos comandos crean un
repositorio Git o un entorno de prueba. Para repetirlos conservando tus propios
resultados, usa una copia de la carpeta en un directorio de prácticas.

Un `assert` comprueba una condición concreta y se detiene si no se cumple.
`✅ Zuzena!` significa que han pasado las comprobaciones de esa celda; no
certifica todas las propiedades del algoritmo. Ejecuta Python sin `-O`, que
desactiva los asserts. En los ejercicios de ML, interpretar una métrica y sus
límites forma parte de la solución.

## Qué está comprobado

[El registro de 2026-09-28](egiaztapena_2026-09-28.md) describe ejecuciones
históricas y sus límites. Las ampliaciones posteriores deben verificarse con
su versión actual. La [auditoría de cobertura](../../00_Transversal/AUDITORIA_EJERCICIOS.md)
identifica también las entregas que necesitan trabajo de equipo, GUI o APIs.
La revisión documental de 2026-10-01 no convierte esas tareas en entregas realizadas.

## Prácticas complementarias fuera de `soluzioak/`

- [Git 4.2](../git_ariketa_4_2/README.md): script de saludo, tests y simulación
  local de ramas/merge; no equivale a una PR publicada.
- [Generación y evaluación de 10 millones de filas](../data/README_10M.md):
  datos sintéticos por chunks, SGD incremental, validación y holdout. El CSV
  grande no está en Git; conserva seed y tamaño de chunk al comparar.
- [Dataset tips local](../data/README_tips.md) y
  [datos del ejercicio 1.1](../data/ariketa_1_1/README.md): procedencia y uso.

Los cuadernos `1_SOLUZIOAK_URLa`/`2_SOLUZIOAK_URLa` descargados de Drive mezclan
ejercicios de PDF y complementarios, e incluyen explicaciones del docente.
Conservan las convenciones de su entorno original (por ejemplo Colab); para
ejecutar localmente usa las guías canónicas anteriores y compara la variante.
No se reescriben esas fuentes descargadas en esta revisión.
