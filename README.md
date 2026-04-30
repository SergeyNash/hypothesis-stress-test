# Hypothesis Stress Test

A lightweight, local-first framework for validating product hypotheses using LLM.

This system does **not generate ideas**.
It **stress-tests them**.

---

## 🧠 What is this?

This repository describes a practical approach to **product decision-making under uncertainty**.

Instead of relying on:

* intuition
* fragmented research
* or internal consensus

the system separates different types of signals and **forces them into conflict**:

* internal perspectives
* external reality
* synthesis through contradictions

> Truth emerges not from agreement, but from tension between viewpoints.

---

## ⚙️ Core Concept

The framework is built around three independent layers:

### 1. Roles Layer (Internal)

Analyzes how the hypothesis behaves across different perspectives:

* user
* developer
* business
* operations

Focus:

* value boundaries
* hidden assumptions
* internal friction

---

### 2. Market Layer (External)

Validates whether the problem exists outside your head.

Uses:

* local knowledge base
* vector search
* external sources (with explicit references)

Focus:

* real demand
* existing solutions
* signal strength

---

### 3. Synthesis Layer (Conflict)

Compares internal and external signals.

Outputs:

* validated opportunities
* internal illusions
* blind spots
* weak signals

This is where decisions become clear.

---

## 🔄 How it works

The system is executed manually in three steps:

```text
1. Define hypothesis
2. Run Roles Layer
3. Run Market Layer
4. Run Synthesis Layer
```

Each layer produces structured artifacts.
The next layer consumes them.

No orchestration required.

---

## 📦 Output Model

Each run produces a directory:

```text
RUN_DIR/
  outputs/
    role_outputs/
    hypothesis_summary.md
    market_analysis.md
    hypothesis_map.md
```

These artifacts form a complete decision trace.

---

## 🧩 Why this approach

Most hypothesis validation fails because signals are mixed too early.

This framework enforces:

* separation of perspectives
* explicit assumptions
* evidence-based validation
* conflict-driven synthesis

It turns vague thinking into a **reproducible process**.

---

## 🚀 What you get

* faster hypothesis validation
* lower cost of mistakes
* clearer decision-making
* reusable reasoning structure

In practice:
bad ideas die early.

---

## 🏗 Architecture

* local LLM (via API)
* local knowledge base (Obsidian)
* vector search for retrieval
* optional web search with sources
* manual execution (human-in-the-loop)

No external dependencies required.

Works in closed environments.

---

## ⚠️ Limitations

This is not:

* a replacement for real users
* an autonomous system
* a generator of new ideas

Quality depends on:

* hypothesis clarity
* role definitions
* knowledge base quality

---

## 📘 Playbook

See `/playbooks/run-hypothesis.md` for step-by-step usage.

---

## 🧬 Philosophy

LLM is not used as an assistant.

It is used as a **pressure tool**.

The goal is not to confirm an idea —
but to determine whether it survives reality.

---

## 🪪 License

MIT (or choose your own)
