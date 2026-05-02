# Run Hypothesis

This playbook describes how to validate a product hypothesis using the framework.

The process is manual, fast, and reproducible.

---

## 🧠 Goal

Determine whether a hypothesis:

* creates real value
* survives external validation
* or should be discarded early

---

## 🧩 Step 0 — Define Hypothesis

Write a clear, testable statement.

Additionally, define:

1. **Relevant roles** (for internal analysis)
2. **Research context** (for market validation)

---

### Hypothesis

Good:

> Users need a way to prioritize notifications based on context

Bad:

> Improve user experience

---

### Relevant Roles

Select only roles that are directly impacted.

Example:

* end-user
* developer
* product manager

---

### Research Context (for Market Layer)

Provide minimal context for external validation:

* domain / product type
* target audience
* usage scenario
* constraints (if any)

---

### Example

Domain:

* productivity tools

Audience:

* knowledge workers

Scenario:

* managing notifications during work

---

### Why this matters

Roles Layer:

* prevents noise from irrelevant perspectives

Market Layer:

* anchors research in a real context
* avoids generic conclusions

---

### Anti-patterns

❌ Include too many roles
❌ Skip role selection
❌ Provide no research context
❌ Use vague or abstract hypotheses

---

### Output of this step

You should have:

* a clear hypothesis
* a defined set of relevant roles
* a minimal research context

---

## ⚙️ Step 1 — Run Roles Layer

Use the facilitator prompt.

Input:

* hypothesis
* selected roles

Output:

* role_outputs/*
* hypothesis_summary.md

Goal:

* identify hidden assumptions
* understand internal value boundaries
* detect friction and rejection conditions

---

## 🌍 Step 2 — Run Market Layer

Use the market prompt.

Input:

* hypothesis
* research context

Output:

* market_analysis.md

Goal:

* validate problem existence
* identify real users
* detect existing solutions
* measure signal strength

Rules:

* no evidence → no claim
* sources must be explicit
* distinguish facts from assumptions

---

## ⚡ Step 3 — Run Synthesis Layer

Use the synthesis prompt.

Input:

* outputs from previous steps

Output:

* hypothesis_map.md
* hypothesis_digest.txt

Goal:

* compare internal vs external signals
* identify contradictions
* classify hypothesis

---

## 🧠 Interpretation Model

The result falls into one of four categories:

### ✅ Validated Opportunity

Internal and external signals align.

→ Proceed with development

---

### ❌ Internal Illusion

Internal logic supports it, market does not.

→ Do NOT build

---

### ⚠️ Blind Spot

Market shows signal, internal model does not.

→ Investigate deeper

---

### 🟡 Weak Signal

No strong evidence anywhere.

→ Low priority

---

## 📦 Output Structure

Each run creates:

RUN_DIR/
outputs/
role_outputs/
hypothesis_summary.md
market_analysis.md
hypothesis_map.md

---

## ⏱ Expected Time

Typical run:

* 5–15 minutes per hypothesis

---

## 💡 Tips

* keep hypotheses narrow
* define roles explicitly
* provide minimal but concrete context
* don’t skip synthesis

---

## ⚠️ Common Mistakes

* using LLM to confirm ideas
* ignoring missing evidence
* mixing layers prematurely
* overcomplicating hypotheses

---

## 🧬 Principle

This is not about generating ideas.

It is about deciding:

> should this idea exist at all
