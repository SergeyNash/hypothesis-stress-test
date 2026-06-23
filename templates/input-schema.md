# Input Schema

A minimal hypothesis input must include:

## Required

### Metadata

- **Hypothesis ID** — stable identifier, format `HYP-YYYY-MM-DD-NNN`
- **Created at** — date the run archive was created (`YYYY-MM-DD`)
- **Run ID** — identifier for this execution, format `RUN-YYYY-MM-DD-NNN`
- **Status** — `draft` | `running` | `completed` | `archived`

---

### Hypothesis

A clear, testable statement.

---

### Relevant Roles

Only roles directly impacted.

---

### Research Context

- Domain
- Target audience
- Scenario

---

## Optional

- Constraints
- Known assumptions
- Owner

---

## Example

```markdown
# Hypothesis

## Metadata

- Hypothesis ID: HYP-2026-06-22-001
- Created at: 2026-06-22
- Run ID: RUN-2026-06-22-001
- Status: draft

## Statement

If Application Security engineers are able to manually prioritize projects in the SAST scanning queue, then business-critical applications will be scanned first, reducing the time required to detect high-risk vulnerabilities.

## Relevant Roles

* AppSec Engineer
* CISO

## Research Context

* Domain: Application Security
* Target audience: Security teams in mid-to-large enterprises
* Scenario: Queue-based SAST scan execution with competing project priorities
```

---

## Archive location

Store the input file at:

```text
RUN_DIR/input/hypothesis.md
```

Where `RUN_DIR` is the hypothesis run archive, e.g. `runs/HYP-2026-06-22-001/`.

**Chat-first:** use `/run-hypothesis-conversational.md` — the workflow creates `RUN_DIR` and writes this file after user confirms the draft. Use `#hypothesis` for ready If…then statements or `#context` for dirty discovery notes. See [examples/chat-first-run.md](../examples/chat-first-run.md).

**File-first:** create `RUN_DIR` and `input/hypothesis.md` manually before `/run-hypothesis.md`.

---

## Principle

Weak input → weak output
