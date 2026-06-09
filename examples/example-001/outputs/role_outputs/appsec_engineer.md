# Role Analysis: Application Security Engineer

## Pain

Priority: CRITICAL

AppSec engineers must balance scan coverage against deep analysis of critical systems under limited scanning capacity.

Main pain points:

* inability to quickly react to changing business priorities
* equal treatment of systems with different risk levels
* manual queue-management workarounds
* difficulty justifying prioritization decisions to developers

---

## New Problems Introduced

* cognitive overload
* political pressure from development teams
* lack of decision reproducibility
* metric manipulation risks
* additional operational overhead

---

## Alternatives

* policy-driven prioritization
* metadata-based automation
* risk-based scanning
* parallel scanning
* keeping FIFO as the default model

---

## Failure Context

* scan duration is already short relative to release cycles
* business-criticality data is unavailable or unreliable
* organization lacks operational maturity for manual decisions
* political pressure makes prioritization unsustainable

---

## Applicability Boundaries

### Works when

* queue wait times block critical findings
* engineer has access to business-criticality context
* team size is 10–50 projects with mature AppSec process

### Does not work when

* automated risk-based scanning already handles prioritization
* FIFO queue creates no operational pain

### Harms when

* decisions cannot be audited or reproduced
* developers systematically bypass or game the queue