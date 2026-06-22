# Customer Discovery Plan

## Research Objective

Reduce decision uncertainty before backlog commitment by confirming whether scan queue prioritization is primarily an operational efficiency problem, and by validating governance, adoption, and buyer constraints for AppSec teams.

---

## What We Already Know

- Queue overload is a real and recurring operational pain for AppSec teams.
- Current hypothesis framing ("reduce production risk") is weakly supported by evidence.
- Signal collision suggests reframing toward efficiency and time-to-action.
- Governance tension exists between AppSec manual control and CISO policy consistency.

---

## Critical Unknowns

| Unknown | Risk Type | Priority |
|----------|------------|----------|
| Do AppSec engineers have reliable business-criticality context to prioritize correctly? | Workflow Risk | HIGH |
| Does queue prioritization materially reduce time-to-action for critical findings? | Severity Risk | HIGH |
| Does the buyer (CISO / security leadership) accept a hybrid manual + policy model? | Buyer Risk | HIGH |
| How often queue overload blocks critical findings across target accounts? | Frequency Risk | MEDIUM |
| Is queue prioritization a standalone purchase driver or only part of broader workflow tooling? | Business Value Risk | MEDIUM |
| Can the process scale beyond 50 projects without governance breakdown? | Strategic Fit Risk | MEDIUM |

---

## Recommended Interview Roles

- **AppSec Engineer** — primary evidence on current queue workflow, context availability, and practical prioritization behavior.
- **Security Team Lead / AppSec Manager** — evidence on operational KPIs, team coordination, and policy exceptions.
- **CISO / Security Director** — evidence on governance constraints, auditability requirements, and purchasing priorities.
- **Developer / Engineering Manager** — evidence on downstream impact (release delays, perceived fairness, queue side effects).
- **Platform / DevOps Engineer** — evidence on CI/CD constraints, integration friction, and operational limits at scale.

---

## Interview Guide

### Current Workflow

- Walk me through how scan queue order is currently determined.
- Who can change queue priority today, and in what situations?
- What information do you check before changing scan priority?

### Recent Experience

- Tell me about the most recent incident where queue order mattered.
- Describe the last time a critical app had to wait in the queue.
- What happened during the last conflict over scan prioritization?

### Consequences

- What are the operational consequences when queue prioritization is wrong?
- How does this affect remediation time for high-severity findings?
- What risks or trade-offs appear when one team is prioritized over others?

### Alternatives

- How do you currently solve this without dedicated prioritization tooling?
- What policies, automation, or workarounds already exist?
- In what cases does the current process work well enough?

### Decision-Making Process

- Who approves prioritization rules or exceptions?
- What evidence is required to justify priority changes?
- What would block rollout of a manual-prioritization capability?

---

## Research Priorities

### High Priority

- Verify context availability for safe prioritization decisions.
- Verify measurable efficiency impact (time-to-action, queue delay reduction).
- Verify governance acceptance for hybrid manual + policy model.

### Medium Priority

- Measure frequency and segment boundaries of queue pain.
- Clarify buyer motivation and purchase framing (feature vs standalone category).
- Test scalability assumptions at 50+ project environments.

### Low Priority

- Compare secondary alternatives that do not change decision outcome in the near term.

---

## Expected Learning Outcomes

- Determine whether the problem is frequent enough in target segments to justify prioritization capabilities.
- Determine whether the value narrative should be efficiency-first instead of risk-reduction-first.
- Determine governance constraints required for adoption in enterprise environments.
- Determine minimum evidence threshold needed for backlog commitment.

