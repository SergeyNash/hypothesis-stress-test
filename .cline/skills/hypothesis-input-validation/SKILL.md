---
name: hypothesis-input-validation
description: Validate hypothesis input before running the stress-test framework. Use when starting a new hypothesis run, before Roles or Market layers, or when input quality is uncertain.
---

# Hypothesis Input Validation

Validate `RUN_DIR/input/hypothesis.md` before any layer executes.

## Read input

1. Locate `RUN_DIR` (ask user if not specified).
2. Read `RUN_DIR/input/hypothesis.md`.
3. Resolve RU/EN section and field aliases from `templates/input-schema.md`. Do
   not require all headings to use one language. Determine the dominant body
   language and use it for validation messages.

## Structured result

Always return this object in chat and to the calling workflow. This is a
workflow result, not a completion marker; do not create a marker file.

```yaml
validation: pass | fail
failed_checks:
  - code: STABLE_CODE
    field: canonical_field
    message: human-readable reason in input language
repair_hints:
  - targeted, actionable repair in input language
```

Use `failed_checks: []` and `repair_hints: []` on pass. A check has one stable
code even if the message is localized. Supported codes:

- `MISSING_SECTION`
- `INVALID_HYPOTHESIS_ID`
- `RUN_DIR_ID_MISMATCH`
- `INVALID_STATUS`
- `VAGUE_STATEMENT`
- `MISSING_ROLES`
- `TOO_MANY_ROLES`
- `MISSING_CONTEXT_FIELD`

Report every failure found in one pass; do not stop at the first error.

## Accepted aliases

- Sections: `Metadata` / `Метаданные`; `Statement` / `Формулировка`;
  `Relevant Roles` / `Релевантные роли` / `Затронутые роли`;
  `Research Context` / `Контекст исследования`.
- Metadata: `Hypothesis ID` / `ID гипотезы`; `Created at` /
  `Дата создания`; `Run ID` / `ID прогона`; `Status` / `Статус`.
- Context: `Domain` / `Домен`; `Target audience` / `Целевая аудитория`;
  `Scenario` / `Сценарий`; `Constraints` / `Ограничения`.

Duplicate canonical concepts under both aliases are ambiguous and fail as
`MISSING_SECTION` with a repair hint to keep one version.

## Required checks

### Metadata

- Hypothesis ID present and matches `HYP-YYYY-MM-DD-NNN` format?
- Created at date is present and matches `YYYY-MM-DD`?
- Run ID is present and matches `RUN-YYYY-MM-DD-NNN`?
- Status uses the stored enum `draft` | `running` | `completed` | `archived`?
- `RUN_DIR` basename MUST equal metadata Hypothesis ID.

Map failures to `MISSING_SECTION`, `INVALID_HYPOTHESIS_ID`,
`RUN_DIR_ID_MISMATCH`, or `INVALID_STATUS`. Missing metadata fields use
`MISSING_SECTION`.

Russian status values may be recognized for repair:
`черновик` → `draft`, `выполняется` / `в работе` → `running`,
`завершён` / `завершено` → `completed`, `архив` / `архивирован` →
`archived`. They are not canonical stored values: return `INVALID_STATUS` and
recommend the mapped token. Never normalize the file silently.

### Hypothesis statement

Apply this testability rubric:

1. **Change** — identifies the intervention, decision, or behavior that changes.
2. **Audience/context** — identifies who is affected or where it applies.
3. **Expected outcome** — states an observable consequence.
4. **Falsifiability** — there is evidence or a comparison that could disprove it.

Fail with `VAGUE_STATEMENT` when fewer than three dimensions are clear or the
statement is a generic goal such as “improve UX” / «улучшить опыт». `If…then`
and `Если…то` are recommended forms, not syntax requirements.

### Relevant roles

- Is at least one role defined?
- Are they real perspectives (not generic placeholders)?
- Are they directly impacted by the hypothesis?
- More than 5 roles fails with `TOO_MANY_ROLES` and asks the user to narrow or
  explicitly revise the scope. No roles fails with `MISSING_ROLES`.

### Research context

- Domain, Target audience, and Scenario are required and non-placeholder.
- Scenario must be concrete enough for market validation.
- Each absent or placeholder required field emits `MISSING_CONTEXT_FIELD` with
  its canonical `field`. Constraints are optional.

## If validation fails

Return `validation: fail`. Do NOT run any layer. Ask only questions associated
with the returned failures, for example:

- "Who is affected by this?"
- "In what context does this happen?"
- "What exactly changes?"

## If validation passes

Return `validation: pass`, then confirm readiness and list:

- Hypothesis ID and Run ID
- Hypothesis statement (one line)
- Roles selected
- Research context summary

Suggest next step: invoke `/run-hypothesis.md` workflow, or `/run-hypothesis-conversational.md` for a new chat-first run.

## Reference

See `templates/input-schema.md` and `playbooks/validate-input.md`.
