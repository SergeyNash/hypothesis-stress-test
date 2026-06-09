# Synthesis Prompt

This is an execution template, not a system prompt.

RUN_DIR: [set your run directory]

---

## What this phase does NOT do

- Does not summarize role or market outputs without comparison
- Does not perform market research
- Does not re-run role analysis
- Does not make final product decisions

---

## Prerequisites

- `outputs/ready_for_synthesis.marker`
- `outputs/market_analysis_complete.marker`
- `outputs/role_outputs/*`
- `outputs/hypothesis_summary.md`
- `outputs/market_analysis.md`

---

## Task

Compare internal (roles) vs external (market) signals. Discover what becomes visible only after collision.

Do NOT generate new ideas. Do NOT add external assumptions. Do NOT smooth contradictions.

---

## Signal model

1. Validated Opportunity — roles + market align
2. Internal Illusion — roles yes, market no
3. Blind Spot — market yes, roles no
4. Weak Signal — weak evidence everywhere
5. Local Optimization Trap — pain confirmed but no strategic business value

---

## Analysis process

1. Internal alignment (agreement / tension / conflict zones)
2. Market validation (confirmed / weak / unconfirmed problems, alternatives)
3. Cross-signal analysis with validation priority (HIGH / MEDIUM / LOW)
4. Applicability discovery
5. Blind spot discovery
6. New information discovery (mandatory — only post-comparison insights)
7. Decision impact on original hypothesis (keep / narrow / expand / reframe / change audience / require validation / reject)

---

## Output language

Match the language of `hypothesis.md`.

---

## Output requirements

1. `RUN_DIR/outputs/hypothesis_map.md` — full synthesis (see skill for EN/RU structure)
2. `RUN_DIR/outputs/hypothesis_digest.txt` — max 150 words
3. `RUN_DIR/outputs/synthesis_complete.marker`

---

## Review rules

- Focus on conflicts, not summaries
- Never smooth contradictions
- Never invent signals
- Uncertainty is allowed and expected

See `.cline/skills/hypothesis-synthesis/SKILL.md` for full output structures.
