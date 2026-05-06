# Hypothesis Summary

## Statement

If Application Security engineers are able to manually prioritize projects in the SAST scanning queue, then business-critical applications will be scanned first, reducing the time required to detect high-risk vulnerabilities and lowering overall production risk.

## Core Idea

The hypothesis assumes that manual prioritization of scan queues by AppSec engineers will improve response time for critical systems and reduce business risk.

---

# Hidden Assumptions

* Current prioritization mechanisms are ineffective
* AppSec engineers have access to business-criticality context
* Earlier scanning directly reduces business risk
* Organizations are operationally mature enough for manual prioritization
* The process is scalable
* Manual prioritization will not create political or behavioral conflicts

---

# Role Summary

| Role | Pain Priority | Adoption Readiness |
|------|---------------|-------------------|
| AppSec Engineer | CRITICAL | Conditional |
| CISO | SECONDARY | Low |
| Enterprise Developer | SECONDARY | Low |
| Penetration Tester | DOES NOT ADDRESS PAIN | Neutral / Negative |

---

# Validation Recommendations

1. Interview AppSec engineers about current scan queue workflows
2. Evaluate operational maturity and business-context availability
3. Explore policy-driven automation alternatives
4. Define applicability boundaries for the feature