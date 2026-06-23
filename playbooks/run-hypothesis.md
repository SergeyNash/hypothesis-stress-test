Language: **English** | [Русский](./run-hypothesis.ru.md)

# Run Hypothesis

This playbook describes how to validate a product hypothesis using the framework.

**Primary method:** Cline in VS Code with skills and workflows.
**Fallback:** manual template execution in any LLM.

---

## Cline quick path

### Chat-first (recommended)

1. Install Cline — see [implementations/cline-setup.md](../implementations/cline-setup.md)
2. Configure Confluence MCP — see [implementations/confluence-mcp.md](../implementations/confluence-mcp.md)
3. In Cline chat:

```text
/run-hypothesis-conversational.md

Describe your hypothesis in natural language.
```

**Intake tags:** `#hypothesis`, `#context`, `#roles`, `#new-run`.  
**Two-step confirm:** draft card → proposed `RUN_DIR` (e.g. `002` if `001` exists). See [examples/chat-first-run.md](../examples/chat-first-run.md).

The agent collects input, shows draft, proposes new `RUN_DIR` in dialog, creates folder only after confirm, validates, and runs the pipeline.

### File-first (fallback)

1. Create `RUN_DIR/input/hypothesis.md` — see [templates/input-schema.md](../templates/input-schema.md)
2. In Cline chat:

```text
RUN_DIR: runs/HYP-2026-06-22-001
/run-hypothesis.md
```

Or step by step:

```text
/validate-hypothesis-input.md
```

Then individual layer workflows as needed.

---

## Goal

Determine whether a hypothesis:

* creates real value
* survives external validation
* or should be discarded early

---

## Step 0 — Define Hypothesis

Write a clear, testable statement in `RUN_DIR/input/hypothesis.md`.

Additionally, define:

1. **Relevant roles** (for internal analysis)
2. **Research context** (for market validation)

See [templates/input-schema.md](../templates/input-schema.md).

### Hypothesis

Good:

> Users need a way to prioritize notifications based on context

Bad:

> Improve user experience

### Relevant Roles

Select only roles that are directly impacted.

### Research Context

* domain / product type
* target audience
* usage scenario
* constraints (optional)

Validate input before proceeding — skill `hypothesis-input-validation` or `/validate-hypothesis-input.md`.

---

## Step 1 — Run Facilitator (Roles Layer / Hypothesis Stress Test)

**Cline:** skill `hypothesis-facilitator` or `/run-facilitator.md` or included in `/run-hypothesis.md`

**Manual:** [templates/facilitator-prompt.md](../templates/facilitator-prompt.md)

This phase does **not**: make decisions, research the market, synthesize conclusions, or design experiments.

Input:

* hypothesis
* selected roles

Output:

* `role_outputs/*`
* `hypothesis_summary.md`
* `validation_questions.md`
* `ready_for_synthesis.marker`

Goal:

* expose hidden assumptions and applicability boundaries
* show role conflicts
* generate behavior-based validation questions
* discover where the hypothesis breaks

Output language matches `input/hypothesis.md`.

---

## Step 2 — Run Local Evidence Discovery

**Cline:** skill `local-knowledge-retrieval` or `/run-knowledge-retrieval.md`

**Manual:** [templates/knowledge-retrieval-prompt.md](../templates/knowledge-retrieval-prompt.md)

Output:

* `discovery_preview.md`
* `evidence_inventory.md`
* `knowledge_retrieval_complete.marker`

Rules:

* one evidence item = one atomic signal
* no synthesis in retrieval step
* preview is always generated, extraction auto-continues in V1

---

## Step 3 — Run Market Layer (Market Reality Check)

**Cline:** skill `hypothesis-market-layer` or `/run-market-layer.md`

**Manual:** [templates/market-prompt.md](../templates/market-prompt.md)

**Inventory first:** use `evidence_inventory.md` from Local Evidence Discovery, then search Confluence MCP for additional internal signals.

Input:

* hypothesis
* research context

Output:

* `market_analysis.md`
* `market_analysis_complete.marker`

Rules:

* no evidence → no claim
* sources must be explicit
* distinguish facts from assumptions
* keep channels separated: KB / Confluence / external / inferred

---

## Step 4 — Run Synthesis Layer

**Cline:** skill `hypothesis-synthesis` or `/run-synthesis.md`

**Manual:** [templates/synthesis-prompt.md](../templates/synthesis-prompt.md)

This phase does **not**: summarize without comparison, add market/role signals, or make final decisions.

Prerequisites: `ready_for_synthesis.marker` + `market_analysis_complete.marker`

Input:

* `role_outputs/*`, `hypothesis_summary.md`, `market_analysis.md`
* optional: `validation_questions.md`

Output:

* `hypothesis_map.md`
* `hypothesis_digest.txt` (max 150 words)
* `synthesis_complete.marker`

Goal:

* collide internal vs external signals
* discover contradictions, blind spots, local optimization traps
* surface new information visible only after comparison
* determine impact on original hypothesis framing

---

## Step 5 — Run Customer Discovery Planning

**Cline:** skill `customer-discovery-planning` or `/run-customer-discovery-planning.md`

**Manual:** [templates/customer-discovery-planning-prompt.md](../templates/customer-discovery-planning-prompt.md)

This phase does **not**: validate hypotheses, make product decisions, or recommend implementation.

Input:

* synthesis outputs and prior artifacts

Output:

* `customer_discovery_plan.md`
* `customer_discovery_planning_complete.marker`

Goal:

* extract critical unknowns and unvalidated assumptions
* identify missing evidence and required customer conversations
* produce a practical interview guide and participant plan

---

## Step 6 — Run Decision Review

**Cline:** skill `hypothesis-decision-review` or `/run-decision-review.md`

**Manual:** [templates/decision-review-prompt.md](../templates/decision-review-prompt.md)

Input:

* synthesis outputs and prior artifacts

Output:

* `decision_review.md`
* `decision_review_complete.marker`

Goal:

* challenge synthesis conclusions
* identify weak evidence and hidden assumptions
* propose cheapest validation path

Do not skip this step. Decision Review does not repeat synthesis — it adds adversarial critique.

---

## Step 7 — Backlog Decision (Human)

Review `decision_review.md` and make the final backlog decision:

* Proceed
* Proceed with Validation
* Additional Research Required
* Reject

---

## Interpretation Model

### Validated Opportunity

Internal and external signals align. → Proceed with development

### Internal Illusion

Internal logic supports it, market does not. → Do NOT build

### Blind Spot

Market shows signal, internal model does not. → Investigate deeper

### Weak Signal

No strong evidence anywhere. → Low priority

### Local Optimization Trap

Roles and market confirm pain, but solving it does not create strategic business value. → Reframe or narrow scope

---

## Output Structure

```text
RUN_DIR/
  input/
    hypothesis.md
  outputs/
    role_outputs/
    hypothesis_summary.md
    validation_questions.md
    market_analysis.md
    hypothesis_map.md
    hypothesis_digest.txt
    customer_discovery_plan.md
    decision_review.md
```

---

## Expected Time

5–15 minutes per hypothesis (Cline assisted).

---

## Tips

* keep hypotheses narrow
* define roles explicitly
* configure Confluence MCP for better local signals
* don't skip customer discovery planning or decision review

---

## Principle

This is not about generating ideas.

It is about deciding:

> should this idea exist at all
