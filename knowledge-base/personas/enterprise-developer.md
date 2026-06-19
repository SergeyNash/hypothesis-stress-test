---
persona: Enterprise Developer
slug: enterprise-developer
source_status: initial_profile
source_interviews: []
last_updated: 2026-06-19
confidence: low
---

# Persona: Enterprise Developer

## Role Summary

An Enterprise Developer is an experienced software developer working in a large organization with established Secure SDLC practices and integrated security tooling.

The developer is primarily responsible for delivering business functionality and maintainable software, while operating inside a security-aware engineering culture.

## Goals

- Deliver reliable, scalable, and maintainable features.
- Pass CI/CD checks, including security gates.
- Minimize recurring security-related rework.
- Preserve development velocity without creating long-term technical or security debt.
- Contribute to secure engineering practices without becoming an AppSec specialist.

## Responsibilities

- Implement features and maintain existing systems.
- Apply secure coding practices during development.
- Address findings raised by CI/CD pipelines or AppSec engineers.
- Participate in code reviews with attention to quality and basic security.
- Collaborate with AppSec, DevOps, QA, and architecture stakeholders when security findings require clarification.

## Recurring Pains

- Security findings that lack technical or business context.
- Fixes that require large refactoring close to release deadlines.
- Duplicate findings from SAST, SCA, DAST, and other tools.
- False positives that consume time and attention.
- Tension between delivery timelines and remediation work.
- Limited visibility into why tools flag certain patterns.

## Decision Criteria

- Does this help me resolve findings without blocking delivery?
- Is the finding actionable and context-aware?
- Can I understand exploitability and priority?
- Does the workflow fit into normal development and CI/CD practices?
- Does this reduce recurring rework?

## Success Metrics

- Low number of security-related pull request rejections.
- Reduced recurrence of similar vulnerabilities.
- Faster response to assigned security findings.
- Stable CI/CD passes without security blockers.
- Peer trust as a reliable and responsible engineer.

## Objections / Anti-Patterns

- Treating security as separate from engineering quality.
- Blindly fixing every issue without context.
- Applying superficial patches only to unblock the pipeline.
- Ignoring security findings because they are seen as AppSec's responsibility.
- Security workflows that create friction without explaining risk.

## Buying / Influence Role

Primary affected user and adoption gate. Usually not a buyer, but can make or break implementation through daily usage, feedback, resistance, or workarounds.

## Evidence Base

No interviews are linked yet. Treat this persona as an initial profile and a weak local signal until it is rebuilt from CustDev materials.

## Open Questions

- Which security findings create the most developer friction?
- What information does a developer need to act confidently on a finding?
- Which security workflows are accepted as quality work versus perceived as blockers?
- How often do developers bypass or ignore security tooling due to false positives?
