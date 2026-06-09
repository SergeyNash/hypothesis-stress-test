# Interview Questions

## Role: Application Security Engineer

### Current process

1. Walk me through how you manage the SAST scan queue today when multiple projects are waiting.
2. Tell me about the last time a business-critical application was delayed in the queue — what happened?
3. Describe how you currently decide which project gets scanned next.

### Constraints

1. What business-criticality information do you actually have access to when prioritizing?
2. What approvals or audit requirements exist for changing scan order?
3. How many concurrent projects do you typically manage in the queue?

### Actual behavior

1. Tell me about workarounds you use when the queue is overloaded.
2. Describe a situation where you could not reprioritize even though you wanted to.
3. How do developers typically react when their project is deprioritized?

### Recent experience

1. What happened the last time manual queue management caused a conflict with a development team?
2. Walk me through the last release where scan timing affected a security finding's remediation.

---

## Role: CISO

### Current process

1. Describe how prioritization decisions are made for security scanning across the organization.
2. Tell me how you currently demonstrate that critical systems receive appropriate scan coverage.
3. Walk me through your preferred model: manual control vs policy-driven automation.

### Constraints

1. What governance or compliance requirements apply to prioritization decisions?
2. How do you measure whether security resources are allocated optimally?
3. At what organizational scale does manual prioritization become unacceptable?

### Actual behavior

1. Tell me about a time when decentralized prioritization created an audit or visibility problem.
2. Describe what happens when AppSec and development teams disagree on scan order.
3. What alternatives to manual queue control have you already implemented or rejected?

### Recent experience

1. What was the outcome the last time a critical system was scanned late?
2. Walk me through a recent incident where scan queue management was discussed at leadership level.

---

## Role: Enterprise Developer

### Current process

1. Tell me how you learn when your project's SAST scan will complete.
2. Walk me through your release process and where scanning fits in the timeline.
3. Describe what you do when a critical finding appears just before release.

### Constraints

1. What release deadlines or SLAs constrain your ability to wait for scan results?
2. How much visibility do you have into why your project was prioritized or deprioritized?
3. What happens when scan results block a release?

### Actual behavior

1. Tell me about the last time unpredictable scan timing affected your delivery.
2. Describe how you escalate when you believe your project should be scanned sooner.
3. What workarounds do teams use when the scan queue is slow?

### Recent experience

1. Walk me through the last time queue prioritization felt unfair to your team.
2. What happened the last time you received a critical finding after assuming the scan was complete?
