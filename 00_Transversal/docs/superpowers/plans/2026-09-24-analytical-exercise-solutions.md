# AABD Analytical Exercise Solutions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the outstanding planning and legal-analysis assignments with reviewable, source-linked model solutions.

**Architecture:** Keep the tortilla scheduling answer under the CNC challenge and keep the GDPR/AI Act answer package under module 5071. The legal package uses one hypothetical education case, official current primary sources, and separate files for the answer key, technical report, user notice, internal protocol, and presentation.

**Tech Stack:** Markdown, Mermaid, official EUR-Lex legislation, official AEPD material, PowerPoint.

**Spec:** [2026-09-24-ejercicios-aabd-design.md](../specs/2026-09-24-ejercicios-aabd-design.md)

## Global Constraints

- Keep source materials intact and create results under their subject's `soluzioak/`.
- Use Euskara for student-facing answers, matching the source materials.
- Mark subjective work as an example; do not invent team names, signatures, or personal choices.
- Verify legal claims against current EUR-Lex and public authorities, including AEPD when used.
- State assumptions and consultation date; make no claim that a real system or company complies.
- Confine output to local files; do not publish or send it externally.
- Address every pending/partial task row in the exercise audit assigned to this plan; maintain blank fields wherever a personal/team deliverable needs real input.

## Review Focus

- PERT task dependencies: potato preparation and oil heating can run in parallel; frying waits for both.
- The 2-minute plating step is assumed to mean final plating after the second side is cooked.
- GDPR legal basis for a public educational institution must follow its actual statutory task and cannot be assumed to be consent.
- AI Act risk depends on the system's intended purpose and role; do not classify by model sophistication alone.
- A legal explanation or human review right must not be broadened beyond the conditions in the current legal text.
- For missing slide-referenced notebooks, answer only the prompt visible in the slides and clearly state that the absent notebook's full rubric could not be checked.

---

### Task 1: Solve the tortilla production schedule

**Files:**
- Create: `01_Erronka1_CNC_Guard/soluzioak/Patata_Tortila_PERT_Gantt_Ebazpena.md`
- Read: `01_Erronka1_CNC_Guard/materialak/patata tortila - planifikazioa eta kostuak lantzekoAA 2026-2027.md`

**Interfaces:**
- Produces: one dependency graph, Mermaid Gantt schedule, calculated critical path, total duration, and an explicit staffing comparison.

- [ ] **Step 1: Define the task graph** using the listed durations: OGB 5, SO 1, ZS 1, PZ 8, PG 15, AI 2, PA 5, TB 5, PT 2 minutes. Record the assumptions that OGB is independent, PG waits for PZ and ZS, PA waits for PG and AI, and final plating follows TB.
- [ ] **Step 2: Calculate the earliest start/finish and float** for every task; show the calculation in a table so the critical path can be independently checked.
- [ ] **Step 3: Write the PERT graph and GitHub-renderable Mermaid Gantt** with task labels and durations from the source.
- [ ] **Step 4: Answer the three source questions**: critical sequence, elapsed time with one cook, and what changes when several cooks can work concurrently.
- [ ] **Step 5: Check the graph and Gantt agree** on prerequisites and total duration; add a link from the audit matrix.
- [ ] **Step 6: Commit only the new solution file and matrix link.**

### Task 2: Verify legal sources and answer the short 5071 activities

**Files:**
- Create: `02_AA_Ereduak_5071/soluzioak/IE6_Marko_Legala/ariketak_eta_jarduerak.md`
- Modify: `02_AA_Ereduak_5071/soluzioak/README.md`
- Read: `02_AA_Ereduak_5071/materialak/5071-IE6-Marko_legala.md`

**Interfaces:**
- Produces: answers for ARIKETA 1.1 and 2.1 and model responses for the five final classroom activities, with numbered source citations.

- [ ] **Step 1: Retrieve primary texts and official guidance** for GDPR 2016/679, AI Act 2024/1689, current application dates, prohibited practices, high-risk Annex III use, human oversight, and AEPD enforcement; store links and access date in the answer file.
- [ ] **Step 2: Add a fillable example for the opening activity** about three AI tools a student has used and what data those tools might process; leave personal experience fields blank and label any filled illustration as fictional.
- [ ] **Step 3: Answer ARIKETA 1.1** by applying all seven GDPR principles to the student-performance scenario; distinguish data necessity, statutory basis, retention, security, accountability, fairness, and the separate AI Act assessment.
- [ ] **Step 4: Answer all eight ARIKETA 2.1 classifications** with intended-purpose assumptions and the exact reason each category applies; call out ambiguity where the prompt does not define context.
- [ ] **Step 5: Evaluate the 911-call system in a mini ethical impact assessment** using the actual factors required in the source; make clear it is a hypothetical classroom model.
- [ ] **Step 6: Answer activities 1–5** with one coherent education-system scenario, including provider questions, an official AEPD case, a credit-decision explanation simulation, HITL/HOTL/HIC choices, and the four EEE question blocks.
- [ ] **Step 7: Verify every legal sentence with a primary citation** and label recommendations separately from binding legal text.
- [ ] **Step 8: Link the solution from `02_AA_Ereduak_5071/soluzioak/README.md` and the audit matrix.**
- [ ] **Step 9: Commit only the legal answer file, the README link, and the matrix.**

### Task 3: Produce the final education-sector model project

**Files:**
- Create: `02_AA_Ereduak_5071/soluzioak/IE6_Marko_Legala/proiektu_integratzailea_txostena.md`
- Create: `02_AA_Ereduak_5071/soluzioak/IE6_Marko_Legala/gardentasun_orria.md`
- Create: `02_AA_Ereduak_5071/soluzioak/IE6_Marko_Legala/protokolo_barnekoa.md`
- Create: `02_AA_Ereduak_5071/soluzioak/IE6_Marko_Legala/aurkezpena.pptx`

**Interfaces:**
- Consumes: the official-source register and answer key from Task 2.
- Produces: a 12–15 page-equivalent technical report, user-facing transparency notice, internal oversight protocol, and a 15-minute presentation.

- [ ] **Step 1: State the fictional system and assumptions**: a school tool predicts academic support needs and proposes student groups; a qualified staff member makes all consequential decisions.
- [ ] **Step 2: Draft the technical report** with GDPR analysis, data map and minimization, rights/explanation, AI Act classification, provider/deployer duties, human oversight, data quality and bias checks, EEE, incident/complaint process, alternatives, limitations, and a go/modify/stop recommendation.
- [ ] **Step 3: Draft the transparency notice** in plain language with purpose, data, logic/role of AI, consequences, retention, contact, rights, and a route to human review.
- [ ] **Step 4: Draft the internal protocol** with named roles as role titles only, pre-use review, monitoring, overrides, logging, complaints, incident response, and periodic reassessment.
- [ ] **Step 5: Build a 10–12 slide presentation** paced for 15 minutes; cite sources in speaker notes or slide footers and include a recommendation and limitations.
- [ ] **Step 6: Cross-check page-equivalent length, required sections, slide pacing, and source consistency** against the assignment rubric.
- [ ] **Step 7: Commit only the four project files, README link, and relevant matrix updates.**

### Task 4: Prepare editable templates for CNC challenge deliverables

**Files:**
- Create: `01_Erronka1_CNC_Guard/soluzioak/Erronka_Entregak_Txantiloia.md`
- Create: `01_Erronka1_CNC_Guard/soluzioak/Ebaluazioa_Txantiloia.md`
- Read: `01_Erronka1_CNC_Guard/materialak/1Erronka_ikaslearen_txostena.docx.pdf`
- Read: `01_Erronka1_CNC_Guard/materialak/ANEXO1-Eus.md`
- Read: `01_Erronka1_CNC_Guard/materialak/ANEXO4.md`
- Create: `01_Erronka1_CNC_Guard/soluzioak/README.md`
- Update: `00_Transversal/AUDITORIA_EJERCICIOS.md`

**Interfaces:**
- Produces: blank editable templates for team contract/roles, personal objectives, preliminary proposal, team planning/checkpoints, final presentation, self-evaluation, and peer evaluation.

- [ ] **Step 1: Extract each formal deliverable and evaluation checkpoint** from the challenge PDF and annexes; do not collapse separate submission items into one template section.
- [ ] **Step 2: Create concise editable templates** with prompts, evidence fields, dates, and role labels only; include the group contract and personal goal sections, and leave team identity, signatures, personal commitments, attendance, and actual peer judgments blank.
- [ ] **Step 3: Clearly label examples vs. fields requiring real student/team input**; do not fabricate submission evidence or assert a consensus.
- [ ] **Step 4: Link both templates from a new CNC solutions README and map the appropriate audit rows to these artifacts.**
- [ ] **Step 5: Verify all deliverables named in the source have a corresponding section and commit only the template, README link, and matrix changes.**

### Task 5: Complete the introductory AI model exercises

**Files:**
- Create: `02_AA_Ereduak_5071/soluzioak/IE1_Sarrera_Ariketak.md`
- Read: `02_AA_Ereduak_5071/materialak/E1-Ereduak-Sarrera.pdf`
- Update: `02_AA_Ereduak_5071/soluzioak/README.md`
- Update: `00_Transversal/AUDITORIA_EJERCICIOS.md`

**Interfaces:**
- Produces: model answers for the Deep Blue/AlphaGo/ChatGPT timeline, one expert-system inference tree, a hand-executable 8–10-rule expert system, and the MYCIN responsibility discussion.

- [ ] **Step 1: Extract the exact four activity prompts and any stated constraints** from the cited pages; answer only what the slides specify.
- [ ] **Step 2: Provide a dated, source-linked AI timeline** and distinguish public milestones from the course's teaching simplification.
- [ ] **Step 3: Build a readable inference tree and an 8–10-rule expert system** with facts, conflict-resolution order, and a worked trace that can be followed by hand.
- [ ] **Step 4: Give balanced model responses to both MYCIN responsibility questions**, labeled as discussion examples rather than a single mandatory opinion.
- [ ] **Step 5: Link the answer file and audit rows; check the rule count and hand trace; commit only the answer, README, and matrix.**

### Task 6: Complete earlier ethics, fairness, and impact-assessment exercises

**Files:**
- Create: `02_AA_Ereduak_5071/soluzioak/etikako_ariketa_osagarriak.md`
- Read: `02_AA_Ereduak_5071/materialak/E1-Ereduak-Etika_eta_legea.pdf`
- Update: `02_AA_Ereduak_5071/soluzioak/README.md`
- Update: `00_Transversal/AUDITORIA_EJERCICIOS.md`

**Interfaces:**
- Produces: one clearly labeled model response for each pending ethics activity summarized by the slides, while distinguishing known slide instructions from missing referenced notebook specifications.

- [ ] **Step 1: Extract and map each outstanding activity visible in the ethics slides**, including fairness metrics, GDPR Article 22, SHAP/LIME, the student-project impact assessment, the camera-attack discussion, the three-goal argument, and a personal protocol template.
- [ ] **Step 2: Answer the hospital fairness case with a metric trade-off table** and an example team argument; leave the actual group choice blank.
- [ ] **Step 3: Explain the Article 22 decision flow and SHAP/LIME exercise at the level required by the slide prompt**; mark the full notebook tasks 3.1/12.0 as unavailable and do not invent their hidden rubric or computed results.
- [ ] **Step 4: Provide a worked mini ethical impact assessment and a defensive analysis of the physical-camera attack**, stating scenario assumptions and separating ethical recommendations from law.
- [ ] **Step 5: Give an example argument for one of the three listed goals and a fillable personal protocol**; do not claim to know a student's actual choice or values.
- [ ] **Step 6: Verify every legal statement against current official primary sources, cite the consultation date, link the answers from the README and audit rows, and commit only owned files.**
