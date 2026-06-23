# Local Evidence Discovery

Local Evidence Discovery is a pre-Market retrieval step.

It discovers traceable local evidence from a messy KB and writes structured retrieval artifacts.

---

## Purpose

Separate retrieval from analysis:

- Discovery collects evidence.
- Market Layer interprets it.
- Synthesis collides interpretations.

This prevents retrieval from becoming a mini-Market Layer.

---

## Inputs

Required:

- `RUN_DIR/input/hypothesis.md`

Optional:

- `RUN_DIR/outputs/hypothesis_summary.md`

---

## Outputs

- `RUN_DIR/outputs/discovery_preview.md`
- `RUN_DIR/outputs/evidence_inventory.md`
- `RUN_DIR/outputs/knowledge_retrieval_complete.marker`

---

## Core rules

- one evidence item = one atomic signal
- no synthesis in observations
- no evidence -> no claim
- preserve source traceability

---

## V1 guardrails

- bounded scan and extraction
- extension whitelist
- binary skip by default
- explicit skipped reasons
- preview is always generated first
- extraction auto-continues after preview

---

## Relationship with Market Layer

Market Layer consumes `evidence_inventory.md` as a local evidence input.

Market output keeps channels separated:

- Local Signals from Knowledge Base
- Confluence Signals
- External Market Signals
- Inferred Signals

---

## Non-goals

- not a chatbot over documents
- not a full-vault semantic search system
- not a source confidence scoring engine
