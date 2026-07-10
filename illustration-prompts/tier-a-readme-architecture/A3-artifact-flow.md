# A3 Artifact flow

## Meta

| Поле | Значение |
|------|----------|
| Target output EN | `assets/en/artifact-flow.svg` |
| Target output RU | `assets/ru/artifact-flow.svg` |
| Canvas | 1480×800 |
| Tier | A |
| Replaces | `assets/artifact-flow.svg` |

## Purpose

Показать как `hypothesis.md` превращается в цепочку файлов RUN_DIR через фазы pipeline, включая business context и human report.

## Audience and context

- README — Artifact flow section
- `architecture/diagram.md`

## Composition

### Layout

Left: input file. Then vertical or horizontal swimlanes by phase color. Each lane contains output files. Markers as small green pills (`*_complete.marker`).

### Phases and files

| Phase color | Files |
|-------------|-------|
| Input amber | `hypothesis.md` |
| Roles blue | `role_outputs/*`, `hypothesis_summary.md`, `validation_questions.md`, `ready_for_synthesis.marker` |
| Evidence sky | `discovery_preview.md`, `evidence_inventory.md` |
| Business pink | `business_context_analysis.md` OR `missing_business_context.md` |
| Market green | `market_analysis.md` |
| Synthesis purple | `hypothesis_map.md`, `hypothesis_digest.txt` |
| Discovery yellow | `customer_discovery_plan.md` |
| Review rose | `decision_review.md` |
| Human red | `human_report.html` |

### Title

- EN: **Artifact flow**
- RU: **Поток артефактов**

## Labels EN

Phase labels: Input · Roles · Evidence · Business · Market · Synthesis · Discovery · Review · Report

## Labels RU

Вход · Роли · Доказательства · Бизнес · Рынок · Синтез · CustDev · Обзор · Отчёт

## Generation prompt (copy-paste)

```
Flat technical diagram "Artifact flow", 1480x800, white background, conference-minimal.

Title top-left "Artifact flow", subtitle "Structured files through sequential phases".

Start left: amber box "hypothesis.md".

Flow right through colored phase containers (swimlanes or grouped boxes):

ROLES (blue): role_outputs/*, hypothesis_summary.md, validation_questions.md
EVIDENCE (sky): discovery_preview.md, evidence_inventory.md  
BUSINESS (pink): business_context_analysis.md
MARKET (green): market_analysis.md
SYNTHESIS (purple): hypothesis_map.md, hypothesis_digest.txt
DISCOVERY (yellow): customer_discovery_plan.md
REVIEW (rose): decision_review.md
REPORT (light rose): human_report.html

Use 2px gray arrows between phases. Optional small green pills labeled "marker" on phase completion.

File names in monospace or pill style. No gradients. Colors per semantic layer palette. Sans-serif.
```

### Russian variant note

```
Title "Поток артефактов", subtitle "Структурированные файлы через последовательные фазы". Phase labels in Russian as listed. File names stay English (repo convention).
```

## Post-generation checklist

- [ ] business_context_analysis.md included
- [ ] human_report.html at end
- [ ] No fictional files (e.g. product_specification.md)
