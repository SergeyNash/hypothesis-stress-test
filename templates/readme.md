# Templates

This directory contains execution templates for running the framework.

Templates define **how each layer is invoked**, not how the model is configured.

---

## 🧠 What are templates?

Templates are structured prompts used to execute each layer:

* Roles Layer
* Market Layer
* Synthesis Layer

They act as an **interface between the user and the system**.

---

## ⚠️ Not system prompts

Templates are NOT full system prompts.

They do not define:

* model behavior
* internal rules
* full constraints

Instead, they provide:

* input structure
* task definition
* expected outputs

---

## ⚙️ How to use

Templates can be used in different ways:

### 1. Direct usage

Copy the template, fill in:

* hypothesis
* roles
* context

Run it as a standard prompt.

---

### 2. System prompt (advanced)

Adapt the template into a system prompt:

* extend with rules
* add file outputs
* integrate into tools (e.g. RooCode)

---

### 3. Internal workflow

Use templates as a thinking structure:

* follow steps manually
* no automation required

---

## 🔄 Why this design

Templates are intentionally minimal.

They allow:

* portability across tools
* flexibility of implementation
* gradual adoption

The framework defines **what to do**,
templates define **how to start**.

---

## 📦 What each template includes

Each template defines:

* required inputs
* task description
* output expectations

---

## 🧬 Relationship with other parts

* Playbook → describes the process
* Templates → execute each step
* Layers → define reasoning logic

---

## ⚠️ Important

Templates assume:

* a clear hypothesis
* defined roles
* basic research context

If input is weak → output will be weak.

---

## 📘 Next

See:

* `facilitator-prompt.md`
* `market-prompt.md`
* `synthesis-prompt.md`
