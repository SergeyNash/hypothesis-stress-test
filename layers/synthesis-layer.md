# Synthesis Layer

The Synthesis Layer is the **signal collision layer** of the system.

It compares internal (roles) and external (market) signals and exposes what becomes visible only after comparison.

---

## What this layer does NOT do

- Does not summarize role or market outputs without comparison
- Does not perform market research
- Does not re-analyze roles
- Does not make final product decisions

---

## Purpose

The goal is not to summarize previous analysis.

The goal is to discover:

> What becomes visible only when internal logic meets external reality?

Truth emerges from contradictions — not from agreement.

---

## Inputs

Required:

- `hypothesis_summary.md`
- `market_analysis.md`
- `role_outputs/*`

Optional:

- `validation_questions.md`

## Start conditions

- `ready_for_synthesis.marker`
- `market_analysis_complete.marker`

---

## Signal model

| Category | Pattern | Risk |
|----------|---------|------|
| **Validated Opportunity** | Roles YES + Market YES | Strong signal |
| **Internal Illusion** | Roles YES + Market NO | Local problem may not exist systematically |
| **Blind Spot** | Roles NO + Market YES | Organization misses opportunity |
| **Weak Signal** | Weak everywhere | Decision based on assumptions |
| **Local Optimization Trap** | Pain confirmed, no strategic value | Efficiency without strategic outcomes |

---

## Analysis process

1. Internal alignment analysis (agreement / tension / conflict zones)
2. Market validation analysis (confirmed / weak / unconfirmed problems)
3. Cross-signal analysis with validation priority
4. Applicability discovery
5. Blind spot discovery
6. New information discovery (mandatory — post-comparison only)
7. Decision impact on original hypothesis

---

## Outputs

| Artifact | Purpose |
|----------|---------|
| `hypothesis_map.md` | Full collision analysis |
| `hypothesis_digest.txt` | Short digest (max 150 words) |
| `synthesis_complete.marker` | Ready for Decision Review |

### hypothesis_map.md sections

- Unified summary
- Confirmed signals, internal illusions, missed opportunities
- Local optimization traps, key divergences, blind spots
- New information (post-comparison only)
- Applicability boundaries
- Impact on original hypothesis
- Validation priorities

Output language matches `hypothesis.md`.

---

## Review rules

- Never smooth contradictions
- Never prioritize consensus
- Never invent signals
- Never summarize without comparison
- Always search for reframing opportunities

---

## Relationship with other layers

- Facilitator (Roles) → internal signals
- Market Layer → external signals
- **Synthesis** → signal collision
- Decision Review → adversarial critique of synthesis conclusions

---

## Next

- `decision-review-layer.md`
- `templates/synthesis-prompt.md` — manual execution
- `.cline/skills/hypothesis-synthesis/SKILL.md` — Cline execution
