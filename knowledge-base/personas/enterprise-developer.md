---
persona: Enterprise Developer
slug: enterprise-developer
source_status: mixed
source_interviews: []
last_updated: 2026-08-26
confidence: medium
---

# Persona: Enterprise Developer

## Role Summary

An Enterprise Developer is an experienced (often senior or lead) software developer in a large organization with established Secure SDLC practices and integrated security tooling, including SAST.

They are primarily responsible for delivering business functionality and maintaining system architecture, while operating inside a security-aware engineering culture. They are not an AppSec specialist, but they understand secure coding principles and work with security teams when needed.

## Goals

- Deliver reliable, scalable, and maintainable features.
- Pass CI/CD checks, including security gates.
- Minimize recurring security-related rework.
- Preserve development velocity without creating long-term technical or security debt.
- Contribute to secure engineering practices without becoming an AppSec specialist.

## Motivations

- Ship production-ready code without last-minute security blockers.
- Be trusted with complex or security-sensitive components.
- Keep engineering quality high without unnecessary friction.
- Grow technically while staying aligned with enterprise standards.

## Responsibilities

- Implement features and maintain existing and legacy systems.
- Apply secure coding practices during day-to-day development.
- Address findings raised by CI/CD pipelines or AppSec engineers.
- Participate in code reviews with attention to quality and basic security, including unsafe patterns in teammates' PRs.
- Collaborate with AppSec, DevOps, QA, and architecture when a finding needs clarification or an architectural decision.

## Recurring Pains

- Security findings that lack technical or business context.
- Fixes that require large refactoring close to release deadlines.
- Duplicate findings from SAST, SCA, DAST, and other tools.
- False positives that consume time and attention.
- Tension between delivery timelines and remediation work.
- Limited visibility into why tools flag certain patterns.

## Challenges and Dilemmas

- Balancing delivery speed with secure design.
- Deciding when to refactor properly versus applying a minimal fix.
- Negotiating priority between business deadlines and security remediation.
- Judging whether a flagged issue is actually exploitable in this context.
- Following corporate security standards without abandoning pragmatic engineering.

## Decision Criteria

- Does this help me resolve findings without blocking delivery?
- Is the finding actionable and context-aware?
- Can I understand exploitability and priority?
- Does the workflow fit into normal development and CI/CD practices?
- Does this reduce recurring rework?

## Success Metrics

- Low number of security-related pull request rejections.
- Reduced recurrence of similar vulnerabilities in the team's codebase.
- Faster response to assigned security findings (MTTR).
- Stable CI/CD passes without security blockers.
- Peer trust as a reliable and responsible engineer.

## Objections / Anti-Patterns

- Treating security as separate from engineering quality, or as an obstacle rather than part of quality.
- Blindly fixing every issue without context.
- Applying superficial patches only to unblock the pipeline.
- Ignoring security findings because they are seen as AppSec's responsibility.
- Avoiding AppSec when a finding needs clarification.
- Security workflows that create friction without explaining risk.

## Buying / Influence Role

Primary affected user and adoption gate. Usually not a buyer, but can make or break implementation through daily usage, feedback, resistance, or workarounds. If the signal is noisy, this persona will ignore the tool even if CISO bought it.

## A Typical Day

Composite, not a literal schedule:

- Stand-up and any pipeline blockers.
- Feature work against internal coding and security guidelines.
- Code review of a teammate's PR, including unsafe patterns.
- A CI or AppSec finding to address, sometimes with a short AppSec sync on exploitability.
- Push, wait for a clean CI/CD run, update task status.

Use this as context for when security work lands in the developer day (mid-afternoon finding, not a dedicated security job), not as evidence of a specific company cadence.

## Evidence Base

This version synthesizes the original initial profile with an interview-informed role brief. Raw interview files are not yet linked in `knowledge-base/interviews/`. Until those sources are attached, treat this persona as a stronger starting profile than `initial_profile`, but still a local signal rather than primary CustDev evidence.

## Open Questions

- Which security findings create the most developer friction?
- What information does a developer need to act confidently on a finding?
- Which security workflows are accepted as quality work versus perceived as blockers?
- How often do developers bypass or ignore security tooling due to false positives?
- When do they choose a minimal patch over a proper refactor, and who decides?
