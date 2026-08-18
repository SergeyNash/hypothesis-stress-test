---
name: human-report-export
description: Generate an executive human_report.html after Decision Review. Compile verdict, business value, contradictions, cheapest validation, and grouped artifact links.
---

# Human Decision Report Export (Executive)

Generate `human_report.html` — a decision-facing **executive report** for product leaders.

This skill does not re-analyze the hypothesis. It compiles existing artifacts into a readable decision slice.

## Purpose

Help a human answer:

- What was the hypothesis?
- What is the recommendation and confidence?
- Is this ready for backlog, or what is still missing?
- What changed from the original framing?
- How does this connect to business value and strategy?
- What are the top contradictions?
- What is the cheapest validation path?

Markdown artifacts remain the source of truth. HTML is a human-facing view.

## Prerequisites

Required:

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/decision_review.md`
- `RUN_DIR/outputs/decision_review_complete.marker` with canonical JSON
  `status: completed`

Recommended:

- `RUN_DIR/outputs/hypothesis_digest.txt`
- `RUN_DIR/outputs/hypothesis_map.md`
- `RUN_DIR/outputs/customer_discovery_plan.md`
- `RUN_DIR/outputs/business_context_analysis.md` or
  `RUN_DIR/outputs/missing_business_context.md`

Stop if Decision Review is incomplete. Ask user to complete it first.

Validate-only mode: if the user asks to check the report without writing files,
run the HTML section checklist and stop.

## Source mapping

| Report section | Source artifacts |
| -------------- | ---------------- |
| Metadata, statement | `input/hypothesis.md` |
| Digest | `hypothesis_digest.txt` |
| Business value | `business_context_analysis.md` (Business Effect Type, Strategic Fit, Value Flow, Summary) |
| What changed? | `hypothesis_map.md` (`Impact on Original Hypothesis`), fallback digest + `decision_review.md` |
| Top contradictions | `hypothesis_map.md` (`Key Divergences`, max 3 items) |
| Confidence, recommendation | `decision_review.md` (Executive Summary, Final Recommendation) |
| Decision Readiness | derived from `decision_review.md` + business context (see mapping below) |
| Cheapest validation | `decision_review.md` (`Validation Plan`, lowest effort rows) |
| Validation priorities | `customer_discovery_plan.md` (HIGH unknowns, High Priority, interview roles) |
| Signal snapshot | `market_analysis.md` (`Signal Summary` only) |
| Detailed artifacts | grouped links to existing contract files |

Do not embed full content of: `role_outputs/*`, full `hypothesis_map.md`, full `evidence_inventory.md`, full `market_analysis.md`.

## Decision Readiness mapping

Choose one most action-guiding status:

| Status | Use when |
| ------ | -------- |
| `Ready for backlog` | recommendation supports build/commit and confidence is high |
| `Needs interviews` | validation-first recommendation, customer discovery is next step, or critical unknowns remain |
| `Needs business context` | `missing_business_context.md` exists, or strategic fit / buyer / budget evidence is missing |
| `Reject / reframe` | reject/reframe recommendation or original hypothesis is materially wrong |

Prefer `Needs business context` when `missing_business_context.md` is present even if other signals look positive.

Add one short supporting sentence grounded in `decision_review.md` or business context.

## What changed?

Extract from `hypothesis_map.md` section `Impact on Original Hypothesis` when present:

- **Original framing:** from `input/hypothesis.md` statement or synthesis summary
- **Reframed as:** from synthesis impact / digest primary insight
- **Why changed:** from synthesis divergences or decision review executive summary

## Top contradictions

From `hypothesis_map.md` → `Key Divergences`: include up to 3 items with title, contradiction summary, and validation priority if stated.

If section missing, omit section or show "not available".

## Cheapest validation

From `decision_review.md` → `Validation Plan`: list items marked Low effort first (max 4). Include objective and expected learning.

If there is no effort column, take the first 4 validation items in document order and label them `effort: unspecified`.

## Relative link rules

Report path: `RUN_DIR/outputs/human_report.html`

**Detailed artifact groups** (omit links to files that do not exist):

1. **Input** — `../input/hypothesis.md`
2. **Role Analysis** — `hypothesis_summary.md`, `validation_questions.md`, `role_outputs/*.md`
3. **Evidence** — `discovery_preview.md`, `evidence_inventory.md`
4. **Business Context** — `business_context_analysis.md`, `missing_business_context.md`
5. **Market** — `market_analysis.md`
6. **Synthesis** — `hypothesis_digest.txt`, `hypothesis_map.md`
7. **Customer Discovery** — `customer_discovery_plan.md`
8. **Decision Review** — `decision_review.md`

## Generation process

1. Read source artifacts listed above.
2. Use `templates/human-report-template.html` as structural reference.
3. Fill all required sections. Use same language as `input/hypothesis.md`.
4. Tick this checklist before writing (or in validate-only mode):
   1. Sticky header — Hypothesis ID, confidence, recommendation, decision readiness
   2. Executive overview
   3. Business value (or not-available card when gap)
   4. What changed?
   5. Top contradictions
   6. Decision summary
   7. Cheapest validation
   8. Validation priorities
   9. Signal snapshot (or not-available)
   10. Detailed artifacts
5. Write `RUN_DIR/outputs/human_report.html` — single file, inline CSS + minimal vanilla JS.
6. Write `RUN_DIR/outputs/human_report_complete.marker`:

```json
{
  "status": "completed",
  "completed_phase": "human_report",
  "next_phase": "human_decision",
  "inputs": [
    "outputs/human_report.html"
  ]
}
```

7. Tell user to open `outputs/human_report.html` in a browser.

## HTML constraints

- Static HTML only; opens via `file://`
- Inline CSS and minimal vanilla JS only
- Sticky header nav: Summary, Business, What changed, Contradictions, Decision, Validation, Details
- Executive tone: short paragraphs, scannable tables, no pipeline dumps

## Review rules

- Do not re-run analysis layers
- Do not modify source Markdown artifacts
- Missing optional artifacts → show "not available" card, not failure
