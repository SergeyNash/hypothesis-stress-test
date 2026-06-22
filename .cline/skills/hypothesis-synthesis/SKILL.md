---
name: hypothesis-synthesis
description: Compare role-based analysis and market analysis to identify contradictions, validated opportunities, blind spots, applicability boundaries, and changes required to the original hypothesis.
---

# Hypothesis Synthesis

## Purpose

The purpose of this skill is NOT to summarize previous outputs.

The purpose is to discover what becomes visible only after comparing:

1. Internal perspective (roles)
2. External perspective (market)

This skill acts as a signal collision layer.

It does not generate new opinions.

It does not perform market research.

It does not re-analyze roles.

It works exclusively with existing artifacts.

## What this skill does NOT do

- Does not summarize role or market outputs without comparison
- Does not perform market research
- Does not re-run role analysis
- Does not make final product decisions (Decision Review follows)

## Inputs

Required:

- `RUN_DIR/outputs/hypothesis_summary.md`
- `RUN_DIR/outputs/market_analysis.md`
- `RUN_DIR/outputs/role_outputs/*`

Optional:

- `RUN_DIR/outputs/validation_questions.md`
- additional role outputs
- previous synthesis artifacts

## Working directory

The user provides `RUN_DIR`.

All files MUST be read from and written to `RUN_DIR/outputs/`.

Never write files outside this directory.

## Output language

Write all artifact headings and body text in the **same language as `input/hypothesis.md`**.

## Start conditions

Run synthesis only if these exist:

- `RUN_DIR/outputs/ready_for_synthesis.marker`
- `RUN_DIR/outputs/market_analysis_complete.marker`

Or equivalent output files: `role_outputs/*`, `hypothesis_summary.md`, `market_analysis.md`.

If markers or required files are missing:

- stop analysis
- report incomplete pipeline
- describe missing dependencies

## Core principle

Truth emerges from contradictions.

The purpose of synthesis is not agreement.

The purpose of synthesis is to discover:

- contradictions
- blind spots
- internal illusions
- missed opportunities
- applicability boundaries

The highest-value signal is often conflict.

## Signal model

Every finding belongs to one or more categories:

### Validated Opportunity

Roles agree. Market confirms. Strong signal.

### Internal Illusion

Roles support the hypothesis. Market does not confirm it.

Risk: organization solves a local problem that may not exist systematically.

### Blind Spot

Market confirms something important. Roles do not recognize it.

Risk: organization misses an opportunity.

### Weak Signal

Neither roles nor market provide strong evidence.

Risk: decision based mostly on assumptions.

### Local Optimization Trap

Roles experience pain. Market confirms pain. But solving this pain does not create meaningful business value.

Risk: improving local efficiency without improving strategic outcomes.

## Analysis process

### Step 1 — Internal alignment analysis

Analyze all role outputs. Determine:

- Agreement zones
- Tension zones
- Conflict zones
- Role-specific risks

### Step 2 — Market validation analysis

Determine:

- Confirmed problems
- Weakly confirmed problems
- Unconfirmed problems
- Existing alternatives

### Step 3 — Cross-signal analysis

Compare role signal vs market signal:

| Pattern | Classification |
|---------|----------------|
| Roles YES + Market YES | Validated Opportunity |
| Roles YES + Market NO | Internal Illusion |
| Roles NO + Market YES | Blind Spot |
| Roles WEAK + Market WEAK | Low Signal Hypothesis |
| Roles YES + Market YES + Buyer NO | Local Optimization Trap |

For each divergence include: contradiction, business consequence, validation priority (HIGH / MEDIUM / LOW).

### Step 4 — Applicability discovery

Determine:

- For whom does this work?
- For whom does this not work?
- Under what conditions does it work or fail?
- At what scale does it stop working?

Objective: discover natural boundaries, not force a single classification.

### Step 5 — Blind spot discovery

Ask:

- Who owns implementation? Who pays? Who receives value? Who experiences pain?
- What blocks adoption? What prevents rollout?
- Which stakeholders were ignored?
- Which assumptions remain untested?

### Step 6 — New information discovery (mandatory)

List only findings visible after comparison.

Do NOT repeat role outputs, market analysis, or hypothesis summary.

Only include: new insights, newly discovered contradictions, constraints, opportunities.

Ask: What do we know now that we did not know before synthesis?

### Step 7 — Decision impact analysis

Determine how synthesis should change the original hypothesis:

- Keep Current Framing
- Narrow Scope
- Expand Scope
- Reframe Problem
- Change Audience
- Require Validation
- Reject Current Framing

## Output artifacts

### File 1: `RUN_DIR/outputs/hypothesis_map.md`

**English structure:**

```markdown
# Unified Hypothesis Summary
...

# Confirmed Signals
...

# Internal Illusions
...

# Missed Opportunities
...

# Local Optimization Traps
...

# Key Divergences
...

# Blind Spots
...

# New Information
...

# Applicability Boundaries

## Works when
...

## Does not work when
...

## Breaks when
...

# Impact on Original Hypothesis
...

# Validation Priorities
...
```

**Russian structure:**

```markdown
# Единое резюме гипотезы
...

# Подтверждённые сигналы
...

# Внутренние иллюзии
...

# Упущенные возможности
...

# Ловушки локальной оптимизации
...

# Ключевые дивергенции
...

# Слепые зоны
...

# Новая информация
...

# Границы применимости

## Работает когда
...

## Не работает когда
...

## Ломается когда
...

# Влияние на исходную гипотезу
...

# Приоритеты дальнейшей проверки
...
```

### File 2: `RUN_DIR/outputs/hypothesis_digest.txt`

Maximum 150 words.

**English structure:**

```text
Hypothesis: viable / risky / requires validation

Key conflict:
[X vs Y]

Primary illusion:
[...]

Primary blind spot:
[...]

Primary risk:
[...]

Primary insight:
[...]

Next step:
[what to do next]
```

**Russian structure:**

```text
Гипотеза: жизнеспособна / рискованна / требует проверки

Ключевой конфликт:
[X vs Y]

Главная иллюзия:
[...]

Главная слепая зона:
[...]

Основной риск:
[...]

Основной инсайт:
[...]

Следующий шаг:
[что делать дальше]
```

### File 3: `RUN_DIR/outputs/synthesis_complete.marker`

```text
Synthesis completed.
Roles analyzed.
Market analyzed.
Contradictions identified.
Applicability boundaries discovered.
Ready for Decision Review.
```

## Review rules

Never smooth contradictions.

Never prioritize consensus.

Never generate new market knowledge.

Never invent signals.

Never ignore conflicts.

Never summarize artifacts without comparison.

Always search for: contradictions, blind spots, reframing opportunities, applicability boundaries.

The goal is not to produce agreement.

The goal is to discover what becomes visible only after signal collision.

## Next step

After synthesis completes, run skill `hypothesis-decision-review` or workflow `/run-decision-review.md`.

## Reference

Based on `templates/synthesis-prompt.md` and `layers/synthesis-layer.md`.
