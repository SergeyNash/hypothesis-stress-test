---
persona: Security Champion
slug: security-champion
source_status: mixed
source_interviews: []
last_updated: 2026-08-26
confidence: medium
---

# Persona: Security Champion

## Role Summary

A Security Champion is a software engineer who takes additional responsibility for security inside a development team. Security is not the formal job title. They remain an engineer first.

The role is a bridge between AppSec and developers: they have more interest and practical security literacy than most peers, translate AppSec requirements into engineering work, and send team constraints back to security. They may train colleagues, join incident analysis, or represent the team in AppSec discussions — without becoming a full-time AppSec engineer.

## Goals

- Embed security into daily development workflows.
- Reduce vulnerabilities reaching production.
- Reduce frustration caused by security requirements by explaining their purpose.
- Help the team adopt secure practices.
- Represent both AppSec reasoning and developer constraints.

## Motivations

- Want the product to be genuinely secure and reliable.
- Proud when colleagues apply secure practices without being pushed.
- Value influencing product quality beyond a single ticket.
- Use the role to grow toward AppSec, architecture, or broader technical leadership — while staying effective as an engineer.

## Responsibilities

- Raise security concerns during planning, stand-ups, and backlog discussions, including fixes that must not slip.
- Perform initial triage of findings from SAST, DAST, and other tools: filter noise, name what is actually critical, and give the team a usable priority.
- Help the team adopt practices such as secret management, authentication handling, and input validation.
- Explain business context and technical limitations to AppSec, including when a requirement is unrealistic in the current delivery context.
- Organize short knowledge-sharing sessions on security topics.
- Include security in code reviews and look for weaknesses while doing ordinary PR work.
- Participate in incident analysis when the team is involved.

## Recurring Pains

- Too many false positives from SAST, which frustrates developers and positions the champion as the "bad cop."
- Time constraints: feature work and deadlines plus champion duties.
- Limited deep security expertise compared with AppSec specialists; assessing risk is often hard.
- If they push security too hard, the team resists; if they relax, quality drops.
- Security tools that do not integrate smoothly into DevOps, so the team lives with workarounds.

## Challenges and Dilemmas

- How to convince the team that security is part of quality, not a blocker.
- How to prioritize vulnerabilities against business-driven features.
- How to tell AppSec that some requirements do not fit current technical or delivery reality.
- How to integrate security without harming velocity.
- How to grow security expertise without stopping being an effective engineer.

## Decision Criteria

- Can this fit into the team's normal development workflow?
- Does it reduce security friction without lowering quality?
- Can it help the team prioritize vulnerabilities pragmatically?
- Is it clear enough for non-specialist developers to use?
- Does it strengthen collaboration with AppSec?

## Success Metrics

- Fewer critical vulnerabilities reaching production.
- Lower average remediation time.
- The team raises security concerns without constant reminders.
- Penetration testing results improve over time.
- AppSec stakeholders are satisfied with collaboration quality.

## Objections / Anti-Patterns

- Acting as a "mini-AppSec" and handling everything alone instead of enabling the team.
- Sacrificing delivery entirely for security, or ignoring security for delivery.
- Passing security requirements to the team without business or technical context.
- Turning security into punishment instead of shared responsibility.

## Buying / Influence Role

Internal adoption bridge and workflow influencer. Usually not a buyer, but decisive for team-level adoption, developer sentiment, feedback loops, and whether a tool is used or treated as noise. AppSec and CISO buy; champions determine whether the team complies in practice.

## A Typical Day

Composite, not a literal schedule:

- Stand-up: remind the team about vulnerability fixes that should not be forgotten.
- Own feature work, plus PR reviews looking for security weaknesses.
- A SAST dump with dozens of findings: filter, pick the critical ones, communicate priorities.
- Sync with AppSec on new requirements and negotiate a practical implementation.
- Retro: "what can we improve in how we handle security?"

Use this as context for split attention (engineer plus champion), not as evidence of a specific company cadence.

## Evidence Base

This version synthesizes the original initial profile with an interview-informed role brief. Raw interview files are not yet linked in `knowledge-base/interviews/`. Until those sources are attached, treat this persona as a stronger starting profile than `initial_profile`, but still a local signal rather than primary CustDev evidence.

## Open Questions

- What level of security responsibility do champions realistically accept?
- Which workflows create resentment versus ownership?
- What support does a Security Champion need from AppSec?
- How often do champions perform real triage versus only coordination?
- How much time do they actually get for champion work versus feature delivery?
