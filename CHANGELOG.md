Language: **English** | [Русский](./CHANGELOG.ru.md)

# Changelog

All notable changes to the **Hypothesis Stress Test** framework are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Current version: see [VERSION](./VERSION).

## Versioning policy

| Bump | When |
| ---- | ---- |
| **MAJOR** | Breaking changes to run structure, artifact contracts, or required input |
| **MINOR** | New layers, skills, workflows, or optional capabilities |
| **PATCH** | Documentation, clarifications, non-breaking skill or rule tweaks |

Framework version is independent of individual hypothesis run IDs (`HYP-YYYY-MM-DD-NNN`).

---

## [Unreleased]

### Added

- **Human Decision Report MVP** — decision-facing `human_report.html` after Decision Review.
- Skill: `human-report-export` — compile verdict, readiness, reframing, validation priorities from existing artifacts.
- Workflow: `/run-human-report-export.md`.
- Template: `templates/human-report-template.html`.
- Report sections: What changed?, Decision Readiness, grouped Detailed Artifacts with relative links.
- Marker: `human_report_complete.marker`.
- Example: `examples/example-001/outputs/human_report.html`.

### Changed

- `/run-hypothesis.md` — Human Decision Report Export as Step 8 (after Decision Review).
- `.clinerules/10-artifact-contracts.md` — `human_report.html` contract, readiness mapping, relative-link rules.
- Playbooks, examples, architecture run-structure, cline-contract — human report as main human-facing output.
- `roadmap/README.md` — P1 Phase 1 marked implemented.

---

## [2.3.0] - 2026-06-23

### Added

- **Local Evidence Discovery** — pre-Market step to collect traceable evidence from unstructured local KB (not document search).
- New skill: `local-knowledge-retrieval` (preview, guardrails, atomic `EVID-NNN` items).
- New workflow: `/run-knowledge-retrieval.md`.
- New layer doc: `layers/local-evidence-discovery-layer.md`.
- New manual template: `templates/knowledge-retrieval-prompt.md`.
- Design reference: `architecture/local-knowledge-retrieval.md`.
- New artifacts: `discovery_preview.md`, `evidence_inventory.md`, `knowledge_retrieval_complete.marker`.
- Evidence contract fields: `evidence_type`, `relevance_reason`, `extraction_note`; atomicity rules.
- Example mixed-source KB: `examples/example-001/kb-samples/` with discovery outputs.

### Changed

- `/run-hypothesis.md` — Local Evidence Discovery as Step 3 (between Facilitator and Market).
- `hypothesis-market-layer` skill — inventory-first, then Confluence MCP; four signal channels in output.
- `/run-market-layer.md` — read `evidence_inventory.md` before Confluence search.
- `.clinerules/10-artifact-contracts.md`, `20-evidence-rules.md` — discovery artifacts and channel separation.
- Market output structure: `Local Signals from Knowledge Base`, `Confluence Signals`, `External Market Signals`, `Inferred Signals`.
- Playbooks, quick-start, cline-setup, architecture docs, SVG diagrams — inventory-first flow.
- `examples/example-001/outputs/market_analysis.md` — local signals with `EVID-*` references.
- `roadmap/README.md` — P0 #1 marked implemented; `architecture/todo.md` — P0 #1 checklist.

---

## [2.2.2] - 2026-06-23

### Added

- **Two-step confirm** for conversational run: (1) hypothesis draft (2) proposed `RUN_DIR` (`HYP-YYYY-MM-DD-NNN`).
- **RUN_DIR dialog** (Step 4b): scan today's runs, propose next suffix, list existing runs as «will not modify».
- **New run isolation**: without explicit `RUN_DIR:` in message, always create a new archive — never reuse open tabs.
- **Trigger tag** `#new-run` / `#новая` / `#новый-прогон` for explicit new-run intent.
- **Artifact allowlist** guardrail: no non-contract files (e.g. `product_specification.md`) in conversational flow.
- Example C (second hypothesis same day → `002` vs `001`) in `examples/chat-first-run.md` and `.ru.md`.

### Changed

- `conversational-hypothesis-intake` skill: Step 4a/4b split, isolation rules, continue-existing only with `RUN_DIR:`.
- `run-hypothesis-conversational.md` workflow: RUN_DIR dialog between draft confirm and bootstrap; do-not rules.
- `.clinerules/10-artifact-contracts.md` — dialog-confirmed bootstrap replaces automatic bootstrap.
- `.clinerules/00-hypothesis-framework.md` — entry modes: new hypothesis = new `HYP-*-NNN` via dialog.
- Quick start, playbooks, cline-setup (EN/RU) — two-step confirm and `#new-run` guidance.

---

## [2.2.1] - 2026-06-23

### Added

- **Intake trigger tags** for conversational run: `#hypothesis`, `#context`, `#roles` (and RU aliases `#гипотеза`, `#контекст`, `#роли`).
- **Dirty input mode** (`#context`): extract hypothesis fields from Q&A tables, CustDev notes, and unstructured discovery paste.
- **Extraction validation step**: agent shows mapped Statement/Roles/Context and asks user to confirm before draft card.
- **Status messages** before bootstrap: `runs/ NOT created yet` until explicit confirm.
- Example B (dirty `#context` flow) in `examples/chat-first-run.md` and `.ru.md`.

### Changed

- `conversational-hypothesis-intake` skill: intake modes (ready / dirty / roles-only), auto-detect, confirm triggers.
- `run-hypothesis-conversational.md` workflow: Step 0 mode detection; dirty-input example.
- Quick start, playbooks, cline-setup, README (EN/RU) — trigger tags and dirty-input guidance.
- `roadmap/README.md` — P0 #2 release table (2.2.0 / 2.2.1), follow-up backlog.
- `architecture/todo.md` — Conversational Run (P0 #2) completed and open items.

---

## [2.2.0] - 2026-06-23

### Added

- **Conversational Run (chat-first)** — primary entry path for new hypothesis runs from Cline chat.
- New skill: `conversational-hypothesis-intake` (guided Q&A, draft card preview, confirm/revise/cancel).
- New workflow: `/run-hypothesis-conversational.md` (intake → auto `RUN_DIR` bootstrap → validate → full pipeline).
- Automatic run archive creation under `runs/HYP-YYYY-MM-DD-NNN/` with `input/hypothesis.md` and `run.md`.
- Automatic metadata assignment: `Hypothesis ID`, `Run ID`, `Created at`, `Status`.
- Validation repair loop: failed input returns to conversational intake before re-validation.
- Example walkthrough: `examples/chat-first-run.md` (EN) and `examples/chat-first-run.ru.md` (RU).

### Changed

- Chat-first documented as **recommended** entry path; file-first (`RUN_DIR` + `/run-hypothesis.md`) remains as fallback.
- `.clinerules/10-artifact-contracts.md` — rules for conversational `RUN_DIR` bootstrap and ID assignment.
- `.clinerules/00-hypothesis-framework.md` — entry modes table (chat-first vs file-first).
- `roadmap/README.md` — Conversational Run marked **P0 #2 implemented**; Business Context renumbered to P0 #3.
- EN/RU docs synchronized: README, quick-start, cline-setup, cline-contract, playbooks, validate-input, templates/readme, architecture/implementations, architecture/overview, implementations/README.

---

## [2.1.0] - 2026-06-23

### Added

- New phase **Customer Discovery Planning** between Synthesis and Decision Review.
- New skill: `customer-discovery-planning`.
- New workflow: `/run-customer-discovery-planning.md`.
- New manual template: `templates/customer-discovery-planning-prompt.md`.
- New layer docs: `layers/customer-discovery-planning-layer.md`.
- New artifacts: `customer_discovery_plan.md` and `customer_discovery_planning_complete.marker`.
- Example artifacts for `examples/example-001`:
  - `outputs/customer_discovery_plan.md`
  - `outputs/customer_discovery_planning_complete.marker`
- New skill: `local-knowledge-retrieval` (**Local Evidence Discovery**).
- New workflow: `/run-knowledge-retrieval.md`.
- New manual template: `templates/knowledge-retrieval-prompt.md`.
- New layer doc: `layers/local-evidence-discovery-layer.md`.
- New retrieval artifacts: `discovery_preview.md`, `evidence_inventory.md`, `knowledge_retrieval_complete.marker`.

### Changed

- Full pipeline order updated to:
  - Validate -> Facilitator -> Market -> Synthesis -> Customer Discovery Planning -> Decision Review -> Human backlog decision.
- Decision Review prerequisites now include Customer Discovery Planning outputs.
- Synthesis next-step guidance now points to Customer Discovery Planning before Decision Review.
- Artifact contracts, workflows, and docs updated across EN/RU:
  - README, playbooks, quick start, architecture docs, Cline contract/setup docs.
- Pipeline diagrams updated:
  - `assets/architecture-overview.svg`
  - `assets/artifact-flow.svg`
  - `assets/cline-workflow.svg`
- Full pipeline order now includes Local Evidence Discovery before Market:
  - Validate -> Facilitator -> Local Evidence Discovery -> Market -> Synthesis -> Customer Discovery Planning -> Decision Review -> Human backlog decision.
- Market Layer updated to channel-separated output:
  - `Local Signals from Knowledge Base`
  - `Confluence Signals`
  - `External Market Signals`
  - `Inferred Signals`
- Market now consumes `evidence_inventory.md` before Confluence search (inventory-first, then Confluence, then external/inferred).
- Artifact contracts and evidence rules updated for atomic evidence items (`evidence_type`, `relevance_reason`, `extraction_note`) and retrieval preview.
- EN/RU docs updated across architecture, playbooks, quick-start, Cline contract/setup, knowledge-base docs, and templates.
- Additional diagrams and reference output updated for the new flow:
  - `assets/cline-mcp-confluence.svg`
  - `assets/artifact-flow-clean.svg`
  - `examples/example-001/outputs/market_analysis.md`

---

## [2.0.0] - 2026-06-22

### Changed

- **Run archive contract (breaking):** hypothesis input moved to `RUN_DIR/input/hypothesis.md`; outputs remain in `RUN_DIR/outputs/`.
- `RUN_DIR` naming pattern: `runs/HYP-YYYY-MM-DD-NNN/`.
- Required **Metadata** block in input: Hypothesis ID, Created at, Run ID, Status.
- All skills, workflows, templates, and docs updated for the new paths.
- `examples/example-001` migrated to the archive layout (`input/`, `outputs/`, `run.md`).

### Added

- Optional `input/attachments/` directory for supporting files per run.
- Migration note in `.clinerules/10-artifact-contracts.md` for users on the old layout.

---

## [1.3.0] - 2026-06-19

### Added

- **Persona model:** `knowledge-base/personas/`, `knowledge-base/interviews/`, `knowledge-base/persona-builds/`.
- Five initial AppSec personas (initial profiles, `confidence: low` until backed by CustDev).
- Persona evidence rules in `.clinerules/20-evidence-rules.md`.
- Roles Layer support for matching personas as supporting context (`hypothesis-facilitator` skill).

---

## [1.2.0] - 2026-06-09

### Added

- **Local Optimization Trap** signal pattern in Synthesis Layer.
- `validation_questions.md` as a Facilitator output (behavior-based interview questions).

### Changed

- Roles Layer reframed as **Facilitator** in pipeline documentation.
- Signal model and synthesis skill expanded with cross-signal patterns.

---

## [1.1.0] - 2026-06-09

### Added

- **Decision Review** as a mandatory gate after Synthesis.
- `hypothesis-decision-review` skill and `/run-decision-review.md` workflow.
- `decision_review.md` and `decision_review_complete.marker` artifacts.

---

## [1.0.0] - 2026-06-09

### Added

- Tool-agnostic layered framework: Roles, Market, Synthesis.
- **Cline adapter:** `.clinerules/`, `.cline/skills/`, slash-command workflows.
- Artifact contracts, completion markers, `RUN_DIR` isolation.
- Confluence-first Market Layer and evidence rules (`local` / `external` / `inferred`).
- Quick Start, playbooks, architecture docs, `examples/example-001`.
- Bilingual documentation (EN / RU).

---

## [0.1.0] - 2026-06-08

### Added

- Initial framework concept: stress-test existing ideas instead of generating new ones.
- Manual execution templates in `templates/`.
- Layer reasoning model in `layers/`.

[2.2.2]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v2.2.1...v2.2.2
[2.2.1]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v2.2.0...v2.2.1
[2.2.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v1.3.0...v2.0.0
[1.3.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/SergeyNash/hypothesis-stress-test/releases/tag/v0.1.0
