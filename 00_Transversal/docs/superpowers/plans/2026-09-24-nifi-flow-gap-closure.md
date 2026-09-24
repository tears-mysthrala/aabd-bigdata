# NiFi Flow Gap Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align the four NiFi flows that differ from the user's revised DF1/DF2 exercises and provide honest local verification evidence.

**Architecture:** Patch the existing canonical flow JSON and case README in place, preserving the flow IDs where possible and adding only required processors, ports, services, and configuration. Validate structure offline and distinguish static validation from an actual NiFi run; never embed credentials or contact external endpoints.

**Tech Stack:** Apache NiFi flow JSON, Docker Compose version pinned by this repository, Python standard-library JSON validation, Markdown.

**Spec:** [2026-09-24-ejercicios-aabd-design.md](../specs/2026-09-24-ejercicios-aabd-design.md)

## Global Constraints

- Preserve the revised exercise PDFs, existing sample data, secrets, and unrelated flows.
- Modify only the four task-listed flows and their case README files plus the audit matrix.
- Do not start, stop, reimport, or reconfigure NiFi or dependent databases as part of this plan; validate JSON and relationships statically.
- Do not call AEMET, AWS/S3, MongoDB, MariaDB, or any remote endpoint. Use placeholder/environment-provided references with no real credentials or bucket data.
- Do not claim a live run or service-side output. Label generated/retained fixture files as static or simulated evidence.
- Keep names and comments consistent with existing module conventions and the revised task PDF.

## Review Focus

- DF1.3 specifically requires a 5-second GenerateFlowFile schedule, ReplaceText append with `${now()}`, ExtractText attribute `datuak`, LogAttribute, and AttributesToJSON → PutMongo.
- DF2.1 requires the four named processors encapsulated inside a process group with `sarrera` InputPort and `irteera` OutputPort and the CSVReader/JsonRecordSetWriter services.
- DF2.2 requires `customers`, `orders`, and `order_items` data through both SplitText + PutMongo classic and PutMongoRecord variants, plus comparison documentation.
- DF2.3 requires Bronze/Silver/Gold dual storage with S3 objects and Parquet Gold output plus Mongo collections, with an AWS credentials provider service that contains no credential value.
- DF2.3's current `api.el-tiempo.net` endpoint does not satisfy the revised prompt's AEMET API requirement; select the current official AEMET endpoint without invoking it.
- NiFi flow JSON must remain parseable and processor/port/service references must resolve within the JSON graph.

---

### Task 1: Align DF1.3 and DF2.1 flows with the revised exercises

**Files:**
- Modify: `06_NiFi/soluzioak/03_Atributuak_eta_Linajea/flow_03_atributuak_linajea_aldaera2_mongodb.json`
- Modify: `06_NiFi/soluzioak/03_Atributuak_eta_Linajea/README.md`
- Modify: `06_NiFi/soluzioak/05_CSV_JSON_ConvertRecord_DF2.1/flow_05_csv_json_df2.1.json`
- Modify: `06_NiFi/soluzioak/05_CSV_JSON_ConvertRecord_DF2.1/README.md`
- Update: `00_Transversal/AUDITORIA_EJERCICIOS.md`
- Read: `06_NiFi/materialak/01_01_ApacheNifi.pdf`
- Read: `06_NiFi/materialak/01_02_ApacheNifi_aurreratua.pdf`

**Interfaces:**
- DF1.3 flow must expose all required processors and configured property values, including the correct 5-second interval and attribute name.
- DF2.1 process group must expose named boundary ports and retain processor/service references.

- [ ] **Step 1: Compare current flow JSON to the exact two source prompts** and record existing component IDs before edits.
- [ ] **Step 2: Correct the DF1.3 flow** to the required schedule, append expression, `datuak` extraction, logging, JSON conversion, and Mongo sink; preserve unrelated provenance components.
- [ ] **Step 3: Add or correct DF2.1 process-group boundary ports** named `sarrera` and `irteera`, keep the four required processors inside, and connect flow paths through the ports.
- [ ] **Step 4: Update each case README** with exact topology, required controller services, and an explicit static-validation/no-live-run evidence statement.
- [ ] **Step 5: Parse both JSON files and assert required processors, properties, ports, and references; link the canonical flows from the matching audit rows and commit only listed files.**

### Task 2: Complete DF2.2 coverage for all three database tables

**Files:**
- Modify: `06_NiFi/soluzioak/06_MariaDB_MongoDB_Laborategia_DF2.2/flow_06_mariadb_mongodb_classic.json`
- Modify: `06_NiFi/soluzioak/06_MariaDB_MongoDB_Laborategia_DF2.2/flow_06_mariadb_mongodb_record.json`
- Modify: `06_NiFi/soluzioak/06_MariaDB_MongoDB_Laborategia_DF2.2/README.md`
- Update: `00_Transversal/AUDITORIA_EJERCICIOS.md`
- Read: `06_NiFi/materialak/01_02_ApacheNifi_aurreratua.pdf`

**Interfaces:**
- Each variant processes all three requested tables (`customers`, `orders`, `order_items`) into its exact variant collection: `6kasua-classic` or `6kasua-record`.
- The README compares classic line-splitting plus PutMongo against PutMongoRecord's record API using stated trade-offs, without inventing benchmark timings.

- [ ] **Step 1: Inventory existing SQL/proc configs and connection graph** for both flow variants.
- [ ] **Step 2: Add missing ExecuteSQLRecord branches for all three tables** to both variants, retaining the two source-required collection names (`6kasua-classic`, `6kasua-record`) and adding a source-table discriminator to records so the merged collections remain interpretable.
- [ ] **Step 3: Document the two variants and their throughput/complexity trade-offs qualitatively**; do not claim a live database insert or fabricate a benchmark.
- [ ] **Step 4: Validate JSON syntax, connection endpoints, processor/service IDs, table queries, and expected collection names; update the matrix with static evidence.**
- [ ] **Step 5: Commit only the two flows, case README, and matrix.**

### Task 3: Align DF2.3 with S3 and Parquet requirements

**Files:**
- Modify: `06_NiFi/soluzioak/07_AEMET_Datu_Lakua_Medallion_DF2.3/flow_07_aemet_datalake_medallion.json`
- Modify: `06_NiFi/soluzioak/07_AEMET_Datu_Lakua_Medallion_DF2.3/README.md`
- Update: `00_Transversal/AUDITORIA_EJERCICIOS.md`
- Read: `06_NiFi/materialak/01_02_ApacheNifi_aurreratua.pdf`

**Interfaces:**
- Bronze and Silver write their required S3 objects; Gold writes Parquet to S3 and records Bronze/Silver/Gold data through the specified Mongo collections.
- AWS credentials provider is a reference to runtime configuration and contains no secret material.

- [ ] **Step 1: Verify available processor bundle and NiFi version against repository-pinned container metadata and official NiFi documentation**; choose property names supported by that version.
- [ ] **Step 2: Replace the mismatched endpoint with the documented official AEMET API URL without calling it, and replace local-JSON/local-PutFile parts** with the required S3 paths and Parquet record services while preserving both Gold sinks and Medallion flow ordering.
- [ ] **Step 3: Add an external credentials-provider placeholder only**; document required runtime configuration without populating account, key, bucket, or endpoint secrets.
- [ ] **Step 4: Update README with the flow layout, static checks, required operator-supplied services, and the fact that no AEMET/AWS/Mongo request was executed.**
- [ ] **Step 5: Validate JSON syntax and internal links, ensure no secret values, and assert required S3/Parquet/Mongo processors/services; update audit status/evidence and commit only listed files.**
