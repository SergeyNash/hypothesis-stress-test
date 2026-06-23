# Templates

This directory contains execution templates for running the framework manually.

Templates define **how each layer is invoked**, not how the model is configured.

For **Cline execution**, use skills in `.cline/skills/` instead — these templates are the source material for those skills.

---

## What are templates?

Templates are structured prompts used to execute each layer:

* Roles Layer
* Local Evidence Discovery
* Market Layer
* Synthesis Layer
* Customer Discovery Planning
* Decision Review

They act as an **interface between the user and the system**.

---

## Not system prompts

Templates are NOT full system prompts.

They provide:

* input structure
* task definition
* expected outputs

---

## How to use

### 1. Cline (recommended)

Use project skills and workflows:

```text
/run-hypothesis.md
```

Skills map from templates:

| Template | Skill |
|----------|-------|
| `facilitator-prompt.md` | `hypothesis-facilitator` |
| `knowledge-retrieval-prompt.md` | `local-knowledge-retrieval` |
| `market-prompt.md` | `hypothesis-market-layer` |
| `synthesis-prompt.md` | `hypothesis-synthesis` |
| `customer-discovery-planning-prompt.md` | `customer-discovery-planning` |
| `decision-review-prompt.md` | `hypothesis-decision-review` |
| `input-schema.md` | `hypothesis-input-validation` |

### 2. Direct usage (manual)

Copy the template, fill in hypothesis, roles, and context. Run as a standard prompt in any LLM.

### 3. Internal workflow

Follow steps manually without automation.

---

## What each template includes

* required inputs
* task description
* output expectations

---

## Relationship with other parts

* Playbook → describes the process
* Templates → manual execution
* Skills → Cline automated execution
* Layers → define reasoning logic

---

## Important

Templates assume:

* a clear hypothesis
* defined roles
* basic research context

If input is weak → output will be weak.

---

## Next

See:

* `facilitator-prompt.md`
* `knowledge-retrieval-prompt.md`
* `market-prompt.md`
* `synthesis-prompt.md`
* `customer-discovery-planning-prompt.md`
* `decision-review-prompt.md`
