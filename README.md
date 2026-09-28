# AABD · Big Data Aplicado — Ejercicios resueltos y laboratorios

Repositorio de estudio del ciclo **IA y Big Data**: apuntes, ejercicios resueltos
y laboratorios Docker de todo el curso, organizados **por asignatura con sus
soluciones dentro**. En euskera (material de clase) con resúmenes en español.

Consulta la [auditoría de ejercicios](00_Transversal/AUDITORIA_EJERCICIOS.md)
para localizar enunciados, soluciones y comprobaciones, incluidos los materiales
de archivo y las tareas que aún dependen de evidencia humana o de laboratorio.

> ⚠️ Material de estudio, no software de producción. MongoDB/Kafka van sin
> autenticación y atados a `127.0.0.1`: apto para laboratorio, no para exponer.
> Lee [SECURITY.md](SECURITY.md).

## Estructura

| Carpeta | Contenido | Estado |
|---|---|---|
| `00_Transversal/` | `SECURITY.md` del lab, `SBOM/`, `notebooklm/`, programaciones | ✅ |
| `01_Erronka1_CNC_Guard/` | Reto 1: `materialak/`, `proyecto_cnc_guard/` (uv + tests), `soluzioak/` | ✅ |
| `02_AA_Ereduak_5071/` | Paradigmas IA + Lógica difusa | ✅ |
| `03_ML_5072/` | ML: EDA, preprocesado, regresión, clasificación | ✅ |
| `04_Programazioa_5073/` | Python, `materialak/` + `soluzioak/` (6 bloques), `data/`, ejercicio Git 4.4 | Material mixto |
| `05_BigData_Ingeniaritza/` | 7V, ciclo de vida, ETL/ELT, Lakehouse | ✅ |
| `06_NiFi/` | 7 casos NiFi (11 flujos), labs MariaDB→MongoDB y AEMET Medallion | Flujos sujetos a validación real |
| `07_Kafka/` | Pub/sub, consumer groups, lab Python y broker compartido en `infra/` | Prácticas en broker aislado |
| `horario/` | Calendarios y horarios del curso | ✅ |
| `infra/` | nginx frontal + Kafka compartidos (red `iabd-infra-net`) | ✅ |
| `_archivo_legacy/` | Duplicados antiguos (no usar) | 🗄️ |
| `INDICE.md` | Mapa detallado + auditoría de seguridad 2026-09-22 | 📖 |

Compatibilidad: `materialak/`, `soluzioak/`, `notebooks_compat/`, `SBOM_compat/`,
`notebooklm_compat/` y `katalogoa.*` son **symlinks** a las rutas canónicas.

Los estados de esta tabla orientan sobre el contenido disponible; no certifican
que todos los ejercicios se hayan ejecutado. Consulta la
[auditoría de ejercicios](00_Transversal/AUDITORIA_EJERCICIOS.md) para distinguir
soluciones existentes, comprobaciones y evidencias pendientes.

## Qué se estudia en cada módulo

| Módulo | Conceptos y prácticas |
|---|---|
| [00 · Transversal](00_Transversal/) | Programaciones y recursos comunes, seguridad del laboratorio, inventario de componentes (SBOM), herramientas de estudio y seguimiento de ejercicios. |
| [01 · CNC Guard](01_Erronka1_CNC_Guard/) | Reto integrador de detección de anomalías en máquinas CNC: datos sintéticos, reglas difusas Mamdani, Isolation Forest y evaluación de alertas. Los resultados con datos sintéticos no demuestran eficacia industrial. |
| [02 · AA Ereduak 5071](02_AA_Ereduak_5071/) | Modelos y paradigmas de IA, lógica difusa, sesgos, ética y marco legal, incluida la clasificación de riesgos del AI Act. |
| [03 · ML 5072](03_ML_5072/) | Exploración y preparación de datos, regresión lineal y logística, clasificación, regularización y evaluación de modelos con Python y Orange. |
| [04 · Programazioa 5073](04_Programazioa_5073/) | Fundamentos de Python, funciones y estructuras de datos; NumPy, Pandas y gráficos; formatos de archivo, Git, DVC y ejercicios de frameworks y herramientas de IA. Las soluciones se agrupan en seis bloques. |
| [05 · Big Data Ingeniaritza](05_BigData_Ingeniaritza/) | Características y ciclo de vida de Big Data, generación de datos, CSV/JSON/Parquet, ETL/ELT y organización de Data Lake/Lakehouse con capas Bronze, Silver y Gold. |
| [06 · NiFi](06_NiFi/) | Flujos de ingestión y transformación: contenido y atributos, Record API, filtrado y conversión, HTTP, MariaDB → MongoDB y datos de AEMET. Importar un JSON no basta para validar un flujo. |
| [07 · Kafka](07_Kafka/) | Topics, particiones, claves, offsets y grupos de consumidores; productores y consumidores Python y prácticas de streaming con un broker de laboratorio. |
| [Infraestructura](infra/) | Servicios Docker compartidos y su configuración: red del laboratorio, nginx y Kafka. La guía de cada práctica indica qué servicios necesita. |

## Cómo moverse por el repositorio

Empieza por el [índice detallado](INDICE.md) para localizar un tema y por la
[auditoría de ejercicios](00_Transversal/AUDITORIA_EJERCICIOS.md) para relacionar
su enunciado con la solución y las comprobaciones disponibles.

Dentro de los módulos, cuando existen estas carpetas:

- **`materialak/`**: material de clase, teoría y enunciados; puede incluir ejemplos originales.
- **`soluzioak/`**: soluciones, scripts, notebooks y guías de prácticas.
- **`data/`**: datos o instrucciones para obtenerlos y generarlos. Algunos ejercicios guardan sus datos junto a la solución.
- **`README.md`**: instrucciones específicas de una práctica, dependencias y límites de validación.

Ejemplo desde la raíz del repositorio, después de clonarlo:

```bash
# Ver el material de programación
cd 04_Programazioa_5073
ls materialak
ls soluzioak

# Volver a la raíz y consultar las prácticas de Kafka
cd ..
cd 07_Kafka/soluzioak
cat README.md

# Volver a la raíz
cd ../..
```

Usa las carpetas de asignatura como rutas principales. Los enlaces de
compatibilidad de la raíz apuntan al mismo contenido. `_archivo_legacy/`
conserva copias históricas: consulta primero la versión canónica del módulo.
Los notebooks `.ipynb` se abren con Jupyter o un editor compatible; los scripts
`.py` se ejecutan siguiendo la guía de su ejercicio.

## Puesta en marcha

Para descargar y leer el material basta con Git. Desde el directorio donde
quieras guardar el repositorio:

```bash
git clone https://github.com/tears-mysthrala/aabd-bigdata.git
cd aabd-bigdata
```

Para ejecutar una práctica, consulta primero su README. Los siguientes comandos
parten de la raíz del repositorio y requieren las herramientas indicadas abajo:

```bash
# 1. Preparar el entorno del proyecto CNC Guard
(cd 01_Erronka1_CNC_Guard/proyecto_cnc_guard && uv sync)

# 2. Práctica ML 5072
01_Erronka1_CNC_Guard/proyecto_cnc_guard/.venv/bin/python \
  03_ML_5072/soluzioak/5072_ML_praktika.py

# 3. Kafka: seguir la guía del módulo y usar un broker de laboratorio aislado
#    07_Kafka/soluzioak/README.md

# 4. Lab NiFi + MariaDB + MongoDB (con infra ya arriba)
#    06_NiFi/soluzioak/06_MariaDB_MongoDB_Laborategia_DF2.2/README.md
#    Revisar .env.example y configurar secretos locales antes de desplegar.
```

El proyecto CNC Guard usa Python 3.13 y [`uv`](https://docs.astral.sh/uv/).
Los laboratorios de servicios requieren Docker y Compose; las dependencias
adicionales se indican en sus guías. No necesitas levantar todos los servicios
para estudiar o ejecutar un ejercicio de Python. No uses `chmod 666` sobre el
socket de Docker. Si ejecutas Jupyter, limítalo a `127.0.0.1` con token.

## NotebookLM

Cuaderno sincronizado con fuentes y artefactos de estudio
(`00_Transversal/notebooklm/`): guía, flashcards, quiz, mapa mental, podcast y vídeo.
Tras `notebooklm login`, las novedades se suben con
`00_Transversal/notebooklm/SUBIR_NOVEDADES.sh`.

## Contribuir y seguridad

- Para añadir soluciones: [CONTRIBUTING.md](CONTRIBUTING.md).
- Para avisar de vulnerabilidades o secretos filtrados: [SECURITY.md](SECURITY.md).
- GitHub Actions valida las PR; no hay CI ni despliegues en cada push.
