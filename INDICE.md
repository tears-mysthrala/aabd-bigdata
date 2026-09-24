# BigData AABD — Índice estable por asignatura (2026-09-22)

Estructura canónica: cada carpeta `0X_*` contiene `materialak/ + soluzioak/ + data/` juntos.
Compat legacy: `materialak/`, `soluzioak/`, `notebooks_compat`, `SBOM_compat`, `notebooklm_compat`, `katalogoa.*` son symlinks, no duplican.

## Mapa

### Orientación rápida

Este es un repositorio docente de IA y Big Data: combina teoría de clase, ejercicios resueltos, notebooks y laboratorios reproducibles. El material está principalmente en euskera y algunos resúmenes operativos en castellano. Los ejemplos de CNC usan datos sintéticos; los servicios Docker son para laboratorio local, no para producción.

| Para encontrar... | Empieza por... |
|---|---|
| La estructura y el arranque general | [README.md](README.md) |
| Dónde añadir materiales o soluciones | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Límites y prácticas seguras del repositorio | [SECURITY.md](SECURITY.md) y [00_Transversal/SECURITY.md](00_Transversal/SECURITY.md) |
| CNC Guard, instalación y validación | [README de CNC Guard](01_Erronka1_CNC_Guard/proyecto_cnc_guard/README.md) |
| Soluciones de Big Data e ingeniería de datos | `05_BigData_Ingeniaritza/soluzioak/` |
| Laboratorios NiFi por caso | Los `README.md` dentro de `06_NiFi/soluzioak/`; el README general de esa carpeta conserva rutas de una estructura anterior |
| Kafka y sus pruebas sin broker | [README de Kafka](07_Kafka/soluzioak/README.md) |
| Infraestructura Docker compartida | [infra/README.md](infra/README.md) |

- `00_Transversal/`: `SECURITY.md`, `SBOM/`, `notebooklm/` (6 artefactos OK), `materialak_00_Orokorra/`
- `01_Erronka1_CNC_Guard/`: `materialak/` (ANEXO1/4 docx+md, tortilla PERT), `proyecto_cnc_guard/` (uv + tests), `soluzioak/Ebazpena_CNC_Guard_eta_AA_Ereduak.md` ✅
- `02_AA_Ereduak_5071/`: `materialak/` (E1 pdfs + 5071 fuzzy + Etika/Legea + Marko legala + Alborapenak/COMPAS con dataset local) ✅, `soluzioak/` → ver `01/.../Ebazpena` (stub)
- `03_ML_5072/`: `materialak/` (5072 pdfs + 02_1 Erregresio Lineala + 02_2 Erregresio Logistikoa ppt) ✅, `soluzioak/` (Orange workflows, regresión lineal/logística y prácticas) ✅
- `04_Programazioa_5073/`: `materialak/` (pdfs + notebooks canónicos 12 ficheros) ✅, `soluzioak/` (4 carpetas, asserts ✅, ariketa 3.1 ejecutado con datos oficiales), `data/` (katalogoa, git_ariketa_4_2, ariketa_1_1, mock_datuak: Ariketa 2.2, Ariketa 2.3 datu_zikinak, Ariketa 3.1 ikasleak_notak_100.csv) ✅
- `05_BigData_Ingeniaritza/`: `materialak/` (actualizados 01_02 y ariketak v2 con Faker/Parquet/formatos) + `soluzioak/` (7V Spotify, ETL/ELT, Smart Factory) ✅
- `06_NiFi/`: `materialak/` (guías 1-7 actualizadas + salmentak.csv + docker) ✅, `soluzioak/` (7 casos, 11 archivos `flow_*.json`) ✅
- `07_Kafka/`: `materialak/01_03_ApacheKafka.pdf` (actualizado v2 con Producer Python) ✅, `soluzioak/` ✅
- `_archivo_legacy/`: `notebooks_root_duplicado/`, `NiFi_duplicado_06_viejo/`, READMEs originales, `deskargatu_berriak/`

## Estado (2026-09-22, stacks reales levantados ✅)

1. ✅ Fix `01/proyecto_cnc_guard`: `.venv` birsortua, `uv run pytest` 3/3, `pip-audit` limpio.
2. ✅ `03_ML_5072/soluzioak/`: `5072_ML_praktika.py/.ipynb` (NaN errealak, Ridge/Lasso, balanced).
3. ✅ `07_Kafka/soluzioak/`: compose KRaft (127.0.0.1) + producer/consumer (+mock, `--csv`, `--keys`, `--skip`) + DF3.1/2/3.
   **Real**: 100k → 100k ✅. **Throughput**: 1M en 21 s produce (~48k/s, 3 en paralelo) y
   59 s consume (~17k/s) → 10M ≈ 3.5/10 min (extrapolado; 10M enteros no movidos).
4. ✅ `06_NiFi` DF2.2 stack (MySQL 12435 customers, Mongo, NiFi, nginx): `test_environment.sh` 8/8,
   11 fluxu inportatuak API-tik, DF2.3 ebidentziak (10/10/3) + `SBOM/releases/0.1.0` (3199).
5. ✅ `04/git_ariketa_4_2`: `feat/arg-izena` + merge `--no-ff` (PR #1) + 4 test, bundle preservado.
6. ✅ `04/data/cnc_10M.csv`: 10M filas seeded (350 MB, gitignoreado) + `test_estabilidad_10M.py`
   (chunks 1M, SGD incremental, holdout): acc=0.9861 F1=0.2036.

Auth: `.env` (fuerte, gitignoreado) + `.env.example` (defaults docentes, solo-lab).

## Erronka 1 completa 2026-09-22 ✅ (prototipo → resolución)

- `proyecto_cnc_guard/src/cnc_guard/fuzzy.py`: Mamdani numpy (12 reglas, zentroidea), 9 tests.
- `proyecto_cnc_guard/src/cnc_guard/anomaly.py`: IsolationForest + `riesgo_final=max`, 9 tests.
- `proyecto_cnc_guard/CNC_Guard.ipynb` (+`.py`, 11 celdas, ejecutado sin errores, determinista):
  EDA 200k → fuzzy crisp (13.3/50.0/94.4) → IF 500k → consenso en holdout 200k.
- Métricas: `ta=0.7 tf=0.5 acc=0.9863 F1=0.1762`. Total tests proyecto: 18/18 + Ruff.
- Límite honesto: datos sintéticos (85% ruido) → F1 techo de los datos; sin OPC-UA/MQTT reales.

## Infra split 2026-09-22 ✅

- `infra/`: nginx frontal + Kafka KRaft compartidos (red externa `iabd-infra-net`).
  Kafka **no** va tras nginx (binario TCP ≠ HTTP; endurecer = SASL/TLS).
- DF2.2 adelgazado (sin nginx/certs, red externa). Healthcheck NiFi robusto a 2 IPs.
- 07 solo-código (scripts leen `TOPIC/GROUP/BOOTSTRAP` del entorno).
- Hallazgo: `flow.json.gz` vive en el contenedor → al recrear, reimportar
  (`inportatu_fluxuak.py`, 7 grupos). Re-verificado: env 8/8, proxy nginx→NiFi 200,
  Kafka infra 5000/5000, NiFi healthy.

Eskuz (interbentzioa behar): Kafka/NiFi/Mongo docker stack-ak altxatu (`docker compose up -d`)
eta fluxuak NiFi UI-n inportatu (`06_NiFi/soluzioak/scripts/`).

## Auditoría seguridad 2026-09-22 ✅ (SECURITY.md + estándar actual)

- **pip-audit** (`proyecto_cnc_guard`, grupo `security`): *No known vulnerabilities* ✅.
- **Secretos**: DF2.2 `.env` (600, aleatorio 32c, gitignoreado) + compose `${VAR:?}` sin hardcode ✅;
  `pass-import.sh` sin ecos ✅; NiFi API scripts con JWT login ✅;
  **fix**: eliminados defaults `nifinifinifi`/`iabd` en `scripts/` (fail-fast) y Kafka a `127.0.0.1:9092`.
- **Red**: MySQL/Mongo/NiFi en `127.0.0.1`; nginx HTTP→HTTPS + TLS; `0.0.0.0` solo intra-contenedor ✅.
- **Git**: `proyecto_cnc_guard` limpio (sin `.env`/venv/pkl, con CI+Security+Dependabot) ✅.
- **Pickle/joblib**: solo procedencia propia (`datuak.pkl` generado en ejercicio, `verify_setup` roundtrip) ✅.
- **SBOM**: base + `releases/0.1.0` (3199 comp.) ✅.

⚠️ Excepciones conocidas (lab-only, no reutilizar fuera sin endurecer):
- `04/materialak/notebooks/5073_1_Lengoaiak.ipynb` celdas 13/35 con `!pip install` (material didáctico que enseña pip; viola la regla de celdas — usar solo en venv desechable).
- `admin:admin123` en `06/.../01_Kasu_Praktikoak...md:126` y compose de `materialak/06-ariketa...` (material docente; el lab DF2.2 usa `.env` propio).
- Mongo DF2.2 y Kafka sin auth (solo `127.0.0.1` + red docker) — activar auth/SASL si sale del lab.
- Discrepancia por verificar al levantar el stack: `Ebazpena_Kasu_6.md` indica URI con `admin:admin123` pero el compose DF2.2 no configura auth en Mongo.
- Jupyter: sin servidor en marcha; al arrancar, solo `127.0.0.1` + token (SECURITY.md).

## Regla futura

Nuevo material → va a su `0X/materialak/`. Nueva solución → a su `0X/soluzioak/`. Nada en raíz salvo este índice. No revivir `data/`, `git/`, `erronka1/` sueltos.

## Auditoría de ejercicios

[Matriz de cobertura de ejercicios](00_Transversal/AUDITORIA_EJERCICIOS.md): enunciados, resultados, verificación, duplicados de archivo y dependencias pendientes.
