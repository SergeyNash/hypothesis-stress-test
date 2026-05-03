# Hypothesis

## Statement

If application security engineers are able to manually prioritize projects in the SAST scanning queue, then critical applications will be scanned earlier, which will reduce the time to detect high-risk vulnerabilities and lower overall production risk.

---

## Relevant Roles

* Application Security Engineer
* Security Team Lead
* Developer
* Engineering Manager

---

## Research Context

### Domain

* Application Security (SAST)

### Product Type

* Static Application Security Testing platform

### Target Audience

* Application security teams in mid-to-large organizations
* Security engineers responsible for vulnerability management

### Scenario

* Multiple projects are queued for SAST scanning
* Scan execution is resource-constrained (queue-based)
* Not all applications have equal business criticality
* Engineers need to process results quickly for high-risk systems

### Constraints

* Limited scanning capacity
* High volume of projects
* Need to balance coverage vs prioritization
* Organizational pressure to reduce production risk

---

## Notes

* The hypothesis assumes that prioritization is currently not flexible or not efficient
* It also assumes that earlier scanning leads to faster mitigation
* These assumptions must be validated through Roles and Market layers
