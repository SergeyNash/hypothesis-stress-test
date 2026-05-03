# Roles Layer

The Roles Layer provides an **internal analysis** of a hypothesis.

It evaluates how the hypothesis behaves across **real user perspectives**, not abstract assumptions.

---

## 🧠 Purpose

The goal is not to validate the hypothesis.

The goal is to define:

> Where this hypothesis creates value — and where it breaks.

---

## ⚙️ What it does

The layer analyzes the hypothesis through a set of **relevant roles**.

Each role represents a real perspective, such as:

* user
* developer
* business
* operations

The exact roles depend on the hypothesis.

---

## 📚 Role Source

Roles are not invented during analysis.

They should come from **real user understanding**:

* interviews
* customer development
* product discovery
* domain expertise

In practice:

> A product manager is expected to already know their users.

This layer does not replace research — it uses it.

---

## 📁 Role Profiles

Each role should be described as a structured profile.

Example:

```text
Role: Developer

Context:
- works under deadlines
- values speed and predictability

Pain:
- interruptions in workflow
- unclear requirements

Behavior:
- prefers simple tools
- avoids unnecessary complexity
```

These profiles can be stored, reused, and improved over time.

---

## 🔍 Core Questions

For each role, the layer answers:

### 1. Pain Point

What real problem does this solve?

Classification:

* critical
* secondary
* none

---

### 2. New Problems

What new complexity does this introduce?

Focus on:

* operational friction
* process overhead
* unintended consequences

---

### 3. Alternatives

What would this role do instead?

Including:

* existing tools
* manual workarounds
* doing nothing

---

### 4. Failure Conditions

When does this become useless or harmful?

Examples:

* edge cases
* scale issues
* misalignment with workflows

---

## 🧠 How it thinks

The layer operates under strict constraints:

* no assumption of value
* no approval bias
* no generic statements

It assumes:

> Every hypothesis works only under specific conditions.

---

## ⚠️ What it does NOT do

* does not confirm the hypothesis
* does not consider market reality
* does not generate solutions
* does not replace user research

It only defines boundaries.

---

## 📦 Output

The Roles Layer produces:

* per-role analysis
* hypothesis summary
* list of hidden assumptions

---

## 🧩 Output semantics

The result is:

* an internal model of applicability
* a set of constraints
* a map of potential failure points

This is not truth.

This is a **structured internal signal**.

---

## ⚠️ Common mistakes

* including too many roles
* using vague or generic roles
* inventing roles instead of using real knowledge
* mixing roles with personas
* assuming all roles must agree

---

## 🔄 Relationship with other layers

* Market Layer → validates external reality
* Synthesis Layer → compares signals

Roles Layer alone is insufficient.

---

## 🧬 Key principle

> Internal logic is not reality.

The Roles Layer defines how the hypothesis *should* work —
not whether it actually does.

---

## 📘 Next

See:

* `market-layer.md`
* `synthesis-layer.md`

Roles can be stored as reusable profiles in /roles directory.