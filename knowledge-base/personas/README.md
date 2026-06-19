# Personas

Personas are synthesized role profiles used by the Roles Layer.

They are not raw evidence. A persona should summarize recurring patterns from interviews, customer discovery notes, internal research, and domain expertise.

## Contract

Each persona file should include frontmatter:

```yaml
persona: Application Security Engineer
slug: application-security-engineer
source_status: initial_profile | custdev_backed | mixed
source_interviews: []
last_updated: YYYY-MM-DD
confidence: low | medium | high
```

## Evidence Rule

If `source_interviews` is empty, treat the persona as a weak local signal.

If the persona is backed by linked interviews or research notes, cite those sources in the Market Layer and Decision Review when relevant.

## Relationship To Interviews

- `knowledge-base/interviews/` stores raw CustDev and interview materials.
- `knowledge-base/persona-builds/` documents how personas were rebuilt from interview evidence.
- `knowledge-base/personas/` stores the current reusable persona artifacts.
