# 🧠 Hypothesis Stress Test

<p align="right">
  🌐 Language:
  <b>English</b> |
  <a href="./README.ru.md">Русский</a>
</p>

<p align="right">
  <sub>
    🌐 <b>Language:</b>
    <b>🇬🇧 English</b> ·
    <a href="./README.ru.md">🇷🇺 Русский</a>
  </sub>
</p>

# 🧠 Hypothesis Stress Test

<p align="center">
  <b>Challenge product hypotheses before you waste time building them.</b>
</p>

<p align="center">
  A lightweight, tool-agnostic framework for product decision-making with LLM.
</p>

<p align="center">
  <a href="./playbooks/run-hypothesis.md"><b>Start with the Playbook</b></a>
  ·
  <a href="./examples/example-001/"><b>View Example</b></a>
  ·
  <a href="./architecture/overview.md"><b>Architecture</b></a>
</p>

<p align="center">
  <img src="./assets/architecture-overview.svg" width="760"/>
</p>

<p align="center">
  <a href="./assets/architecture-overview.svg">Open architecture diagram</a>
</p>

---

## Why this exists

Most product teams don’t fail because they lack ideas.

They fail because they:

* validate ideas too late
* rely on intuition
* mix assumptions with reality
* avoid confronting contradictions

This framework helps answer one question early:

> **Should this idea exist at all?**

---

## The core idea

Do not ask an LLM to generate more ideas.

Use it to apply pressure to the ideas you already have.

```text
idea → stress test → decision
```

---

## How it works

The framework separates reasoning into three layers:

| Layer               | Purpose                     | Output                 |
| ------------------- | --------------------------- | ---------------------- |
| **Roles Layer**     | Tests internal perspectives | role-based constraints |
| **Market Layer**    | Checks external reality     | evidence-based signals |
| **Synthesis Layer** | Exposes contradictions      | decision boundaries    |

---

## Decision model

<p align="center">
  <img src="./assets/signal-model.svg" width="660"/>
</p>

<p align="center">
  <a href="./assets/signal-model.svg">Open signal model</a>
</p>

The system classifies a hypothesis into four decision patterns:

* **Validated Opportunity** — internal and external signals align
* **Internal Illusion** — internal logic looks strong, market signal is weak
* **Blind Spot** — market signal exists, internal model misses it
* **Weak Signal** — no strong evidence from either side

---

## Artifact flow

<p align="center">
  <img src="./assets/artifact-flow.svg" width="820"/>
</p>

<p align="center">
  <a href="./assets/artifact-flow.svg">Open artifact flow</a>
</p>

Every run creates a traceable decision trail:

```text
outputs/
  role_outputs/*
  hypothesis_summary.md
  market_analysis.md
  hypothesis_map.md
  hypothesis_digest.txt
```

---

## Who this is for

Primary user:

> **Product Manager**

This framework assumes that you:

* know your users
* have done interviews
* understand your domain
* have some internal or external knowledge to reason from

It does not replace discovery.

It amplifies it.

---

## Quick start

1. Define a hypothesis
2. Select relevant roles
3. Add research context
4. Run the layers
5. Read the synthesis

Start here:

```text
playbooks/run-hypothesis.md
```

---

## Example

See:

```text
examples/example-001/
```

The example shows a B2B hypothesis where the initial framing:

> “reduce production risk”

is reframed into:

> “improve operational efficiency”

That reframing is the point of the framework.

---

## Framework vs tooling

This is not a tool.

It is a framework.

```text
Framework → how to think
Tools     → how to run it
```

You can use:

* ChatGPT
* local LLMs
* APIs
* LLM-based IDE tools
* internal AI platforms

No specific setup is required.

---

## Repository structure

```text
layers/        reasoning model
templates/     execution templates
playbooks/     usage workflows
examples/      worked examples
architecture/  system design
assets/        diagrams
```

---

## Principles

* Separate internal and external signals
* No evidence → no claim
* Contradictions matter more than consensus
* Human makes the decision
* Bad ideas should die early

---

## What this is not

This is not:

* an idea generator
* a replacement for real users
* a market research substitute
* an autonomous decision-maker
* AI magic

---

## Use it when

Use this framework when:

* time is limited
* resources are limited
* the hypothesis sounds “obvious”
* the cost of building the wrong thing is high

---

<p align="center">
  <b>Stress-test the idea before you build it.</b>
</p>
