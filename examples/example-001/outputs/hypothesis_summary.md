# Hypothesis Summary

## Statement

If Application Security engineers are able to manually prioritize projects in the SAST scanning queue, then business-critical applications will be scanned first, reducing the time required to detect high-risk vulnerabilities and lowering overall production risk.

## Core Idea

The hypothesis assumes that manual prioritization of scan queues by AppSec engineers will improve response time for critical systems and reduce business risk.

---

# Hidden Assumptions

## Assumption 1: Current prioritization is ineffective
- Why it matters: without real pain, the feature has no adoption driver
- Evidence present: role analysis shows queue overload and workarounds
- Evidence missing: quantitative data on queue wait times and impact

## Assumption 2: Engineers have business-criticality context
- Why it matters: prioritization requires knowing which apps matter most
- Evidence present: none direct
- Evidence missing: interviews confirming data availability and quality

## Assumption 3: Earlier scanning reduces production risk
- Why it matters: core value proposition depends on risk reduction
- Evidence present: internal logic only
- Evidence missing: market or telemetry linking scan order to risk outcomes

## Assumption 4: Manual prioritization scales
- Why it matters: enterprise adoption requires governance at scale
- Evidence present: CISO concerns about scalability
- Evidence missing: proof of sustainable process beyond 10–50 projects

---

# Applicability Boundaries

## When it creates value

* Mature AppSec teams with 10–50 active projects
* Clear business-criticality metadata available
* Queue wait times materially block critical findings
* Hybrid model: manual exceptions on top of policy automation

## When it is useless

* Scan duration is already short relative to release cycles
* FIFO queue does not create operational pain
* Organizations rely fully on automated risk-based scanning

## When it becomes harmful

* Decentralized prioritization conflicts with centralized risk governance
* Developers game the queue ("everything is critical")
* Audit cannot reproduce prioritization decisions

---

# Role Conflicts

## Agreement zones

* Scan queue overload is a real operational problem (AppSec, partially CISO)

## Tension zones

* AppSec wants control and responsiveness; CISO wants policy consistency
* Developers want predictability; AppSec wants flexibility to reprioritize

## Conflict zones

* Manual prioritization empowers AppSec but weakens CISO governance model
* Faster scans for critical apps may delay other teams' releases

## Blind spots

* Penetration Tester perspective not fully represented in role outputs
* Finance / procurement impact of queue tooling not analyzed
* Platform team CI/CD constraints not explicitly modeled

---

# Key Risks

* Feature solves efficiency, not risk reduction as originally framed
* Governance friction at enterprise scale
* Adoption blocked without business-context data

---

# Key Uncertainties

* Whether engineers can access reliable business-criticality data
* Whether prioritization measurably changes time-to-remediation for critical findings
* Whether hybrid manual + automated model is acceptable to CISO

---

# Assessment

## Promising

* Strong CRITICAL pain for AppSec engineers under queue constraints
* Real operational workflow improvement potential

## Uncertain

* Link between scan order and production risk reduction
* Enterprise scalability and governance acceptance

## Risky

* Political conflict between AppSec decentralization and CISO centralization
* Misaligned product narrative (risk vs efficiency)

## Requires validation

* AppSec engineer interviews on queue workflows and context access
* CISO workshop on governance model for prioritization
* Pilot with one mature account (10–30 projects)
