# Market Analysis

## MCP Status

Confluence MCP: not configured (example run — canonical outputs produced without live Confluence search)

## Local Signals from Knowledge Base

- Critical projects experience multi-hour scan queue delays
  - signal: strong
  - type: local
  - evidence: EVID-001, EVID-004
  - evidence_type: quote, image_observation
  - source: `workshop_queue.md`, `whiteboard_scan_queues.txt`

- Queue backlog surfaces only when releases are blocked
  - signal: medium
  - type: local
  - evidence: EVID-002
  - evidence_type: quote
  - source: `workshop_queue.md`

- Business-critical apps are not automatically prioritized in current workflow
  - signal: strong
  - type: local
  - evidence: EVID-003
  - evidence_type: transcript_excerpt
  - source: `2025-03-appsec-interview-excerpt.md`

- Manual flagging required for tier-1 / escalated apps
  - signal: medium
  - type: local
  - evidence: EVID-001, EVID-003
  - evidence_type: quote, transcript_excerpt
  - note: tribal knowledge and Slack-driven reordering described in sources

## Confluence Signals

missing confluence evidence — example artifacts; configure Confluence MCP for live runs per [implementations/confluence-mcp.md](../../../implementations/confluence-mcp.md)

## External Market Signals

- Pipeline blocking friction in CI/CD security gates
  - signal: strong
  - type: external
  - source: industry pattern (SAST in CI/CD pipelines)

- SAST false positives and adoption failure
  - signal: strong
  - type: external
  - source: industry pattern (developer friction with security tools)

- Risk-based prioritization as recognized market pattern
  - signal: strong
  - type: external
  - source: vendor landscape (Snyk, GitHub Advanced Security, Checkmarx)

- Scan queue prioritization as standalone problem category
  - signal: weak
  - type: external
  - note: not explicitly established as a standalone market category

## Inferred Signals

- Security vs Delivery conflict is structural in enterprise AppSec
  - signal: strong
  - type: inferred
  - basis: EVID-002 (release blocking) + external pipeline friction signals

- Manual prioritization scalability issues at enterprise scale
  - signal: medium
  - type: inferred
  - basis: EVID-003 (manual flagging) + external policy-automation trend

## Key Stakeholders

| Role | Type |
|------|------|
| CISO | Buyer |
| AppSec Engineer | Primary user |
| Platform / DevOps | Operational owner |
| Enterprise Developer | Secondary user |

## Existing Market Solutions

* Risk-Based Prioritization
* AI-Assisted Triage
* Developer Feedback Loops
* Policy-Based Automation
* Vendor-specific approaches (Snyk, GitHub Advanced Security, Checkmarx)

## Gaps in Existing Approaches

* No flexible scan queue prioritization
* Security vs Delivery conflict
* Manual prioritization scalability issues
* Lack of transparent prioritization criteria
* Dependency on business context
* Adoption matters more than detection quality

## Signal Summary

- Overall local KB signal: strong (4 extractable items from mixed markdown/text/custdev sources)
- Overall confluence signal: none (MCP not used in example)
- Overall external signal: strong (related problems), weak (standalone queue prioritization)
- Missing evidence: internal Confluence research on AppSec queue workflows; full audio transcript (EVID-005 metadata only)
- Opportunity window: MEDIUM–HIGH (local evidence supports queue pain; external category still weak)
