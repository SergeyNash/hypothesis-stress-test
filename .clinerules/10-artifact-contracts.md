# Artifact Contracts

Every hypothesis run uses an isolated workspace directory (`RUN_DIR`) — a hypothesis run archive.

## RUN_DIR structure

```text
RUN_DIR/
  input/
    hypothesis.md          # input: metadata, statement, roles, research context
    attachments/           # optional: supporting files
  run.md                   # optional: execution log
  outputs/
    role_outputs/          # one file per role
    hypothesis_summary.md
    validation_questions.md
    discovery_preview.md
    evidence_inventory.md
    business_context_analysis.md
    missing_business_context.md
    market_analysis.md
    hypothesis_map.md
    hypothesis_digest.txt
    customer_discovery_plan.md
    decision_review.md
    human_report.html
    ready_for_synthesis.marker
    knowledge_retrieval_complete.marker
    business_context_complete.marker
    market_analysis_complete.marker
    synthesis_complete.marker
    customer_discovery_planning_complete.marker
    decision_review_complete.marker
    human_report_complete.marker
```

## Input: input/hypothesis.md

Required sections:

```markdown
# Hypothesis

## Metadata

- Hypothesis ID: HYP-YYYY-MM-DD-NNN
- Created at: YYYY-MM-DD
- Run ID: RUN-YYYY-MM-DD-NNN
- Status: draft | running | completed | archived

## Statement
[Clear, testable statement]

## Relevant Roles
- [role 1]
- [role 2]

## Research Context
- Domain: [domain]
- Target audience: [audience]
- Scenario: [scenario]
- Constraints: [optional]
```

See `templates/input-schema.md` for the full schema.

## Optional local role sources

Reusable role profiles may exist in:

```text
knowledge-base/personas/
```

Raw CustDev inputs and persona rebuild logs may exist in:

```text
knowledge-base/interviews/
knowledge-base/persona-builds/
```

Roles listed in `input/hypothesis.md` remain the run-specific source of scope. Persona files are supporting context, not a replacement for hypothesis-specific role selection.

## Output naming

| Artifact | Path | Produced by |
| ---------- | ------ | ------------- |
| Per-role analysis | `outputs/role_outputs/{role_slug}.md` | Facilitator (Roles Layer) |
| Internal summary | `outputs/hypothesis_summary.md` | Facilitator (Roles Layer) |
| Interview questions | `outputs/validation_questions.md` | Facilitator (Roles Layer) |
| Retrieval preview | `outputs/discovery_preview.md` | Local Evidence Discovery |
| Evidence inventory | `outputs/evidence_inventory.md` | Local Evidence Discovery |
| Business context analysis | `outputs/business_context_analysis.md` | Business Context & Value Check |
| Missing business context | `outputs/missing_business_context.md` | Business Context & Value Check (gap only) |
| Market analysis | `outputs/market_analysis.md` | Market Layer |
| Full synthesis | `outputs/hypothesis_map.md` | Synthesis Layer |
| Short digest | `outputs/hypothesis_digest.txt` | Synthesis Layer |
| Customer discovery plan | `outputs/customer_discovery_plan.md` | Customer Discovery Planning |
| Decision review | `outputs/decision_review.md` | Decision Review |
| Human decision report | `outputs/human_report.html` | Human Report Export |

Role slugs: lowercase, underscores (e.g. `appsec_engineer`, `ciso`).

### hypothesis_summary.md (facilitator)

Must include: hidden assumptions, applicability boundaries, role conflicts, key risks, key uncertainties, assessment (promising / uncertain / risky / requires validation). Language matches `input/hypothesis.md`.

### role_outputs/{role_slug}.md (facilitator)

Must include: pain, new problems, alternatives, failure context, applicability boundaries. Language matches `input/hypothesis.md`.

### validation_questions.md (facilitator)

Behavior-based interview questions per role. No leading or hypothetical questions (e.g. "Would you use this?"). Language matches `input/hypothesis.md`.

### discovery_preview.md (local evidence discovery)

Must include:

- limits applied (`max_files_scanned`, `max_file_size`, `max_evidence_items`)
- files scanned
- files skipped with reasons
- candidate files
- top relevant files with planned evidence type

Preview is mandatory and generated before evidence extraction.

### evidence_inventory.md (local evidence discovery)

Must include atomic `EVID-NNN` items. Each item should capture one signal only.

Required fields per item:

- `source_path`
- `source_kind`
- `evidence_type` (`quote`, `transcript_excerpt`, `image_observation`, `metadata_only`, `observation`)
- `observation`
- `relevance`
- `relevance_reason`
- `retrieved_by`

Optional fields:

- `location`
- `companion_source`
- `extraction_note` (required for `image_observation`)

### business_context_analysis.md (business context & value check)

Must include: available context, missing context, stakeholder map, value flow (Problem → Beneficiary → Behavior change → Business effect), business effect type(s), strategic fit with citations, key risks, key opportunities, summary for downstream layers. Language matches `input/hypothesis.md`.

### missing_business_context.md (business context gap)

Created only when strategy/OKR/business-model materials are absent. Must list missing source types and what to add to KB. Do not substitute fabricated strategic fit.

## Completion markers

Marker presence means that the named phase was attempted and the marker body is the canonical machine-readable result. Presence alone does not always mean that a full analysis artifact exists: consumers MUST read `status`.

Canonical status semantics:

- `completed` — the phase completed and its required outputs listed in `inputs` are available to the next phase.
- `skipped_missing_context` — allowed only for `business_context_complete.marker`; the phase completed as a gap check, `missing_business_context.md` exists, and downstream phases must preserve this gap rather than infer strategic fit.

Marker bodies MUST be valid JSON with the keys `status`, `completed_phase`, `next_phase`, and `inputs` when the completed phase produced or checked relevant artifacts. Canonical examples do not support legacy free-text marker bodies.

### Canonical machine-readable marker registry

```json
{
  "ready_for_synthesis.marker": {
    "status": "completed",
    "completed_phase": "facilitator",
    "next_phase": "local_evidence",
    "inputs": [
      "outputs/role_outputs/*",
      "outputs/hypothesis_summary.md",
      "outputs/validation_questions.md"
    ]
  },
  "knowledge_retrieval_complete.marker": {
    "status": "completed",
    "completed_phase": "local_evidence",
    "next_phase": "business_context",
    "inputs": [
      "outputs/discovery_preview.md",
      "outputs/evidence_inventory.md"
    ]
  },
  "business_context_complete.marker": [
    {
      "status": "completed",
      "completed_phase": "business_context",
      "next_phase": "market",
      "inputs": [
        "outputs/business_context_analysis.md"
      ]
    },
    {
      "status": "skipped_missing_context",
      "completed_phase": "business_context",
      "next_phase": "market",
      "inputs": [
        "outputs/missing_business_context.md"
      ]
    }
  ],
  "market_analysis_complete.marker": {
    "status": "completed",
    "completed_phase": "market",
    "next_phase": "synthesis",
    "inputs": [
      "outputs/market_analysis.md"
    ]
  },
  "synthesis_complete.marker": {
    "status": "completed",
    "completed_phase": "synthesis",
    "next_phase": "customer_discovery_planning",
    "inputs": [
      "outputs/hypothesis_map.md",
      "outputs/hypothesis_digest.txt"
    ]
  },
  "customer_discovery_planning_complete.marker": {
    "status": "completed",
    "completed_phase": "customer_discovery_planning",
    "next_phase": "decision_review",
    "inputs": [
      "outputs/customer_discovery_plan.md"
    ]
  },
  "decision_review_complete.marker": {
    "status": "completed",
    "completed_phase": "decision_review",
    "next_phase": "human_report",
    "inputs": [
      "outputs/decision_review.md"
    ]
  },
  "human_report_complete.marker": {
    "status": "completed",
    "completed_phase": "human_report",
    "next_phase": "human_decision",
    "inputs": [
      "outputs/human_report.html"
    ]
  }
}
```

The registry describes each individual marker body; write only the object under that marker's filename, not the entire registry. For `business_context_complete.marker`, write exactly one of the two objects in its array.

### human_report.html (human report export)

Decision-facing HTML report for humans. Generated after Decision Review. Does not replace Markdown artifacts as source of truth.

**Canonical prerequisite:** `decision_review_complete.marker` with `status: completed`. A bare `decision_review.md` is a historical-run migration fallback only.

**Source artifacts (read-only):**

| Section | Primary sources |
| ------- | --------------- |
| Header / metadata | `input/hypothesis.md` |
| Digest | `hypothesis_digest.txt` |
| What changed? | `hypothesis_map.md` (`Impact on Original Hypothesis`), fallback: digest + `decision_review.md` |
| Confidence / Recommendation | `decision_review.md` |
| Decision Readiness | derived from `decision_review.md` + business context (see mapping below) |
| Business value summary | `business_context_analysis.md` (Strategic Fit, Business Effect Type, Summary) |
| Stakeholder / value flow | `business_context_analysis.md` (Stakeholder Map, Value Flow) |
| Top contradictions | `hypothesis_map.md` (`Key Divergences`, max 3) |
| Cheapest validation path | `decision_review.md` (`Validation Plan`, lowest effort items) |
| Validation priorities | `customer_discovery_plan.md` |
| Signal snapshot | `market_analysis.md` (`Signal Summary` only) |
| Detailed artifacts | grouped links to all contract artifacts present in `RUN_DIR` |

**Required HTML sections:**

1. Sticky header — Hypothesis ID, confidence, recommendation, decision readiness badges
2. Executive overview — statement, digest, status cards
3. Business value — effect type, strategic fit, value flow (if `business_context_analysis.md` exists)
4. What changed? — original framing, reframed as, why changed
5. Top contradictions — up to 3 key divergences from synthesis
6. Decision summary — executive summary, final recommendation, next step
7. Cheapest validation — lowest-effort validation plan items from decision review
8. Validation priorities — high-priority unknowns, research actions, interview roles
9. Signal snapshot — opportunity window / signal summary (if available)
10. Detailed artifacts — grouped relative links (include Business Context group when present)

**Decision Readiness mapping** (choose one most action-guiding status):

| Status | Typical signal |
| ------ | -------------- |
| `Ready for backlog` | recommendation supports build/commit and confidence is high |
| `Needs interviews` | validation-first recommendation, customer discovery next, critical unknowns remain |
| `Needs business context` | strategic fit, buyer, budget, or business value evidence missing |
| `Reject / reframe` | reject/reframe recommendation or original hypothesis materially wrong |

**Relative link rules** (report lives at `RUN_DIR/outputs/human_report.html`):

| Target | Link from `human_report.html` |
| ------ | ----------------------------- |
| Input | `../input/hypothesis.md` |
| Sibling output | `hypothesis_digest.txt`, `decision_review.md`, etc. |
| Role output | `role_outputs/{role_slug}.md` |

**Detailed artifact groups:**

- Input: `../input/hypothesis.md`
- Role Analysis: `hypothesis_summary.md`, `validation_questions.md`, `role_outputs/*.md`
- Evidence: `discovery_preview.md`, `evidence_inventory.md`
- Business Context: `business_context_analysis.md`, `missing_business_context.md`
- Market: `market_analysis.md`
- Synthesis: `hypothesis_digest.txt`, `hypothesis_map.md`
- Customer Discovery: `customer_discovery_plan.md`
- Decision Review: `decision_review.md`

Omit links to files that do not exist. Show "not available" only for optional sections, not for missing grouped links.

**Constraints:**

- Single static file, inline CSS and minimal vanilla JS only
- No CDN, npm, build tools, or external assets
- Must open via `file://`
- Language matches `input/hypothesis.md`

### hypothesis_map.md (synthesis)

Must include: confirmed signals, internal illusions, missed opportunities, local optimization traps, key divergences, blind spots, new information (post-comparison only), applicability boundaries, impact on original hypothesis, validation priorities. Language matches `input/hypothesis.md`.

### hypothesis_digest.txt (synthesis)

Max 150 words: viability, key conflict, primary illusion, blind spot, risk, insight, next step. Language matches `input/hypothesis.md`.

### customer_discovery_plan.md (customer discovery planning)

Must include: research objective, what is already known, critical unknowns with risk type and priority, recommended interview roles, behavior-based interview guide, research priorities (HIGH / MEDIUM / LOW), expected learning outcomes. Language matches `input/hypothesis.md`.

Canonical order:

```text
Validate → Facilitator → Local Evidence → Business Context → Market → Synthesis → Customer Discovery Planning → Decision Review → Human Report → human decision
```

For canonical runs, do not start the next phase until the preceding marker exists and has an allowed canonical status:

- Local Evidence requires `ready_for_synthesis.marker` with `status: completed`.
- Business Context requires `knowledge_retrieval_complete.marker` with `status: completed`.
- Market requires `business_context_complete.marker` with `status: completed` or `status: skipped_missing_context`.
- Synthesis requires `market_analysis_complete.marker` with `status: completed`; it also consumes the existing Facilitator, Local Evidence, and Business Context artifacts or explicit Business Context gap.
- Customer Discovery Planning requires `synthesis_complete.marker` with `status: completed`.
- Decision Review requires `customer_discovery_planning_complete.marker` with `status: completed`.
- Human Report requires `decision_review_complete.marker` with `status: completed`.
- Human decision requires `human_report_complete.marker` with `status: completed`.

Equivalent output files and legacy free-text markers may be used only when migrating historical runs; they are not canonical completion signals.

## RUN_DIR examples

```text
examples/example-001/              # canonical example
runs/HYP-2026-06-22-001/           # user-created run archive
```

When the user does not specify `RUN_DIR`:

- **Chat-first (preferred):** invoke `/run-hypothesis-conversational.md` — intake collects input, agent **proposes** new `runs/HYP-YYYY-MM-DD-NNN/` in dialog, user confirms, then bootstrap.
- **File-first (fallback):** ask for `RUN_DIR` or create a new directory under `runs/` using the naming pattern `HYP-YYYY-MM-DD-NNN`.

When the user **does** specify `RUN_DIR: runs/HYP-...` — continue that existing archive; do not create a new folder.

### Conversational bootstrap (dialog-confirmed)

When creating a new run via `/run-hypothesis-conversational.md` (no `RUN_DIR:` in message):

**Two-step confirm:**

1. User confirms hypothesis draft card
2. Agent proposes next free `HYP-YYYY-MM-DD-NNN`, lists existing runs for today, user confirms `RUN_DIR`

**Only after step 2** — create directory and write `input/hypothesis.md`.

**New run isolation:**

- Never reuse an existing `runs/HYP-*` for a new hypothesis
- Open editor tabs from a previous run are not a write target
- Scan `runs/` for `HYP-YYYY-MM-DD-*`, propose next `NNN` (001, 002, …)
- Set `Hypothesis ID` = folder name; `Run ID` = `RUN-YYYY-MM-DD-NNN`
- Folder name must match `Hypothesis ID` in metadata
- Write only contract artifacts from this document — no ad-hoc files (e.g. `product_specification.md`)

## Migration note

```text
Old: runs/my-hypothesis/hypothesis.md
New: runs/HYP-YYYY-MM-DD-NNN/input/hypothesis.md
```
