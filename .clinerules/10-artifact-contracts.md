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
    market_analysis.md
    hypothesis_map.md
    hypothesis_digest.txt
    ready_for_synthesis.marker
    market_analysis_complete.marker
    synthesis_complete.marker
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
| Per-role analysis | `outputs/role_outputs/{role_slug}.md` | Roles Layer |
| Internal summary | `outputs/hypothesis_summary.md` | Roles Layer |
| Market analysis | `outputs/market_analysis.md` | Market Layer |
| Full synthesis | `outputs/hypothesis_map.md` | Synthesis Layer |
| Short digest | `outputs/hypothesis_digest.txt` | Synthesis Layer |

Role slugs: lowercase, underscores (e.g. `appsec_engineer`, `ciso`).

## Completion markers

Markers signal that a layer finished and outputs are ready for the next step:

| Marker | Created after |
|--------|---------------|
| `ready_for_synthesis.marker` | Roles Layer |
| `market_analysis_complete.marker` | Market Layer |
| `synthesis_complete.marker` | Synthesis Layer |

Do not run Synthesis until both Roles and Market markers exist (or their output files are present).

## RUN_DIR examples

```text
examples/example-001/          # canonical example
runs/my-hypothesis-2026-06-09/ # user-created run
```

When the user does not specify `RUN_DIR`, ask for it or default to a new directory under `runs/`.
