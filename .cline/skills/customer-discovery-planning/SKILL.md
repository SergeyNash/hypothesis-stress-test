---
name: customer-discovery-planning
description: Transform unresolved assumptions, weak signals, contradictions, and uncertainty into a practical customer research and interview plan.
---

# Customer Discovery Planning

## Purpose

The purpose of this skill is NOT to validate a hypothesis.

The purpose is NOT to make a product decision.

The purpose is to determine:

- what remains unknown;
- what assumptions require validation;
- what evidence is missing;
- which customer conversations should happen next.

This skill converts analytical uncertainty into a structured customer discovery plan.

## What this skill does NOT do

- Does not validate hypotheses
- Does not make backlog or product decisions
- Does not recommend implementation
- Does not ask opinion-based feature questions

## Inputs

Required:

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/hypothesis_summary.md`
- `RUN_DIR/outputs/market_analysis.md`
- `RUN_DIR/outputs/hypothesis_map.md`

Optional:

- `RUN_DIR/outputs/decision_review.md`
- `RUN_DIR/outputs/validation_questions.md`
- `RUN_DIR/outputs/role_outputs/*`

## Working directory

The user provides `RUN_DIR`.

All files MUST be read from and written to `RUN_DIR/outputs/`.

Never write files outside this directory.

## Output language

Write all artifact headings and body text in the **same language as `input/hypothesis.md`**.

- English hypothesis -> English outputs
- Russian hypothesis -> Russian outputs

## Start conditions

Run only after:

- `RUN_DIR/outputs/synthesis_complete.marker`

exists.

If synthesis is incomplete:

- stop execution;
- report missing dependencies.

## Core principle

The goal is not:

"What should we build?"

The goal is:

"What must we learn before deciding what to build?"

## Research philosophy

Never ask customers:

- Would you use this?
- Do you need this feature?
- Would you buy this?
- Is this useful?

These questions generate opinions.

Research must focus on:

- behavior;
- workflows;
- recent experience;
- real decisions;
- operational constraints.

The objective is evidence, not opinions.

## Analysis process

### Step 1 — Extract unknowns

Review all available artifacts.

Identify:

- assumptions without evidence;
- weak signals;
- unresolved contradictions;
- missing perspectives;
- unsupported conclusions.

Create a list of:

`Critical Unknowns`

### Step 2 — Classify uncertainty

Assign every unknown to one category.

#### Problem Risk

Does the problem actually exist?

#### Frequency Risk

How often does it occur?

#### Severity Risk

How painful is it?

#### Workflow Risk

How do users solve it today?

#### Adoption Risk

Will users change behavior?

#### Buyer Risk

Does the buyer care?

#### Business Value Risk

Can solving this create meaningful business value?

#### Strategic Fit Risk

Does solving this support strategic goals?

### Step 3 — Define research objectives

Convert uncertainty into research goals.

Bad:

`Validate hypothesis`

Good:

`Understand whether queue prioritization is a frequent operational problem for large AppSec teams.`

Every objective must:

- reduce uncertainty;
- produce actionable evidence;
- influence future decisions.

### Step 4 — Identify interview participants

Determine who can provide evidence.

Examples:

- AppSec Engineer
- Security Team Lead
- CISO
- Developer
- DevOps Engineer
- Product Owner
- Security Manager
- Platform Owner

For each role explain:

- why they should be interviewed;
- what evidence they can provide.

### Step 5 — Build interview guide

For every research objective create interview blocks.

#### Current Workflow

Understand how things work today.

#### Recent Experience

Discuss recent examples.

#### Consequences

Explore impact and outcomes.

#### Alternatives

Discover existing solutions.

#### Decision-Making Process

Understand who influences decisions.

### Step 6 — Prioritize research

Determine priority:

- HIGH — blocks decision making
- MEDIUM — improves confidence
- LOW — nice to know

Prioritization must reflect:

- business impact;
- decision impact;
- uncertainty level.

### Step 7 — Expected learning outcomes

For every research objective define:

`What exactly will we learn?`

Bad:

`Better understand users`

Good:

`Determine whether queue management issues occur weekly or only during incidents.`

## Output artifacts

### File 1: `RUN_DIR/outputs/customer_discovery_plan.md`

**English structure:**

```markdown
# Customer Discovery Plan

## Research Objective
...

---

## What We Already Know
...

---

## Critical Unknowns
| Unknown | Risk Type | Priority |
|----------|------------|----------|

---

## Recommended Interview Roles
...

---

## Interview Guide

### Current Workflow
...

### Recent Experience
...

### Consequences
...

### Alternatives
...

### Decision-Making Process
...

---

## Research Priorities

### High Priority
...

### Medium Priority
...

### Low Priority
...

---

## Expected Learning Outcomes
...
```

**Russian structure:**

```markdown
# План Customer Discovery

## Цель исследования
...

---

## Что уже известно
...

---

## Критические неизвестные
| Неизвестность | Тип риска | Приоритет |
|---------------|-----------|-----------|

---

## Рекомендуемые роли для интервью
...

---

## Гайд для интервью

### Текущий процесс
...

### Последний опыт
...

### Последствия
...

### Альтернативы
...

### Процесс принятия решений
...

---

## Приоритеты исследования

### Высокий приоритет
...

### Средний приоритет
...

### Низкий приоритет
...

---

## Ожидаемые результаты обучения
...
```

### File 2: `RUN_DIR/outputs/customer_discovery_planning_complete.marker`

```text
Customer Discovery Planning completed.
Critical unknowns identified.
Interview plan prepared.
Ready for Decision Review.
```

## Review rules

Never ask opinion-based questions.

Never ask feature-based questions.

Never ask customers to design solutions.

Always investigate:

- behavior;
- workflows;
- decisions;
- constraints;
- real events.

The purpose is not to validate the solution.

The purpose is to reduce uncertainty before decisions.

## Next step

After planning completes, run skill `hypothesis-decision-review` or workflow `/run-decision-review.md`.
