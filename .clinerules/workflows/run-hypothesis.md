# Run Hypothesis (Full)

End-to-end and resumable hypothesis stress test for a single `RUN_DIR`.

## Preflight and resume plan

Before executing or writing anything:

1. Resolve `RUN_DIR` and validate `input/hypothesis.md` with
   `/validate-hypothesis-input.md`. Stop on `validation: fail`.
2. Read every phase marker as JSON and compare it with the per-file object in
   `.clinerules/10-artifact-contracts.md`. Presence alone is not completion.
3. For each phase in canonical order, verify:
   - marker JSON has expected `status`, `completed_phase`, `next_phase`, and
     `inputs`;
   - status is allowed for that marker (`completed`, plus
     `skipped_missing_context` only for Business Context);
   - every required artifact named by `inputs` exists and is usable;
   - the preceding phase has an allowed canonical marker/status.
4. Classify each phase:
   - **completed** — canonical marker, allowed status, valid prerequisites and
     required artifacts;
   - **incomplete** — no marker;
   - **invalidated** — canonical JSON marker exists but its fields, status,
     prerequisites, or artifacts are inconsistent;
   - **non-canonical** — malformed JSON or a legacy/free-text marker body.
5. Skip the contiguous completed prefix. The resume point is the first
   incomplete, invalidated, or non-canonical phase. Later markers do not make an
   earlier gap complete.

Show a resume summary before execution:

```yaml
RUN_DIR: runs/HYP-...
validation: pass
completed_phases: [...]
resume_phase: facilitator | local_evidence | business_context | market | synthesis | customer_discovery_planning | decision_review | human_report | none
resume_reason: incomplete | invalidated | non-canonical | all_completed
planned_action: concise localized description
overwrite_candidates: [...]
confirmation_required: true | false
```

If every phase is completed, do not rerun; go directly to **Report**.

## Safe write and migration rules

- A missing marker with no existing phase outputs may run without extra
  confirmation after the resume summary.
- Before overwriting any existing output, rerunning a completed phase, or
  rerunning an invalidated phase, obtain explicit confirmation naming the phase
  and files at risk. Without confirmation, stop without writes.
- Never silently trust, migrate, delete, or overwrite malformed/free-text
  legacy markers. Explain that they are non-canonical and ask the user to choose:
  **migrate marker after artifact verification**, **rerun phase**, or **cancel**.
  Migration and rerun both require explicit confirmation.
- Marker migration may only write the exact JSON body defined in
  `.clinerules/10-artifact-contracts.md` after all claimed prerequisites and
  artifacts have been verified. Otherwise offer rerun or cancel.
- If the user explicitly requests a rerun of a completed phase, include all
  downstream phases that become stale in the confirmation and resume plan.
- Never infer completion from output files alone.

## Steps

1. **Validate input**
   - Invoke `/validate-hypothesis-input.md` or skill `hypothesis-input-validation`.
   - Stop if validation fails.
   - Then perform the marker/artifact preflight above and summarize the planned
     resume point.

2. **Facilitator (Roles Layer)**
   - Run only when it is the resume phase; otherwise skip as completed.
   - Activate skill `hypothesis-facilitator`.
   - Produce `role_outputs/*`, `hypothesis_summary.md`, `validation_questions.md`, `ready_for_synthesis.marker`.
   - Show user a brief summary (assumptions, conflicts) before continuing.

3. **Local Evidence Discovery**
   - Require `ready_for_synthesis.marker` with canonical `status: completed`.
   - Activate skill `local-knowledge-retrieval`.
   - Produce `discovery_preview.md`, `evidence_inventory.md`, `knowledge_retrieval_complete.marker`.
   - Show user retrieval summary (scanned/skipped/items) before continuing.

4. **Business Context & Value Check**
   - Require `knowledge_retrieval_complete.marker` with canonical
     `status: completed`.
   - Activate skill `business-context-value-check`.
   - Produce `business_context_analysis.md` or `missing_business_context.md`, `business_context_complete.marker`.
   - Show user stakeholder map and strategic fit (or KB gap) before continuing.

5. **Market Layer**
   - Require `business_context_complete.marker` with canonical status
     `completed` or `skipped_missing_context`.
   - Activate skill `hypothesis-market-layer`.
   - Read `evidence_inventory.md` first for KB-local signals.
   - Then search Confluence MCP for internal wiki signals.
   - Produce `market_analysis.md`, `market_analysis_complete.marker`.
   - Show user signal summary before continuing.

6. **Synthesis Layer**
   - Require `market_analysis_complete.marker` with canonical
     `status: completed`.
   - Activate skill `hypothesis-synthesis`.
   - Produce `hypothesis_map.md`, `hypothesis_digest.txt`, `synthesis_complete.marker`.

7. **Customer Discovery Planning**
   - Require `synthesis_complete.marker` with canonical `status: completed`.
   - Activate skill `customer-discovery-planning`.
   - Produce `customer_discovery_plan.md`, `customer_discovery_planning_complete.marker`.
   - Show user critical unknowns and high-priority interview targets.

8. **Decision Review**
   - Require `customer_discovery_planning_complete.marker` with canonical
     `status: completed`.
   - Activate skill `hypothesis-decision-review`.
   - Produce `decision_review.md`, `decision_review_complete.marker`.
   - Show user confidence and recommendation before continuing.

9. **Human Decision Report Export**
   - Require `decision_review_complete.marker` with canonical
     `status: completed`.
   - Activate skill `human-report-export`.
   - Produce `human_report.html`, `human_report_complete.marker`.
   - Show user path to `human_report.html` and decision readiness summary.

10. **Report**
   - Display `hypothesis_digest.txt` and key verdict from `decision_review.md`.
   - Point user to `outputs/human_report.html` as the main human-facing decision report.
   - Remind: human makes the final backlog decision.

After each newly executed phase, re-read its JSON marker and required outputs.
Stop at that phase if verification fails; do not proceed to downstream phases.

## Expected time

5–15 minutes per hypothesis.

## Reference

See `playbooks/run-hypothesis.md` for interpretation model and tips.
