---
name: hypothesis-roles-layer
description: Execute the Roles Layer of the hypothesis stress-test. Analyze a hypothesis through relevant role perspectives and produce role_outputs and hypothesis_summary. Use after input validation.
---

# Roles Layer

Execute internal analysis of the hypothesis through each relevant role.

## Prerequisites

- `RUN_DIR/hypothesis.md` exists and passed validation
- Roles are listed in the input file

## Instructions

Read `RUN_DIR/hypothesis.md`. For **each role** listed:

1. **Pain point** — priority: critical / secondary / none
2. **New problems** — complexity or friction introduced by the hypothesis
3. **Alternatives** — what the role would do instead (including "do nothing")
4. **Failure conditions** — when this becomes useless or harmful

## Constraints

- Do NOT validate the hypothesis
- Do NOT assume value
- Do NOT consider market reality
- Focus on boundaries and limitations

## Outputs

Write to `RUN_DIR/outputs/`:

### Per-role files

`RUN_DIR/outputs/role_outputs/{role_slug}.md`

One file per role. Use lowercase slugs with underscores.

### Summary

`RUN_DIR/outputs/hypothesis_summary.md` containing:

- Hypothesis statement
- Hidden assumptions (list)
- Role summary table (pain priority, adoption readiness)
- Validation recommendations

### Completion marker

`RUN_DIR/outputs/ready_for_synthesis.marker` — empty file or timestamp.

## Reference

Based on `templates/facilitator-prompt.md` and `layers/roles-layer.md`.
