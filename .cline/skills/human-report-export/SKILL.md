---
name: human-report-export
description: Generate a decision-facing human_report.html after Decision Review. Summarize verdict, readiness, reframing, and validation priorities with grouped links to source Markdown artifacts.
---

# Human Decision Report Export

Generate `human_report.html` — a concise, decision-facing HTML report for humans.

This skill does not re-analyze the hypothesis. It compiles existing artifacts into a readable decision slice.

## Purpose

Help a human answer:

- What was the hypothesis?
- What is the recommendation and confidence?
- Is this ready for backlog, or what is still missing?
- What changed from the original framing?
- What validation should happen next?

Markdown artifacts remain the source of truth. HTML is a human-facing view.

## Prerequisites

Required:

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/decision_review.md`

Recommended:

- `RUN_DIR/outputs/decision_review_complete.marker`
- `RUN_DIR/outputs/hypothesis_digest.txt`
- `RUN_DIR/outputs/hypothesis_map.md`
- `RUN_DIR/outputs/customer_discovery_plan.md`

Stop if `decision_review.md` is missing. Ask user to complete Decision Review first.

## Source mapping

| Report section | Source artifacts |
| -------------- | ---------------- |
| Metadata, statement | `input/hypothesis.md` |
| Digest | `hypothesis_digest.txt` |
| What changed? | `hypothesis_map.md` (`Impact on Original Hypothesis`), fallback digest + `decision_review.md` |
| Confidence, recommendation | `decision_review.md` (Executive Summary, Final Recommendation) |
| Decision Readiness | derived from `decision_review.md` (see mapping below) |
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
| `Needs business context` | strategic fit, buyer, budget, or business value evidence is missing |
| `Reject / reframe` | reject/reframe recommendation or original hypothesis is materially wrong |

Add one short supporting sentence grounded in `decision_review.md`.

## What changed?

Extract from `hypothesis_map.md` section `Impact on Original Hypothesis` when present:

- **Original framing:** from `input/hypothesis.md` statement or synthesis summary
- **Reframed as:** from synthesis impact / digest primary insight
- **Why changed:** from synthesis divergences or decision review executive summary

If `hypothesis_map.md` is missing, derive conservatively from digest + decision review only. Do not invent unsupported claims.

## Relative link rules

Report path: `RUN_DIR/outputs/human_report.html`

Generate links relative to `outputs/`:

- Input: `../input/hypothesis.md`
- Sibling output: `hypothesis_digest.txt`, `decision_review.md`, `customer_discovery_plan.md`
- Role output: `role_outputs/{role_slug}.md`

**Detailed artifact groups** (omit links to files that do not exist):

1. **Input** — `../input/hypothesis.md`
2. **Role Analysis** — `hypothesis_summary.md`, `validation_questions.md`, `role_outputs/*.md`
3. **Evidence** — `discovery_preview.md`, `evidence_inventory.md`
4. **Market** — `market_analysis.md`
5. **Synthesis** — `hypothesis_digest.txt`, `hypothesis_map.md`
6. **Customer Discovery** — `customer_discovery_plan.md`
7. **Decision Review** — `decision_review.md`

## Generation process

1. Read source artifacts listed above.
2. Use `templates/human-report-template.html` as structural reference.
3. Fill all required sections. Use same language as `input/hypothesis.md`.
4. Write `RUN_DIR/outputs/human_report.html` — single file, inline CSS + minimal vanilla JS.
5. Write `RUN_DIR/outputs/human_report_complete.marker`.
6. Tell user to open `outputs/human_report.html` in a browser.

## Required outputs

1. `RUN_DIR/outputs/human_report.html`
2. `RUN_DIR/outputs/human_report_complete.marker`

Marker content:

```text
Human decision report export completed.
human_report.html generated.
Source artifacts preserved as Markdown.
```

## HTML constraints

- Static HTML only; opens via `file://`
- Inline CSS and minimal vanilla JS only
- No CDN, npm, build tools, external fonts, or images
- Sticky header with nav anchors: Summary, What changed, Decision, Validation, Details
- Badges for confidence, recommendation, decision readiness
- Collapsible blocks optional for long validation content

## Review rules

- Do not re-run analysis layers
- Do not modify source Markdown artifacts
- Do not embed full pipeline dumps
- Missing optional artifacts → show "not available" card, not failure
- All artifact links must be valid relative paths from `outputs/`
