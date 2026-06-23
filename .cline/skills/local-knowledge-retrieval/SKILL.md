---
name: local-knowledge-retrieval
description: Discover traceable local evidence from a messy knowledge base before Market Layer. Produce discovery_preview.md and evidence_inventory.md with atomic evidence items only.
---

# Local Evidence Discovery

Collect a small, traceable set of local evidence artifacts.

This skill does not perform market interpretation.

## Purpose

`evidence_inventory.md` separates retrieval from analysis:

- Retrieval discovers evidence.
- Market Layer interprets evidence.
- Synthesis resolves contradictions.

## Prerequisites

- `RUN_DIR/input/hypothesis.md` exists
- `RUN_DIR` is provided by user
- Workspace root is the KB project root (recommended)

Optional input:

- `RUN_DIR/outputs/hypothesis_summary.md` (for relevance hints)

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

## Scan root and exclusions

Scan recursively from KB workspace root.

Exclude:

- `hypothesis-stress-test/`
- `runs/`
- `.git/`
- `.clinerules/`
- `.cline/`
- `node_modules/`

## Output language

Write output headings/body in the same language as `input/hypothesis.md`.

## Discovery process

### Step 1 — Build preview (always)

Write `RUN_DIR/outputs/discovery_preview.md` with:

- limits applied
- files scanned
- files skipped (with reasons)
- candidate files
- top relevant files with planned evidence type

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

For `image_observation`, include `extraction_note`:

- `derived from visible text in image`
- `derived from diagram labels and layout`
- `derived from whiteboard handwriting`
- `derived from image content (no readable text)`

### Step 5 — Media without transcript

If audio/video has no transcript:

- allow metadata-only stub
- do not invent content
- do not turn metadata-only into factual claim

## Required outputs

1. `RUN_DIR/outputs/discovery_preview.md`
2. `RUN_DIR/outputs/evidence_inventory.md`
3. `RUN_DIR/outputs/knowledge_retrieval_complete.marker`

Marker content:

```text
Local Evidence Discovery completed.
discovery_preview.md generated.
evidence_inventory.md generated.
Ready for Market Layer.
```

## Review rules

- no evidence -> no claim
- no generalized observations
- no synthesis in retrieval step
- preserve traceability to source path and anchor
