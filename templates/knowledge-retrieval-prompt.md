# Local Evidence Discovery Prompt

This is an execution template, not a system prompt.

RUN_DIR: [set your run directory]

---

## Inputs

Read:

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/ready_for_synthesis.marker` (`status: completed`)
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
- Skip unsupported binaries only; PDF/DOCX/XLSX are supported.

Supported kinds:

- markdown/text
- images
- transcript files
- audio/video only with companion transcript (or metadata-only stub)

Read PDF/DOCX/XLSX/HTML with scripts/extract_evidence.py; keep anchors and extraction limits. Skip unsupported binaries (including PPTX).

Exclude directories:

- `hypothesis-stress-test/`
- `runs/`
- `.git/`
- `.clinerules/`
- `.cline/`
- `node_modules/`

---

## Step 0 — Catalog before selecting

Resolve the actual framework directory, including downloaded ZIP names. Run its `scripts/discover_sources.py --root <KB_ROOT> --query "<topic terms>"`. Review nested folder/file names before exclusions. Hypotheses/growth/development/ideas/strategy/research and Russian equivalents are priority hints. Do not reject a parent business folder without checking descendants. Record metadata limits/errors separately from extraction limits. Include input/attachments explicitly; keep generated outputs excluded.

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

## Prerequisites

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/ready_for_synthesis.marker` (`status: completed`)

If `RUN_DIR/kb-samples/` exists, scan it first.

---

## Step 3 — Completeness review

After inventory, show scope/read/skipped/partial files and gaps. Ask whether the user wants to add materials or point out a missed folder; wait for additions or Continue. Process additions and repeat. Record `Retrieval Review` with `status: accepted` (or `waived` only for an explicit prior instruction). While pending, no retrieval completion marker and no Business Context. On late additions, invalidate downstream results through the authorized rerun flow.

## Step 4 — Completion marker

Write canonical JSON from `.clinerules/10-artifact-contracts.md` to
`RUN_DIR/outputs/knowledge_retrieval_complete.marker`.
`next_phase` must be `business_context`.

---

## Important

- no evidence -> no claim
- metadata_only cannot become factual claim
- if no extractable evidence exists, state gap explicitly

## Application profile

Resolve Application Profile from input Metadata (default digital_product). For service_business apply [service-business.md](../profiles/service-business.md) for this phase before the generic template. Preserve unknowns, separate customer/provider, and use the existing output paths.
