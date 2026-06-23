# Local Evidence Discovery Prompt

This is an execution template, not a system prompt.

RUN_DIR: [set your run directory]

---

## Inputs

Read:

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/hypothesis_summary.md` (if present)

---

## Task

Discover local evidence from the KB workspace before Market analysis.

Do not interpret market implications.

Do not synthesize conclusions.

---

## Guardrails (V1)

- max_files_scanned: 200
- max_file_size: 2 MB
- max_evidence_items: 20
- skip_binary_by_default: true

Supported kinds:

- markdown/text
- images
- transcript files
- audio/video only with companion transcript (or metadata-only stub)

Skip in V1:

- pdf/docx/html/pptx/xlsx

Exclude directories:

- `hypothesis-stress-test/`
- `runs/`
- `.git/`
- `.clinerules/`
- `.cline/`
- `node_modules/`

---

## Step 1 — Preview (always)

Write `RUN_DIR/outputs/discovery_preview.md`:

- limits applied
- files scanned
- files skipped + reason
- candidate files
- top relevant files + planned evidence type

Then continue automatically (no manual confirmation gate in V1).

---

## Step 2 — Evidence inventory

Write `RUN_DIR/outputs/evidence_inventory.md`.

Each item:

- `EVID-NNN`
- one atomic signal only
- source path and anchor
- no synthesis language

Required fields:

- source_path
- source_kind
- evidence_type (`quote` | `transcript_excerpt` | `image_observation` | `metadata_only` | `observation`)
- observation
- relevance
- relevance_reason
- retrieved_by

Additional:

- location
- companion_source
- extraction_note (required for image_observation)

Forbidden example:

```text
Observation: "Customers struggle with queue management."
```

Allowed example:

```text
Observation: "Critical projects wait several hours before scanning."
Source: workshop_queue.md
```

---

## Step 3 — Completion marker

Write:

`RUN_DIR/outputs/knowledge_retrieval_complete.marker`

---

## Important

- no evidence -> no claim
- metadata_only cannot become factual claim
- if no extractable evidence exists, state gap explicitly
