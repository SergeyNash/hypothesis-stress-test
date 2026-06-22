# Decision Review

Decision Review is the **adversarial gate** after Customer Discovery Planning.

It does not re-analyze the hypothesis. It challenges conclusions already produced by the framework.

---

## Purpose

Act as an independent reviewer. Identify:

- weak evidence
- overconfidence
- unsupported conclusions
- hidden assumptions
- reasoning gaps
- confirmation bias
- missing validation
- overlooked risks

Goal: improve decision quality before a hypothesis enters backlog planning or implementation.

---

## Core principle

Assume the current conclusion may be wrong.

Your task is not to support the recommendation.

Your task is to identify why the recommendation may fail.

---

## Inputs

Required:

- `input/hypothesis.md`
- `hypothesis_summary.md`
- `market_analysis.md`
- `hypothesis_map.md`

Optional:

- `role_outputs/*`
- `hypothesis_digest.txt`
- `customer_discovery_plan.md`

---

## Review process

1. **Evaluate evidence quality** — classify each major conclusion: Strong / Moderate / Weak / Unsupported
2. **Identify hidden assumptions** — what must be true for the hypothesis to work?
3. **Search for missing perspectives** — finance, compliance, operations, platform teams, etc.
4. **Evaluate scalability** — at 10 / 50 / 100 / enterprise scale
5. **Evaluate business risk** — false positive and false negative risk
6. **Challenge the recommendation** — actively attempt to disprove it
7. **Design the cheapest validation** — maximum learning per unit of effort

---

## Output

`outputs/decision_review.md`

### Structure

- Executive Summary (confidence: High / Medium / Low; recommendation: Proceed / Proceed with Validation / Additional Research Required / Reject)
- Evidence Quality Review (table)
- Hidden Assumptions (table)
- Missing Perspectives
- Scalability Risks
- Business Risks (false positive / false negative)
- Validation Plan
- Final Recommendation

---

## Review rules

- Never repeat the synthesis
- Never summarize existing outputs
- Always add new critical thinking
- Always look for weaknesses
- Always assume uncertainty exists
- If no weaknesses are found, explicitly explain why confidence is high

---

## Relationship with other phases

- Roles Layer → internal signals
- Market Layer → external signals
- Synthesis Layer → conflict classification
- Customer Discovery Planning → interview-focused learning plan
- **Decision Review** → adversarial critique of synthesis conclusions
- **Human** → backlog decision

Decision Review does not introduce new data. It critiques existing artifacts only.

---

## Next

- `templates/decision-review-prompt.md` — manual execution
- `.cline/skills/hypothesis-decision-review/SKILL.md` — Cline execution
- `playbooks/run-hypothesis.md` — full pipeline
