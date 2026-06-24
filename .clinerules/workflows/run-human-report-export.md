# Run Human Decision Report Export

Generate a decision-facing HTML report for an existing completed `RUN_DIR`.

## Prerequisites

Confirm these exist:

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/decision_review.md`

Recommended:

- `RUN_DIR/outputs/decision_review_complete.marker`
- `RUN_DIR/outputs/hypothesis_digest.txt`
- `RUN_DIR/outputs/customer_discovery_plan.md`

If `decision_review.md` is missing, stop and ask user to complete Decision Review first.

## Steps

1. Confirm `RUN_DIR` and `decision_review.md` exist.
2. Activate skill `human-report-export`.
3. Read source artifacts per skill mapping.
4. Generate `RUN_DIR/outputs/human_report.html`.
5. Generate `RUN_DIR/outputs/human_report_complete.marker`.
6. Show user:
   - path to `human_report.html`
   - confidence, recommendation, decision readiness
   - one-line "what changed" summary
   - reminder: open in browser; Markdown artifacts remain source of truth

## Rules

- Do not modify existing Markdown artifacts.
- Do not re-run pipeline layers.
- Omit links to artifacts that do not exist.
- Use relative links from `outputs/` only.

## Reference

- Skill: `.cline/skills/human-report-export/SKILL.md`
- Template: `templates/human-report-template.html`
- Contract: `.clinerules/10-artifact-contracts.md` — `human_report.html`
