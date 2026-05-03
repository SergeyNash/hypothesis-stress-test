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

This example is tool-agnostic.

It can be executed using:

- ChatGPT
- local LLM
- LLM-based tools
- API-based workflow
- any other LLM environment

The framework does not require a specific tool.

---

## Step 1 — Roles Layer

Template used:

```text
templates/facilitator-prompt.md
```

Input:

* hypothesis statement
* relevant roles
* scenario context

Expected output:

```text
outputs/role_outputs/
outputs/hypothesis_summary.md
```

Purpose:

* identify role-specific value
* reveal hidden assumptions
* detect internal friction
* define failure conditions

---

## Step 2 — Market Layer

Template used:

```text
templates/market-prompt.md
```

Input:

* hypothesis statement
* research context
* domain and product type

Expected output:

```text
outputs/market_analysis.md
```

Purpose:

* validate whether the problem exists externally
* identify current solution patterns
* detect weak or missing market signals
* classify signal strength

---

## Step 3 — Synthesis Layer

Template used:

```text
templates/synthesis-prompt.md
```

Input:

* role outputs
* hypothesis summary
* market analysis

Expected output:

```text
outputs/hypothesis_map.md
outputs/hypothesis_digest.txt
```

Purpose:

* compare internal and external signals
* identify contradictions
* classify the hypothesis
* make decision boundaries visible

---

## Expected Result

After all layers are completed, the example should contain:

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
```

---

## Notes

This example intentionally uses a domain-specific B2B hypothesis.

The framework itself is domain-agnostic.
