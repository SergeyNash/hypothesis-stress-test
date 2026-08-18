# Run Human Decision Report Export

Generate a decision-facing HTML report for an existing completed `RUN_DIR`.

## Prerequisites

Confirm these exist:

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/decision_review.md`
- `RUN_DIR/outputs/decision_review_complete.marker` with canonical JSON
  `status: completed`

Recommended:

- `RUN_DIR/outputs/hypothesis_digest.txt`
- `RUN_DIR/outputs/customer_discovery_plan.md`
- `RUN_DIR/outputs/business_context_analysis.md` or
  `RUN_DIR/outputs/missing_business_context.md`

If the Decision Review marker is missing, stop and ask user to complete Decision Review first.

## Steps

1. Confirm `RUN_DIR` and the Decision Review gate above.
2. Activate skill `human-report-export`.
3. If the user asked for validate-only, run the HTML section checklist without writing files.
4. Read source artifacts per skill mapping.
5. Generate `RUN_DIR/outputs/human_report.html`.
6. Generate `RUN_DIR/outputs/human_report_complete.marker` as the canonical JSON body from `.clinerules/10-artifact-contracts.md`.
7. Show user:
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
