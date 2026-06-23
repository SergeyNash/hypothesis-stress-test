# Market Analysis

## MCP Status

Confluence MCP: not configured (example run — canonical outputs produced without live Confluence search)

## Local Signals from Knowledge Base

missing local file evidence — example artifacts do not include discovery inventory

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
  - basis: combination of pipeline friction and adoption failure signals

- Manual prioritization scalability issues at enterprise scale
  - signal: medium
  - type: inferred
  - basis: policy-driven automation trend vs manual queue control

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

- Overall local KB signal: none (inventory not included in canonical example)
- Overall confluence signal: none (MCP not used in example)
- Overall external signal: strong (related problems), weak (standalone queue prioritization)
- Missing evidence: internal Confluence research on AppSec queue workflows, customer interview summaries
- Opportunity window: MEDIUM
