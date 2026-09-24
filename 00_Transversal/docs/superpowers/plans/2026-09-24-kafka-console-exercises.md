# Kafka Console Exercises Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Provide complete, reproducible model results for the five hands-on Kafka console exercises added to the current lab PDF.

**Architecture:** Add one Euskara solution guide in the Kafka module with isolated topic names, executable console commands, expected observations, and answer tables. Separate deterministic facts from broker-dependent observations, and record verification without deleting or resetting existing Kafka state.

**Tech Stack:** Markdown, Docker Compose, Apache Kafka console scripts.

**Spec:** [2026-09-24-ejercicios-aabd-design.md](../specs/2026-09-24-ejercicios-aabd-design.md)

## Global Constraints

- Preserve the lab PDF and all existing Kafka topics, containers, and volumes.
- Use a clearly prefixed isolated topic namespace for live verification; do not reuse or delete the requested topic names if they already exist with unknown state.
- Do not stop, recreate, or reconfigure any running infrastructure. If the local broker is unavailable, provide commands and explain that live output was not captured.
- Distinguish Kafka guarantees from outputs that depend on broker version, producer partitioning, and prior consumer-group offsets.
- Keep commands consistent with the repository's local Docker Compose setup and avoid publishing results.

## Review Focus

- Exercise 2 asks whether records produced while the consumer is offline remain available; explain retention and the `--from-beginning` behavior.
- Exercise 3 starts a second consumer from the beginning; show that a fresh consumer/group can read retained records again.
- Exercise 4's partition assignment and per-partition offsets depend on producer behavior; capture the actual mapping or clearly label a sample mapping.
- Exercise 5 permits increasing partitions but Kafka does not support reducing a topic's partition count in place; capture and explain the command failure.
- Never infer successful live verification from example output alone.

---

### Task 1: Write the five console exercise solutions

**Files:**
- Create: `07_Kafka/soluzioak/ariketa_kontsola_topic_partizio_offset.md`
- Read: `07_Kafka/materialak/01_03_ApacheKafka.pdf`
- Read: `07_Kafka/soluzioak/README.md`
- Update: `07_Kafka/soluzioak/README.md`
- Update: `00_Transversal/AUDITORIA_EJERCICIOS.md`

**Interfaces:**
- Produces: one section per source exercise, including commands, expected observation, answer, and verification status.
- Topic prefix for live verification: `codex-aabd-20260924-` followed by exercise-purpose suffixes.

- [ ] **Step 1: Extract and map the exact requirements** for exercises 1–5: create/describe topics, sensor message sequence and three offline messages, five purchases, partition/offset display, partition increase, and attempted decrease.
- [ ] **Step 2: Add isolated commands** for topic creation and inspection, clearly separating the requested lab names from prefixed live-verification topics; explain cleanup only as an optional manual action after review.
- [ ] **Step 3: Document exercise 1** with required 2- and 4-partition counts and a table identifying partition IDs from `--describe`.
- [ ] **Step 4: Document exercises 2–3** with producer/consumer command order and answers on retained records, `--from-beginning`, and reading the same retained messages again.
- [ ] **Step 5: Document exercise 4** with the `print.partition` and `print.offset` properties, a five-row result table, and concise answers explaining that offsets are local to partitions and message identity requires topic, partition, and offset.
- [ ] **Step 6: Document exercise 5** with `--alter --partitions 4`, verification by `--describe`, and a safe attempted decrease command plus expected rejection; do not present a fabricated error transcript as live evidence.
- [ ] **Step 7: Verify commands against the repository's Kafka version and Compose service names**; if a local broker is available, use only prefixed topics and capture outputs without stopping or resetting any service.
- [ ] **Step 8: Link the solution from the module README and audit matrix**, with verification status (`live local run` or `commands reviewed only`) explicit.
- [ ] **Step 9: Check all source requirements are answered and commit only the solution, README, and matrix files.**
