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

- New phase **Customer Discovery Planning** between Synthesis and Decision Review.
- New skill: `customer-discovery-planning`.
- New workflow: `/run-customer-discovery-planning.md`.
- New manual template: `templates/customer-discovery-planning-prompt.md`.
- New layer docs: `layers/customer-discovery-planning-layer.md`.
- New artifacts: `customer_discovery_plan.md` and `customer_discovery_planning_complete.marker`.
- Example artifacts for `examples/example-001`:
  - `outputs/customer_discovery_plan.md`
  - `outputs/customer_discovery_planning_complete.marker`

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

[2.0.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v1.3.0...v2.0.0
[1.3.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/SergeyNash/hypothesis-stress-test/releases/tag/v0.1.0
