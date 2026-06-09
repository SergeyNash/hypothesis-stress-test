# Role Analysis: Enterprise Developer

## Pain

Priority: SECONDARY

Developers experience uncertainty around scan timing and release predictability.

Pain points:

* unpredictable scan completion times
* last-minute critical findings before release
* perceived unfairness in prioritization
* waiting for scan results blocks delivery

---

## New Problems Introduced

* perceived unfairness
* lack of transparency
* political pressure on AppSec teams
* “everything is critical” behavior
* focus shift from code quality to queue manipulation

---

## Alternatives

* shift-left scanning
* CI/CD-integrated scanning
* predictable schedules
* self-service scanning
* increasing throughput

---

## Failure Context

* prioritization criteria are unclear
* release deadlines are ignored
* informal bypasses exist
* release blocking becomes operationally destructive
* developers receive no visibility into queue changes

---

## Applicability Boundaries

### Works when

* scan timing transparency is provided to development teams
* prioritization rules are predictable and documented

### Does not work when

* queue changes are opaque and unpredictable
* scan throughput is already sufficient for release cadence

### Harms when

* "everything is critical" behavior emerges
* developers shift focus from code quality to queue manipulation