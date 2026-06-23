Language: **English** | [Русский](./validate-input.ru.md)

# Validate Input

Before running the system, validate the hypothesis input.

**Cline:** `/validate-hypothesis-input.md` or skill `hypothesis-input-validation`

**Chat-first:** if input is collected via `/run-hypothesis-conversational.md`, validation runs automatically after bootstrap. On failure, skill `conversational-hypothesis-intake` repairs the draft before re-validation.

---

## Checks

### 1. Hypothesis

* Is it specific?
* Is it testable?

---

### 2. Roles

* Are roles defined?
* Are they real (not generic)?
* Are they relevant?

---

### 3. Research Context

* Is domain defined?
* Is audience defined?
* Is scenario concrete?

---

## If missing

Do NOT run the system.

Instead, ask:

* “Who is affected by this?”
* “In what context does this happen?”
* “What exactly changes?”

---

## Principle

Bad input is not processed.

It is refined.
