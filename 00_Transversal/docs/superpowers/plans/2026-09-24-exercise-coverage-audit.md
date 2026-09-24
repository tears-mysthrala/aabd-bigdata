# AABD Exercise Coverage Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a source-to-result audit covering all explicit exercises in active, compatibility, and legacy material.

**Architecture:** A Markdown coverage matrix will be the source of truth for exercise IDs, original prompt paths, existing or new solutions, archive equivalence, and evidence. Subject-specific plans create the solution artifacts; this plan owns the complete inventory, cross-links, and verification that every task-like source appears once.

**Tech Stack:** Markdown, `rg`, `git`, Python standard library for inventory and path validation.

**Spec:** [2026-09-24-ejercicios-aabd-design.md](../specs/2026-09-24-ejercicios-aabd-design.md)

## Global Constraints

- Cover `01_Erronka1_CNC_Guard/` through `07_Kafka/`, explicit transversal tasks, compatibility symlinks, and `_archivo_legacy/`.
- Treat compatibility symlinks as references to their targets, not additional copies.
- Do not alter class source materials or existing user changes.
- Put current solutions under the appropriate `soluzioak/`; put unique legacy solutions under `_archivo_legacy/soluzioak/`.
- Keep exercise artifacts primarily in Euskara and preserve each module's established formats.
- Do not include secrets, private data, credentials, or team member identities.
- Mark answers as examples when a prompt requires personal judgment; leave identity and signature fields blank.
- Use current official sources for legal claims and label educational assumptions.
- Confine any infrastructure checks to local lab services; do not publish changes.

## Review Focus

- Compatibility paths can duplicate a source: count the target once and link every alias to it.
- Archive files may contain a different prompt revision: compare prompt text and exercise IDs before marking duplicate.
- Existing code can solve an exercise with a different dataset: verify input path, schema, row count, and generated result.
- Infrastructure labs can retain state between runs: identify isolated lab state and avoid deleting existing topics or flows.
- A document may contain discussion prompts without a numbered “exercise”: include explicit activities and deliverables, while excluding examples and theory-only questions.

---

### Task 1: Build the exercise source inventory

**Files:**
- Create: `00_Transversal/AUDITORIA_EJERCICIOS.md`
- Read: `01_Erronka1_CNC_Guard/materialak/`, `02_AA_Ereduak_5071/materialak/`, `03_ML_5072/materialak/`, `04_Programazioa_5073/materialak/`, `05_BigData_Ingeniaritza/materialak/`, `06_NiFi/materialak/`, `07_Kafka/materialak/`, `00_Transversal/`, `_archivo_legacy/`

**Interfaces:**
- Produces: one row per explicit exercise/activity, with columns `ID`, `Fuente`, `Estado inicial`, `Resultado`, `Ruta`, `Verificación`.

- [x] **Step 1: Enumerate candidate prompt files** using `rg --files` and include PDF, DOCX, Markdown, notebooks, and archive paths; omit `.venv`, cache, and binary outputs.
- [x] **Step 2: Extract task markers** from Markdown/Python/notebook sources with `rg` and from PDFs/DOCX using `pdftotext` and `python-docx`; add tasks that are phrased as `Eginkizuna`, `Entregablea`, `Ariketa`, or an explicit practical instruction.
- [x] **Step 3: Compare each task with existing results** in the matching module's `soluzioak/`; use statuses `resuelto`, `parcial`, `pendiente`, `duplicado de otra fuente`, or `requiere datos humanos`.
- [x] **Step 4: Map legacy copies** to their canonical result only after checking prompt identity; list any unique prompt as its own task.
- [x] **Step 5: Self-check inventory completeness** by comparing every task-like file path returned by `rg --files` against a matrix source row.
- [x] **Step 6: Commit the matrix** with only `00_Transversal/AUDITORIA_EJERCICIOS.md` staged.

### Task 2: Verify existing ML and programming exercise coverage

**Files:**
- Read: `03_ML_5072/soluzioak/5072_ML_praktika.py`, `03_ML_5072/materialak/5072_2_01_Erregresio_Lineala.pdf`
- Read: `04_Programazioa_5073/soluzioak/`, `04_Programazioa_5073/materialak/`, `_archivo_legacy/notebooks_root_duplicado/`
- Update: `00_Transversal/AUDITORIA_EJERCICIOS.md`

**Interfaces:**
- Consumes: Task 1 exercise IDs.
- Produces: coverage rows with evidence for ML regression and programming notebooks, including the current Ariketa 2.3 input dataset and the dedicated planned solution path `04_Programazioa_5073/soluzioak/04_Datu_Zientzia_PDF_Ariketak/ariketa_2_3_datu_berria.py`.

- [x] **Step 1: Confirm ML regression coverage** by matching the regression prompt to the existing notebook's model, objective, evaluation, and interpretation sections; record missing requirements if any.
- [x] **Step 2: Compare programming exercise IDs** across source PDFs, canonical `.py`/`.ipynb` solutions, and archive copies; list only distinct prompt revisions as separate rows.
- [x] **Step 3: Trace Ariketa 2.3's current CSV** from `04_Programazioa_5073/data/mock_datuak/Ariketa 2.3/datu_zikinak.csv`, keep the pre-existing different CSV result distinct, and mark the new variant's planned result path as `04_Programazioa_5073/soluzioak/04_Datu_Zientzia_PDF_Ariketak/ariketa_2_3_datu_berria.py` for the programming-results plan.
- [x] **Step 4: Record testable evidence paths** for exercises already covered; do not create duplicate solution files.
- [x] **Step 5: Commit the updated matrix** with only `00_Transversal/AUDITORIA_EJERCICIOS.md` staged.

### Task 3: Verify NiFi exercise coverage

**Files:**
- Read: `06_NiFi/materialak/01_01_ApacheNifi.pdf`, `06_NiFi/materialak/01_02_ApacheNifi_aurreratua.pdf`, both NiFi case-guide PDFs
- Read: `06_NiFi/soluzioak/`
- Update: `00_Transversal/AUDITORIA_EJERCICIOS.md`

**Interfaces:**
- Consumes: Task 1 exercise IDs.
- Produces: seven case rows linked to flow JSON, data fixtures, README, and available lab evidence.

- [x] **Step 1: Map cases 1–7** from prompt to the current flow JSON and the matching case README.
- [x] **Step 2: Validate each flow file as JSON** and record any missing processor/configuration requirement without modifying a flow that already meets the prompt.
- [x] **Step 3: Check existing sample outputs and environment-verifier coverage**; distinguish prior recorded results from a live run in this session.
- [x] **Step 4: Mark each case** `resuelto`, `parcial`, or `pendiente` with its evidence path.
- [x] **Step 5: Commit the updated matrix** with only the matrix file staged.

### Task 4: Close legacy and index references

**Files:**
- Read: `_archivo_legacy/README.md`, `_archivo_legacy/materialak_README.md`, `_archivo_legacy/soluzioak_README_original.md`, `_archivo_legacy/notebooks_root_duplicado/`, `_archivo_legacy/NiFi_duplicado_06_viejo/`
- Modify: `README.md`, `INDICE.md`, module READMEs only when they need a link to a newly created result
- Update: `00_Transversal/AUDITORIA_EJERCICIOS.md`

**Interfaces:**
- Consumes: all module result paths from the three subject-specific plans.
- Produces: no unindexed task and no broken path to a result.

- [x] **Step 1: Compare archive task notebooks with active solutions**; record byte-identical or semantically identical pairs as duplicates.
- [x] **Step 2: Compare archived NiFi task folders** with current cases and list any unique prompt or output.
- [x] **Step 3: Reconcile every matrix route** against the exact actual result paths created by the subject plans; correct any stale planned filename or missing `soluzioak/` route, while preserving an existing user-owned result in `materialak/` without copying it.
- [x] **Step 4: Add one cross-reference** from the root `INDICE.md` to the audit matrix and add links from module READMEs only where new files need discovery.
- [x] **Step 5: Validate every local Markdown link added by this plan** by resolving its relative path from the file that contains it.
- [x] **Step 6: Re-run the task-source inventory** and confirm each task-like source has exactly one matrix row and each open task maps to a concrete artifact or a clearly stated human/missing-source dependency.
- [x] **Step 7: Commit only the audit, index, and README files changed in this task.**
