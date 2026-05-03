# Implementations

This framework is tool-agnostic.

It describes **how to structure reasoning**, not which tool to use.

---

## 🧠 Framework vs Tooling

The framework defines:

* layers
* inputs
* outputs
* reasoning contracts
* decision logic

Tooling defines:

* where prompts are executed
* where files are stored
* how artifacts are passed between steps
* whether execution is manual or automated

---

## ✅ Recommended Mental Model

```text
Framework = how to think
Implementation = how to run it
```

Do not confuse the two.

---

## 🔧 Possible Implementations

The framework can be implemented using:

* ChatGPT or similar chat interfaces
* local LLMs
* LLM-based IDE tools
* API workflows
* custom scripts
* internal AI platforms

No specific tool is required.

---

## 🧩 Manual Implementation

The simplest implementation is fully manual:

1. Copy the template for a layer
2. Insert hypothesis and context
3. Run it in an LLM interface
4. Save the output artifact
5. Move to the next layer

This is enough for early adoption.

---

## 🧱 Local LLM Implementation

A local implementation can use:

* local or internal LLM API
* local knowledge base
* vector search
* filesystem-based artifacts

This is useful when:

* data must stay inside the organization
* hypotheses contain sensitive information
* external AI tools are not allowed

## 🔗 Knowledge Integration (MCP / Internal Systems)

The framework becomes significantly more effective when connected to internal knowledge sources.

This can be achieved using tools like MCP (Model Context Protocol) to access systems such as:

* Confluence (wiki)
* internal documentation
* knowledge bases
* research repositories

---

### Why this matters

Internal systems often contain:

* real user problems
* past decisions
* architectural constraints
* historical context

This information is more reliable than generic external sources.

---

### Example Usage

Market Layer can use internal knowledge to:

* validate whether a problem has already been observed
* identify recurring issues
* extract patterns from past discussions
* understand domain-specific constraints

---

### Signal Quality Impact

```text
Without internal knowledge:
→ generic market assumptions

With internal knowledge:
→ context-aware, high-confidence signals
```

---

### Important

* internal data must still follow evidence rules
* assumptions must be separated from documented facts
* outdated information must be treated carefully

---

### Key Principle

> The best market signal is often already inside the organization.

External research complements it — not replaces it.


---

## 🛠 LLM-based IDE Tool Implementation

The framework can also be implemented inside LLM-enabled development environments.

In this setup:

* templates can be adapted into system prompts
* each layer can be represented as a separate configured mode/tool
* outputs can be written into local files
* `RUN_DIR` can be used as the execution workspace

Example mapping:

```text
Template          → system prompt or reusable command
RUN_DIR           → local workspace for one run
Layer output      → markdown artifact
Synthesis input   → artifacts from previous layers
```

This approach is useful when the user wants:

* local execution
* editable prompts
* file-based workflow
* manual control over each step

---

## 🔄 API-based Implementation

An API implementation can execute each layer through programmatic LLM calls.

Typical flow:

```text
hypothesis
  → roles layer call
  → market layer call
  → synthesis layer call
  → final artifact
```

This can be implemented using:

* Python scripts
* internal services
* workflow tools
* CI-like pipelines

This is useful when repeated execution becomes frequent.

---

## ⚠️ What NOT to do

Do not make the framework dependent on a specific tool.

Avoid:

* hardcoding one IDE
* requiring one LLM provider
* assuming orchestration is mandatory
* hiding reasoning inside automation

The value of the framework is in the reasoning structure.

---

## 🚀 Implementation Maturity

### Level 1 — Manual

* copy templates
* run manually
* save artifacts

Best for:

* first experiments
* individual use
* low-frequency analysis

---

### Level 2 — Assisted

* predefined prompts
* local file structure
* reusable workspaces

Best for:

* regular use
* repeatable analysis
* small teams

---

### Level 3 — Automated

* API calls
* workflow orchestration
* artifact validation
* reusable runs

Best for:

* high-frequency analysis
* team workflows
* internal platforms

---

## 🧬 Key Principle

Implementation should not change the reasoning model.

Tools may vary.

The layers stay the same.
