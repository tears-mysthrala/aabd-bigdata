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
| `04_Programazioa_5073/` | Python, `materialak/` + `soluzioak/` (5 bloques), `data/`, ejercicio Git 4.4 | Material mixto |
| `05_BigData_Ingeniaritza/` | 7V, ciclo de vida, ETL/ELT, Lakehouse | ✅ |
| `06_NiFi/` | 7 casos NiFi (11 flujos), labs MariaDB→MongoDB y AEMET Medallion | Flujos sujetos a validación real |
| `07_Kafka/` | Pub/sub, consumer groups, lab Python y broker compartido en `infra/` | Prácticas en broker aislado |
| `horario/` | Calendarios y horarios del curso | ✅ |
| `infra/` | nginx frontal + Kafka compartidos (red `iabd-infra-net`) | ✅ |
| `_archivo_legacy/` | Duplicados antiguos (no usar) | 🗄️ |
| `INDICE.md` | Mapa detallado + auditoría de seguridad 2026-09-22 | 📖 |

Compatibilidad: `materialak/`, `soluzioak/`, `notebooks_compat/`, `SBOM_compat/`,
`notebooklm_compat/` y `katalogoa.*` son **symlinks** a las rutas canónicas.

## Puesta en marcha

```bash
# 1. Clonar (pesa ~230 MB por los vídeos y PDFs del curso)
git clone <url> && cd bigdata

# 2. Proyecto CNC Guard (desde la raíz del repositorio)
(cd 01_Erronka1_CNC_Guard/proyecto_cnc_guard && uv sync)

# 3. Práctica ML 5072
01_Erronka1_CNC_Guard/proyecto_cnc_guard/.venv/bin/python \
  03_ML_5072/soluzioak/5072_ML_praktika.py

# 4. Kafka: seguir la guía del módulo y usar un broker de laboratorio aislado
#    07_Kafka/soluzioak/README.md

# 5. Lab NiFi + MariaDB + MongoDB (con infra ya arriba)
#    06_NiFi/soluzioak/06_MariaDB_MongoDB_Laborategia_DF2.2/README.md
#    Revisar .env.example y configurar secretos locales antes de desplegar.
```

Requisitos: Python 3.13 + [`uv`](https://docs.astral.sh/uv/), Docker con grupo
`docker` (nunca `chmod 666` al socket). Jupyter solo en `127.0.0.1` con token.

## NotebookLM

Cuaderno sincronizado con fuentes y artefactos de estudio
(`00_Transversal/notebooklm/`): guía, flashcards, quiz, mapa mental, podcast y vídeo.
Tras `notebooklm login`, las novedades se suben con
`00_Transversal/notebooklm/SUBIR_NOVEDADES.sh`.

## Contribuir y seguridad

- Para añadir soluciones: [CONTRIBUTING.md](CONTRIBUTING.md).
- Para avisar de vulnerabilidades o secretos filtrados: [SECURITY.md](SECURITY.md).
- GitHub Actions valida las PR; no hay CI ni despliegues en cada push.
