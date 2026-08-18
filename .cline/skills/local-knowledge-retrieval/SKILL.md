---
name: local-knowledge-retrieval
description: Discover traceable local evidence from a messy knowledge base before Business Context and Market Layer. Produce discovery_preview.md and evidence_inventory.md with atomic evidence items only.
---

# Local Evidence Discovery

Collect a small, traceable set of local evidence artifacts.

This skill does not perform market interpretation.

## Purpose

`evidence_inventory.md` separates retrieval from analysis:

- Retrieval discovers evidence.
- Business Context and Market Layer interpret evidence.
- Synthesis resolves contradictions.

## Prerequisites

Required:

- `RUN_DIR/input/hypothesis.md` exists
- `RUN_DIR/outputs/ready_for_synthesis.marker` with canonical JSON
  `status: completed`
- Workspace root is the KB project root (recommended)

Optional input:

- `RUN_DIR/outputs/hypothesis_summary.md` (for relevance hints)

If the Facilitator marker is missing, stop and ask the user to run Facilitator first.

## Scope and limits (V1 defaults)

Use strict guardrails:

- `max_files_scanned`: 200
- `max_file_size`: 2 MB
- `max_evidence_items`: 20
- `skip_binary_by_default`: true

Supported source kinds:

- `markdown`: `.md`, `.markdown`
- `text`: `.txt`, `.log`, `.csv`
- `image`: `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`
- `transcript`: `.srt`, `.vtt`, transcript `.md`/`.txt`
- `audio`: `.mp3`, `.wav`, `.m4a`, `.ogg` (transcript preferred)
- `video`: `.mp4`, `.mov`, `.webm`, `.mkv` (transcript preferred)

Explicitly skip in V1:

- `.pdf`, `.docx`, `.html`, `.pptx`, `.xlsx`

Record `limit_reached: true` in preview metadata when a cap stops the scan or extraction.

## Scan root and exclusions

If `RUN_DIR/kb-samples/` exists, scan it **first** as a run-local KB island (used by examples and isolated demos).

Otherwise scan recursively from KB workspace root.

Exclude:

- `hypothesis-stress-test/` (skip only when the workspace root is a parent KB, not when this repo is the workspace)
- `runs/`
- `.git/`
- `.clinerules/`
- `.cline/`
- `node_modules/`

## Output language

Write output headings/body in the same language as `input/hypothesis.md`.

## Discovery process

### Step 1 — Build preview (always)

Write `RUN_DIR/outputs/discovery_preview.md`:

```markdown
# Discovery Preview

## Limits
- max_files_scanned: 200
- max_file_size: 2 MB
- max_evidence_items: 20
- limit_reached: true | false

## Scanned
- [path]

## Skipped
- [path] — reason

## Candidates
- [path] — planned evidence_type

## Top relevant
- [path] — planned evidence_type — why relevant
```

Preview is mandatory and non-blocking in V1.

### Step 2 — Auto-continue extraction

After preview, automatically extract evidence to `evidence_inventory.md` (no confirm gate in V1).

### Step 3 — Atomic evidence only

One evidence item = one atomic signal.

Forbidden:

```text
Observation: "Customers struggle with queue management."
Reason: synthesis
```

Allowed:

```text
Observation: "Critical projects wait several hours before scanning."
Source: workshop_queue.md
```

### Step 4 — Evidence contract fields

Each `EVID-NNN` item must include:

- `source_path`
- `source_kind`
- `evidence_type`: `quote` | `transcript_excerpt` | `image_observation` | `metadata_only` | `observation`
- `location` (when available)
- `companion_source` (for media transcripts)
- `observation`
- `relevance`
- `relevance_reason`
- `retrieved_by`

For `image_observation`, include `extraction_note`.

Canonical item:

```markdown
### EVID-001

- source_path: kb-samples/notes_2024/workshop_queue.md
- source_kind: markdown
- evidence_type: quote
- observation: "Critical projects wait several hours before scanning."
- relevance: scan queue latency
- relevance_reason: Direct wait-time claim for critical projects
- retrieved_by: local-knowledge-retrieval
```

### Step 5 — Media without transcript

If audio/video has no transcript:

- allow metadata-only stub
- do not invent content
- do not turn metadata-only into factual claim

## Required outputs

1. `RUN_DIR/outputs/discovery_preview.md`
2. `RUN_DIR/outputs/evidence_inventory.md`
3. `RUN_DIR/outputs/knowledge_retrieval_complete.marker`

Marker body (JSON):

```json
{
  "status": "completed",
  "completed_phase": "local_evidence",
  "next_phase": "business_context",
  "inputs": [
    "outputs/discovery_preview.md",
    "outputs/evidence_inventory.md"
  ]
}
```

## Review rules

- no evidence -> no claim
- no generalized observations
- no synthesis in retrieval step
- preserve traceability to source path and anchor
- next phase is Business Context, not Market
