# Role Analysis: CISO

## Pain

Priority: SECONDARY

The CISO is responsible for enterprise risk management and wants visibility into how security resources are allocated.

Main concerns:

* critical systems may not be scanned early enough
* lack of visibility into prioritization decisions
* inability to demonstrate optimized risk allocation

However, mature organizations often prefer policy-based automation instead of manual operational control.

---

## New Problems Introduced

* escalation of prioritization conflicts
* auditability risks
* dependency on specific AppSec employees
* poor scalability
* distorted security metrics

---

## Alternatives

* policy-driven automation
* GRC integrations
* risk-based security programs
* increased scanning capacity
* CI/CD gating policies

---

## Failure Context

* security maturity is low — manual control adds chaos, not value
* prioritization cannot be audited for compliance
* dependency on individual AppSec engineers creates bus-factor risk
* scale exceeds 50+ projects without governance automation

---

## Applicability Boundaries

### Works when

* hybrid model: policy automation with documented manual exceptions
* visibility and audit trail for every prioritization decision

### Does not work when

* organization requires centralized, policy-driven risk allocation
* manual prioritization replaces rather than supplements automation

### Harms when

* metrics are distorted to justify ad-hoc queue changes
* escalation paths for prioritization conflicts are undefined