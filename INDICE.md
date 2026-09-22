# BigData AABD — Índice estable por asignatura (2026-09-22)

Estructura canónica: cada carpeta `0X_*` contiene `materialak/ + soluzioak/ + data/` juntos.
Compat legacy: `materialak/`, `soluzioak/`, `notebooks_compat`, `SBOM_compat`, `notebooklm_compat`, `katalogoa.*` son symlinks, no duplican.

## Mapa

- `00_Transversal/`: `SECURITY.md`, `SBOM/`, `notebooklm/` (6 artefactos OK), `materialak_00_Orokorra/`
- `01_Erronka1_CNC_Guard/`: `materialak/` (ANEXO1/4, tortilla PERT), `proyecto_cnc_guard/` (uv + tests), `soluzioak/Ebazpena_CNC_Guard_eta_AA_Ereduak.md` ✅
- `02_AA_Ereduak_5071/`: `materialak/` (E1 pdfs + 5071 fuzzy) ✅, `soluzioak/` → ver `01/.../Ebazpena` (stub)
- `03_ML_5072/`: `materialak/` (5072 pdfs) ✅, `soluzioak/` ⏳ PENDIENTE
- `04_Programazioa_5073/`: `materialak/` (pdfs + notebooks canónicos 12 ficheros) ✅, `soluzioak/` (4 carpetas, asserts ✅), `data/` (katalogoa, git_ariketa_4_2, ariketa_1_1, mock_datuak) ✅
- `05_BigData_Ingeniaritza/`: `materialak/` + `soluzioak/` (7V Spotify, ETL/ELT, Smart Factory) ✅
- `06_NiFi/`: `materialak/` (guías 1-7 + salmentak.csv + docker) ✅, `soluzioak/` (7 casos, 13 flows JSON OK) ✅
- `07_Kafka/`: `materialak/01_03_ApacheKafka.pdf` ✅, `soluzioak/` ⏳ PENDIENTE
- `_archivo_legacy/`: `notebooks_root_duplicado/`, `NiFi_duplicado_06_viejo/`, READMEs originales, `deskargatu_berriak/`

## Estado (2026-09-22, dena eginda ✅)

1. ✅ Fix `01/proyecto_cnc_guard`: `.venv` birsortua (shebang zaharra `erronka1/…`), `uv run pytest` 3/3.
2. ✅ `03_ML_5072/soluzioak/`: `5072_ML_praktika.py/.ipynb` (NaN errealak, Ridge/Lasso, balanced).
3. ✅ `07_Kafka/soluzioak/`: compose KRaft + producer/consumer (+mock) + DF3.1/2/3, mock test 1/1.
4. ✅ `06_NiFi` DF2.3 ebidentziak (`simulatu_aemet_medallion.py`: 10/10/3) + `SBOM/releases/0.1.0` (3199).
5. ✅ `04/git_ariketa_4_2`: `feat/arg-izena` + merge `--no-ff` (PR #1) + 4 test, 6 commit.

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
