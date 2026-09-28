# AABD Programming and Data Results Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the missing executable results for the current Ariketa 2.3 dataset and all newly added Data Engineering assignments.

**Architecture:** Add focused solutions beside the existing course solutions. Keep the supplied dirty CSV unchanged; read it with its real semicolon delimiter, write a cleaned result and summary, and provide a separate Faker generator for the 100/10,000 customer examples plus JSON conversion.

**Tech Stack:** Python 3.13, `uv`, pandas, Faker, CSV/JSON, Jupyter notebooks.

**Spec:** [2026-09-24-ejercicios-aabd-design.md](../specs/2026-09-24-ejercicios-aabd-design.md)

## Global Constraints

- Leave source exercise documents and supplied datasets unchanged.
- Put solutions in the module's `soluzioak/`; keep `.py` and `.ipynb` synchronized for new coding exercises.
- Use isolated `uv` environments and locked dependencies; never install packages globally.
- Preserve the supplied schema and document any inference, especially European numeric formatting and missing values.
- Use deterministic Faker output only when a seed is supplied; mark all generated customer records synthetic.
- Do not fabricate teacher-provided CSV inputs or external DVC remote evidence; record those limits while verifying all code that can be checked locally.
- Do not include secrets or real personal/customer records.

## Review Focus

- The new Ariketa 2.3 CSV is semicolon-delimited, unlike the existing comma-separated example.
- `28.000€` represents 28,000 in the supplied Spanish-style data; empty salary must remain missing because no salary-imputation rule is requested.
- Names must be normalized before duplicate removal so `Ane` and `ane` are treated as the same person.
- Missing ages use the mean required by the source; missing cities use `Ezezaguna`.
- Faker determinism requires resetting the same seed before each generation, not reusing a partially consumed generator.

---

### Task 1: Add a result for the current dirty-customer CSV

**Files:**
- Create: `04_Programazioa_5073/soluzioak/04_Datu_Zientzia_PDF_Ariketak/ariketa_2_3_datu_berria.py`
- Create: `04_Programazioa_5073/soluzioak/04_Datu_Zientzia_PDF_Ariketak/ariketa_2_3_datu_berria.ipynb`
- Create: `04_Programazioa_5073/soluzioak/04_Datu_Zientzia_PDF_Ariketak/data/datu_zikinak_garbia.csv`
- Create: `04_Programazioa_5073/soluzioak/04_Datu_Zientzia_PDF_Ariketak/data/datu_zikinak_laburpena.json`
- Update: `04_Programazioa_5073/soluzioak/04_Datu_Zientzia_PDF_Ariketak/README.md`
- Read: `04_Programazioa_5073/data/mock_datuak/Ariketa 2.3/datu_zikinak.csv`
- Read: `04_Programazioa_5073/materialak/5073_2_Datu_Zientzia.pdf`

**Interfaces:**
- `garbitu_datuak(entrada: Path) -> tuple[pandas.DataFrame, dict[str, object]]`
- `main() -> None` writes the cleaned CSV and summary JSON beside the solution.

- [ ] **Step 1: Write input-validation assertions** for required columns `izena`, `adina`, `hiria`, `soldata` and at least one row.
- [ ] **Step 2: Implement delimiter-aware loading and normalization**: read `sep=";"`, trim and title-case names/cities, normalize names for case-insensitive duplicate detection, parse dot-thousands/euro salary strings to numeric, and preserve empty salaries as missing.
- [ ] **Step 3: Apply the exact exercise rules**: report initial missing percentages, drop duplicate names, fill missing ages with the non-missing mean, fill missing cities with `Ezezaguna`, and record before/after row counts.
- [ ] **Step 4: Save clean CSV and summary JSON** with the selected assumptions documented in the notebook markdown.
- [ ] **Step 5: Run the script and verify** output columns, duplicate removal, age bounds/mean filling, city replacement, parsed salary values, and preserved missing salary.
- [ ] **Step 6: Regenerate or synchronize the `.ipynb` from the `.py` cells** and verify both contain the same logic.
- [ ] **Step 7: Link the dataset variant and outputs** from the module README and audit matrix.
- [ ] **Step 8: Commit only the new exercise files and their two links.**

### Task 2: Complete the updated Data Engineering written answers

**Files:**
- Modify: `05_BigData_Ingeniaritza/soluzioak/02_Datuen_Ingeniaritza/Ariketak_01_02_Datuen_Ingeniaritza_Ebazpena.md`
- Read: `05_BigData_Ingeniaritza/materialak/Ariketak_01_02_datuen_ingeniaritza.md`

**Interfaces:**
- Produces: numbered answers for all questions added after the current solution's section 9.

- [ ] **Step 1: Add the six format-choice answers** for spreadsheet sharing, API payload, line-at-a-time logs, large Spark lake, interoperable table, and column-pruned 200 GB analysis.
- [ ] **Step 2: Add the four row/column orientation answers** and explain why full-record lookups and column scans favor different layouts.
- [ ] **Step 3: Add the Faker exercise's short conceptual answers** for scaling row count, seed behavior, unseeded/seeded comparison, and shared classroom seed.
- [ ] **Step 4: Add the CSV-versus-JSON comparison** covering readability, explicit structure, field names, and streaming/large-file memory use.
- [ ] **Step 5: Complete the E/T/L diagram exercise** by mapping the source image's CSV input, cleaning/join/year filter, and Parquet output to Extract, Transform, and Load.
- [ ] **Step 6: Check section numbering and every answer** against the current Markdown and DOCX wording; do not change either source.
- [ ] **Step 7: Commit only the solution Markdown and audit matrix link.**

### Task 3: Generate reproducible Faker datasets and conversion result

**Files:**
- Create: `05_BigData_Ingeniaritza/soluzioak/02_Datuen_Ingeniaritza/generar_bezeroak.py`
- Create: `05_BigData_Ingeniaritza/soluzioak/02_Datuen_Ingeniaritza/generar_bezeroak.ipynb`
- Create: `05_BigData_Ingeniaritza/soluzioak/02_Datuen_Ingeniaritza/README.md`
- Create: `05_BigData_Ingeniaritza/soluzioak/02_Datuen_Ingeniaritza/pyproject.toml`
- Create: `05_BigData_Ingeniaritza/soluzioak/02_Datuen_Ingeniaritza/uv.lock`
- Create: `05_BigData_Ingeniaritza/soluzioak/02_Datuen_Ingeniaritza/data/bezeroak_100.csv`
- Create: `05_BigData_Ingeniaritza/soluzioak/02_Datuen_Ingeniaritza/data/bezeroak_10000.csv`
- Create: `05_BigData_Ingeniaritza/soluzioak/02_Datuen_Ingeniaritza/data/bezeroak.json`
- Create: `05_BigData_Ingeniaritza/soluzioak/02_Datuen_Ingeniaritza/data/salmentak_10000.csv`
- Create: `05_BigData_Ingeniaritza/soluzioak/02_Datuen_Ingeniaritza/data/salmentak_10000.json`

**Interfaces:**
- `generar_bezeroak(kopurua: int, seed: int | None = None) -> list[dict[str, object]]`
- `generar_salmentak(kopurua: int = 10_000, seed: int | None = 42) -> list[dict[str, object]]`
- `gorde_csv(erregistroak: list[dict[str, object]], helmuga: Path) -> None`
- `gorde_json(erregistroak: list[dict[str, object]], helmuga: Path, erro_izena: str) -> None`
- `csv_json_bihurtu(sarrera: Path, helmuga: Path) -> None`
- `main() -> None` writes customer CSVs with 100 and 10,000 rows, the 100-row customer JSON, and 10,000-row sales CSV and JSON.

- [ ] **Step 1: Define the isolated module dependency** in `pyproject.toml` with Python `>=3.13` and Faker; generate `uv.lock` without changing global Python packages.
- [ ] **Step 2: Implement the customer functions** with fields `id`, `izena`, `emaila`, `hiria`, `adina`, locale `es_ES`, and an age range of 18–80.
- [ ] **Step 3: Implement the sales generator** with the exact source columns `id,data,bezeroa,hiria,produktua,kategoria,prezioa,unitateak`, locale `es_ES`, seed 42, price 5–2000, units 1–10, and categories `Ordenagailuak`, `Osagaiak`, `Periferikoak`, `Sareak`.
- [ ] **Step 4: Add validation assertions** for headers, exact/minimum row counts, unique IDs, required fields, customer age range, sales price/unit bounds, category membership, and both sales output formats.
- [ ] **Step 5: Demonstrate customer seed semantics** by generating twice with no seed and twice with seed 42; print the first five rows of each run and assert the seeded runs match.
- [ ] **Step 6: Convert the 100-row customer CSV to the requested `{"bezeroak": [...]}` JSON shape and write 10,000 sales records as `{"salmentak": [...]}` JSON; document JSON array memory limits and avoid representing a 10-million-row file as an in-memory object.
- [ ] **Step 7: Run `uv sync --locked` and the generator**; inspect CSV/JSON schemas and verify deterministic sales output and customer seed behavior.
- [ ] **Step 8: Synchronize and validate the notebook** against the script and link all scripts, generated data, and answer key from the README and audit matrix.
- [ ] **Step 9: Commit only the module code, lock, generated educational datasets, README, and matrix link.**

### Task 4: Complete the distinct PDF revisions not solved by the current notebooks

**Files:**
- Create: `04_Programazioa_5073/soluzioak/03_Lengoaiak_PDF_Ariketak/ariketa_pdf_aldaerak.md`
- Create: `04_Programazioa_5073/soluzioak/04_Datu_Zientzia_PDF_Ariketak/ariketa_pdf_aldaerak.py`
- Create: `04_Programazioa_5073/soluzioak/04_Datu_Zientzia_PDF_Ariketak/ariketa_pdf_aldaerak.ipynb`
- Update: `04_Programazioa_5073/soluzioak/03_Lengoaiak_PDF_Ariketak/README.md`
- Update: `04_Programazioa_5073/soluzioak/04_Datu_Zientzia_PDF_Ariketak/README.md`
- Read: `04_Programazioa_5073/materialak/5073_1_Lengoaiak.pdf`
- Read: `04_Programazioa_5073/materialak/5073_2_Datu_Zientzia.pdf`
- Update: `00_Transversal/AUDITORIA_EJERCICIOS.md`

**Interfaces:**
- `ariketa_1_2_matrizea() -> numpy.ndarray` demonstrates the PDF's seeded 6×4 matrix, reshape/flatten, and impossible 5×5 reshape.
- `ariketa_1_3_prezioak(prezioak: numpy.ndarray) -> tuple[numpy.ndarray, numpy.ndarray]` returns VAT/discounted prices and standardized 5×4 values using stated illustrative input values.
- `ariketa_1_4_stock(stock: numpy.ndarray) -> tuple[numpy.ndarray, numpy.ndarray]` returns exhausted/low-stock masks and the requested replenishment result.
- `ariketa_2_2_csvak(bideak: list[Path]) -> tuple[pandas.DataFrame, dict[str, int]]` loads the three teacher-shaped monthly inputs, concatenates them, and counts rows by month.
- `ariketa_2_5_concat(urtarrila: pandas.DataFrame, otsaila: pandas.DataFrame) -> pandas.DataFrame` demonstrates two monthly sales tables combined by rows.

- [ ] **Step 1: Complete the language-PDF 1.1, 2.4, and 2.5 revisions** with a six-section paper NIF-script outline plus `__main__` explanation, an isolated requirements/CSV handoff walkthrough that clearly marks the real teammate confirmation as unavailable, and a PDF 2.5 model response with two labeled illustrative agent outputs, a locally executed unchanged code sample, linter/verification notes, a 100-word production reflection, and a non-personal-data isolation recommendation.
- [ ] **Step 2: Implement the Data Science PDF 1.2, 1.3, 1.4, 2.2, and 2.5 revisions** in a focused supplementary `.py` file; use deterministic explicit illustrative arrays, document assumptions, and never overwrite the original solution datasets.
- [ ] **Step 3: Generate a synchronized notebook** from the supplementary script with concise explanatory Markdown and reproducible outputs; ensure both files contain the same calculations.
- [ ] **Step 4: For the teacher-supplied 2.2 CSV requirement**, provide small synthetic fixtures matching the requested schema and show the combined output, while explicitly marking the real teacher data as unavailable and the actual classroom result as not verified.
- [ ] **Step 5: Verify every PDF-only requirement** against the exact source pages, execute the supplementary Python, validate matrix shapes, VAT/discount values, stock masks, row counts, and concat results, and inspect the notebook structure without changing source PDFs.
- [ ] **Step 6: Link the supplemental outputs from both solution READMEs and the corresponding PDF rows of the audit matrix; keep each `-NB` row pointed at the existing notebook solution.**
- [ ] **Step 7: Commit only the two supplemental solutions, two README links, any owned small fixtures, and the matrix.**
