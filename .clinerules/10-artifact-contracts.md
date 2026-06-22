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
    market_analysis.md
    hypothesis_map.md
    hypothesis_digest.txt
    customer_discovery_plan.md
    decision_review.md
    ready_for_synthesis.marker
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

## Completion markers

Markers signal that a layer finished and outputs are ready for the next step:

| Marker | Created after |
| -------- | --------------- |
| `ready_for_synthesis.marker` | Facilitator (Roles Layer) |
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

Do not run Synthesis until both Facilitator and Market markers exist (`ready_for_synthesis.marker` + `market_analysis_complete.marker`, or equivalent output files).

Do not run Customer Discovery Planning until Synthesis completes (`synthesis_complete.marker` or `hypothesis_map.md` + `hypothesis_digest.txt` present).

Do not run Decision Review until Customer Discovery Planning completes (`customer_discovery_planning_complete.marker` or `customer_discovery_plan.md` present).

## RUN_DIR examples

```text
examples/example-001/              # canonical example
runs/HYP-2026-06-22-001/           # user-created run archive
```

When the user does not specify `RUN_DIR`, ask for it or default to a new directory under `runs/` using the naming pattern `HYP-YYYY-MM-DD-NNN`.

## Migration note

```text
Old: runs/my-hypothesis/hypothesis.md
New: runs/HYP-YYYY-MM-DD-NNN/input/hypothesis.md
```
