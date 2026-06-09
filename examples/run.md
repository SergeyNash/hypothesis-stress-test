Language: **English** | [Русский](./run.ru.md)

# Run

This file describes how the hypothesis was processed through the framework.

---

## Input

Hypothesis file:

```text
examples/example-001/hypothesis.md
```

---

## Execution Mode

**Primary:** Cline in VS Code with project rules, skills, and workflows.

```text
RUN_DIR: examples/example-001
/run-hypothesis.md
```

**Fallback:** manual execution using templates in any LLM interface.

---

## Prerequisites

1. Cline extension installed — [implementations/cline-setup.md](../implementations/cline-setup.md)
2. Confluence MCP configured (recommended) — [implementations/confluence-mcp.md](../implementations/confluence-mcp.md)
3. Input validated — `/validate-hypothesis-input.md`

---

## Step 1 — Roles Layer

**Cline skill:** `hypothesis-roles-layer`

**Manual template:** `templates/facilitator-prompt.md`

Input:

* hypothesis statement
* relevant roles
* scenario context

Expected output:

```text
outputs/role_outputs/
outputs/hypothesis_summary.md
outputs/ready_for_synthesis.marker
```

Purpose:

* identify role-specific value
* reveal hidden assumptions
* detect internal friction
* define failure conditions

---

## Step 2 — Market Layer

**Cline skill:** `hypothesis-market-layer`

**Manual template:** `templates/market-prompt.md`

**Confluence first:** search Confluence MCP for local signals before external sources.

Input:

* hypothesis statement
* research context
* domain and product type

Expected output:

```text
outputs/market_analysis.md
outputs/market_analysis_complete.marker
```

Purpose:

* validate whether the problem exists externally
* retrieve local signals from Confluence
* identify current solution patterns
* classify signal strength

---

## Step 3 — Synthesis Layer

**Cline skill:** `hypothesis-synthesis-layer`

**Manual template:** `templates/synthesis-prompt.md`

Input:

* role outputs
* hypothesis summary
* market analysis

Expected output:

```text
outputs/hypothesis_map.md
outputs/hypothesis_digest.txt
outputs/synthesis_complete.marker
```

Purpose:

* compare internal and external signals
* identify contradictions
* classify the hypothesis
* make decision boundaries visible

---

## Step 4 — Decision Review

**Cline skill:** `hypothesis-decision-review`

**Manual template:** `templates/decision-review-prompt.md`

Input:

* synthesis outputs and prior artifacts

Expected output:

```text
outputs/decision_review.md
outputs/decision_review_complete.marker
```

Purpose:

* challenge synthesis conclusions
* identify weak evidence and hidden assumptions
* propose cheapest validation path

---

## Expected Result

```text
examples/example-001/
  hypothesis.md
  run.md
  outputs/
    role_outputs/
    hypothesis_summary.md
    market_analysis.md
    hypothesis_map.md
    hypothesis_digest.txt
    decision_review.md
    *.marker
```

---

## Notes

This example uses a domain-specific B2B AppSec hypothesis.

The framework itself is domain-agnostic.

Canonical outputs in `examples/example-001/outputs/` were produced by the framework layers and serve as reference artifacts.
