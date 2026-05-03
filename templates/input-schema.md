# Input Schema

A minimal hypothesis input must include:

## Required

### Hypothesis

A clear, testable statement.

---

### Relevant Roles

Only roles directly impacted.

---

### Research Context

* Domain
* Target audience
* Scenario

---

## Optional

* Constraints
* Known assumptions

---

## Example

```yaml
hypothesis: >
  Allowing application security engineers to prioritize SAST scans
  reduces time to detect critical vulnerabilities

roles:
  - AppSec Engineer
  - CISO

context:
  domain: Application Security
  audience: Security teams
  scenario: Queue-based scan execution
```

---

## Principle

Weak input → weak output
