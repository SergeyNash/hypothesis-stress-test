# Artifact Contracts

Every hypothesis run uses an isolated workspace directory (`RUN_DIR`).

## RUN_DIR structure

```text
RUN_DIR/
  hypothesis.md          # input: statement, roles, research context
  run.md                 # optional: execution log
  outputs/
    role_outputs/        # one file per role
    hypothesis_summary.md
    validation_questions.md
    market_analysis.md
    hypothesis_map.md
    hypothesis_digest.txt
    decision_review.md
    ready_for_synthesis.marker
    market_analysis_complete.marker
    synthesis_complete.marker
    decision_review_complete.marker
```

## Input: hypothesis.md

Required sections:

```markdown
# Hypothesis

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

## Output naming

| Artifact | Path | Produced by |
|----------|------|-------------|
| Per-role analysis | `outputs/role_outputs/{role_slug}.md` | Facilitator (Roles Layer) |
| Internal summary | `outputs/hypothesis_summary.md` | Facilitator (Roles Layer) |
| Interview questions | `outputs/validation_questions.md` | Facilitator (Roles Layer) |
| Market analysis | `outputs/market_analysis.md` | Market Layer |
| Full synthesis | `outputs/hypothesis_map.md` | Synthesis Layer |
| Short digest | `outputs/hypothesis_digest.txt` | Synthesis Layer |
| Decision review | `outputs/decision_review.md` | Decision Review |

Role slugs: lowercase, underscores (e.g. `appsec_engineer`, `ciso`).

### hypothesis_summary.md (facilitator)

Must include: hidden assumptions, applicability boundaries, role conflicts, key risks, key uncertainties, assessment (promising / uncertain / risky / requires validation). Language matches `hypothesis.md`.

### role_outputs/{role_slug}.md (facilitator)

Must include: pain, new problems, alternatives, failure context, applicability boundaries. Language matches `hypothesis.md`.

### validation_questions.md (facilitator)

Behavior-based interview questions per role. No leading or hypothetical questions (e.g. "Would you use this?"). Language matches `hypothesis.md`.

## Completion markers

Markers signal that a layer finished and outputs are ready for the next step:

| Marker | Created after |
|--------|---------------|
| `ready_for_synthesis.marker` | Facilitator (Roles Layer) |
| `market_analysis_complete.marker` | Market Layer |
| `synthesis_complete.marker` | Synthesis Layer |
| `decision_review_complete.marker` | Decision Review |

### hypothesis_map.md (synthesis)

Must include: confirmed signals, internal illusions, missed opportunities, local optimization traps, key divergences, blind spots, new information (post-comparison only), applicability boundaries, impact on original hypothesis, validation priorities. Language matches `hypothesis.md`.

### hypothesis_digest.txt (synthesis)

Max 150 words: viability, key conflict, primary illusion, blind spot, risk, insight, next step. Language matches `hypothesis.md`.

Do not run Synthesis until both Facilitator and Market markers exist (`ready_for_synthesis.marker` + `market_analysis_complete.marker`, or equivalent output files).

Do not run Decision Review until Synthesis completes (`synthesis_complete.marker` or `hypothesis_map.md` + `hypothesis_digest.txt` present).

## RUN_DIR examples

```text
examples/example-001/          # canonical example
runs/my-hypothesis-2026-06-09/ # user-created run
```

When the user does not specify `RUN_DIR`, ask for it or default to a new directory under `runs/`.
