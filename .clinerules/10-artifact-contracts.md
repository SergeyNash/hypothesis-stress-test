# Artifact Contracts

Every hypothesis run uses an isolated workspace directory (`RUN_DIR`) — a hypothesis run archive.

## RUN_DIR structure

```text
RUN_DIR/
  input/
    hypothesis.md          # input: metadata, statement, roles, research context
    attachments/           # optional: supporting files
  run.md                   # optional: execution log
  outputs/
    role_outputs/          # one file per role
    hypothesis_summary.md
    validation_questions.md
    discovery_preview.md
    evidence_inventory.md
    market_analysis.md
    hypothesis_map.md
    hypothesis_digest.txt
    customer_discovery_plan.md
    decision_review.md
    ready_for_synthesis.marker
    knowledge_retrieval_complete.marker
    market_analysis_complete.marker
    synthesis_complete.marker
    customer_discovery_planning_complete.marker
    decision_review_complete.marker
```

## Input: input/hypothesis.md

Required sections:

```markdown
# Hypothesis

## Metadata

- Hypothesis ID: HYP-YYYY-MM-DD-NNN
- Created at: YYYY-MM-DD
- Run ID: RUN-YYYY-MM-DD-NNN
- Status: draft | running | completed | archived

## Statement
[Clear, testable statement]

## Relevant Roles
- [role 1]
- [role 2]

## Research Context
- Domain: [domain]
- Target audience: [audience]
- Scenario: [scenario]
- Constraints: [optional]
```

See `templates/input-schema.md` for the full schema.

## Optional local role sources

Reusable role profiles may exist in:

```text
knowledge-base/personas/
```

Raw CustDev inputs and persona rebuild logs may exist in:

```text
knowledge-base/interviews/
knowledge-base/persona-builds/
```

Roles listed in `input/hypothesis.md` remain the run-specific source of scope. Persona files are supporting context, not a replacement for hypothesis-specific role selection.

## Output naming

| Artifact | Path | Produced by |
| ---------- | ------ | ------------- |
| Per-role analysis | `outputs/role_outputs/{role_slug}.md` | Facilitator (Roles Layer) |
| Internal summary | `outputs/hypothesis_summary.md` | Facilitator (Roles Layer) |
| Interview questions | `outputs/validation_questions.md` | Facilitator (Roles Layer) |
| Retrieval preview | `outputs/discovery_preview.md` | Local Evidence Discovery |
| Evidence inventory | `outputs/evidence_inventory.md` | Local Evidence Discovery |
| Market analysis | `outputs/market_analysis.md` | Market Layer |
| Full synthesis | `outputs/hypothesis_map.md` | Synthesis Layer |
| Short digest | `outputs/hypothesis_digest.txt` | Synthesis Layer |
| Customer discovery plan | `outputs/customer_discovery_plan.md` | Customer Discovery Planning |
| Decision review | `outputs/decision_review.md` | Decision Review |

Role slugs: lowercase, underscores (e.g. `appsec_engineer`, `ciso`).

### hypothesis_summary.md (facilitator)

Must include: hidden assumptions, applicability boundaries, role conflicts, key risks, key uncertainties, assessment (promising / uncertain / risky / requires validation). Language matches `input/hypothesis.md`.

### role_outputs/{role_slug}.md (facilitator)

Must include: pain, new problems, alternatives, failure context, applicability boundaries. Language matches `input/hypothesis.md`.

### validation_questions.md (facilitator)

Behavior-based interview questions per role. No leading or hypothetical questions (e.g. "Would you use this?"). Language matches `input/hypothesis.md`.

### discovery_preview.md (local evidence discovery)

Must include:

- limits applied (`max_files_scanned`, `max_file_size`, `max_evidence_items`)
- files scanned
- files skipped with reasons
- candidate files
- top relevant files with planned evidence type

Preview is mandatory and generated before evidence extraction.

### evidence_inventory.md (local evidence discovery)

Must include atomic `EVID-NNN` items. Each item should capture one signal only.

Required fields per item:

- `source_path`
- `source_kind`
- `evidence_type` (`quote`, `transcript_excerpt`, `image_observation`, `metadata_only`, `observation`)
- `observation`
- `relevance`
- `relevance_reason`
- `retrieved_by`

Optional fields:

- `location`
- `companion_source`
- `extraction_note` (required for `image_observation`)

## Completion markers

Markers signal that a layer finished and outputs are ready for the next step:

| Marker | Created after |
| -------- | --------------- |
| `ready_for_synthesis.marker` | Facilitator (Roles Layer) |
| `knowledge_retrieval_complete.marker` | Local Evidence Discovery |
| `market_analysis_complete.marker` | Market Layer |
| `synthesis_complete.marker` | Synthesis Layer |
| `customer_discovery_planning_complete.marker` | Customer Discovery Planning |
| `decision_review_complete.marker` | Decision Review |

### hypothesis_map.md (synthesis)

Must include: confirmed signals, internal illusions, missed opportunities, local optimization traps, key divergences, blind spots, new information (post-comparison only), applicability boundaries, impact on original hypothesis, validation priorities. Language matches `input/hypothesis.md`.

### hypothesis_digest.txt (synthesis)

Max 150 words: viability, key conflict, primary illusion, blind spot, risk, insight, next step. Language matches `input/hypothesis.md`.

### customer_discovery_plan.md (customer discovery planning)

Must include: research objective, what is already known, critical unknowns with risk type and priority, recommended interview roles, behavior-based interview guide, research priorities (HIGH / MEDIUM / LOW), expected learning outcomes. Language matches `input/hypothesis.md`.

Do not run Market Layer until Facilitator completes (`ready_for_synthesis.marker` or equivalent facilitator outputs). Local Evidence Discovery is recommended before Market but optional for backward compatibility.

Do not run Synthesis until both Facilitator and Market markers exist (`ready_for_synthesis.marker` + `market_analysis_complete.marker`, or equivalent output files).

Do not run Customer Discovery Planning until Synthesis completes (`synthesis_complete.marker` or `hypothesis_map.md` + `hypothesis_digest.txt` present).

Do not run Decision Review until Customer Discovery Planning completes (`customer_discovery_planning_complete.marker` or `customer_discovery_plan.md` present).

## RUN_DIR examples

```text
examples/example-001/              # canonical example
runs/HYP-2026-06-22-001/           # user-created run archive
```

When the user does not specify `RUN_DIR`:

- **Chat-first (preferred):** invoke `/run-hypothesis-conversational.md` — intake collects input, agent **proposes** new `runs/HYP-YYYY-MM-DD-NNN/` in dialog, user confirms, then bootstrap.
- **File-first (fallback):** ask for `RUN_DIR` or create a new directory under `runs/` using the naming pattern `HYP-YYYY-MM-DD-NNN`.

When the user **does** specify `RUN_DIR: runs/HYP-...` — continue that existing archive; do not create a new folder.

### Conversational bootstrap (dialog-confirmed)

When creating a new run via `/run-hypothesis-conversational.md` (no `RUN_DIR:` in message):

**Two-step confirm:**

1. User confirms hypothesis draft card
2. Agent proposes next free `HYP-YYYY-MM-DD-NNN`, lists existing runs for today, user confirms `RUN_DIR`

**Only after step 2** — create directory and write `input/hypothesis.md`.

**New run isolation:**

- Never reuse an existing `runs/HYP-*` for a new hypothesis
- Open editor tabs from a previous run are not a write target
- Scan `runs/` for `HYP-YYYY-MM-DD-*`, propose next `NNN` (001, 002, …)
- Set `Hypothesis ID` = folder name; `Run ID` = `RUN-YYYY-MM-DD-NNN`
- Folder name must match `Hypothesis ID` in metadata
- Write only contract artifacts from this document — no ad-hoc files (e.g. `product_specification.md`)

## Migration note

```text
Old: runs/my-hypothesis/hypothesis.md
New: runs/HYP-YYYY-MM-DD-NNN/input/hypothesis.md
```
