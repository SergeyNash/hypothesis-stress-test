---
name: hst-run
description: Conduct one HST run through dialogue; use scripts for data operations and checks of already-produced artifacts.
---

# HST: one isolated run

For fresh runs use execution_driver `dialogue` and the contract in `FRAMEWORK_DIR/implementations/dialogue-run.md`. This takes precedence over legacy controller instructions in phase skills/playbooks. For existing lifecycle_version 1 runs preserve the old protocol described in 50-run-lifecycle; no silent migration.

Resolve one RUN_DIR. Read only this run, installed instructions/templates and user-authorized sources. Never inspect other archives to learn their schema or imitate successful output. Source permission applies to native reads/search/MCP as well as Python; whole-KB searches must exclude runs, .hst, framework copies and environments. Prior outputs are not independent evidence.

Validate the hypothesis semantically, preserve its confirmed wording, and clarify essential gaps through dialogue. No Python/scripted preflight is required before substantive work. No viewer/HTTP acknowledgement is a prerequisite for research. An installed monitor reads files independently; say only what is actually observed.

## Work by phase

Load detailed instructions just in time. Existing substantive requirements and canonical output names stay applicable:

| Phase | Skill |
| --- | --- |
| facilitator | hypothesis-facilitator |
| local_evidence | local-knowledge-retrieval |
| business_context | business-context-value-check |
| market | hypothesis-market-layer |
| synthesis | hypothesis-synthesis |
| customer_discovery_planning | customer-discovery-planning |
| decision_review | hypothesis-decision-review |
| human_report | human-report-export |

Resolve actual skill folders by name if a shorthand differs; do not search old runs. Record actual starts/waits/errors/completions using file tools and the existing JSONL event schema. Load audit templates only when producing artifacts that need them. Missing context stays a gap; role simulation is never empirical evidence.

At a decision show findings/uncertainty, available options and a reasoned recommendation. Ask in the selected channel (chat or TUI), save the exact reply and its effect in run.md. Already-authorized routine work continues without another approval. A technical check reports consistency issues; it never chooses a product/service decision or automatically starts the next phase. If changing scope or overwriting results is needed, ask before doing so. Never downgrade audit requirements to obtain PASS.

## Scripts are tools

Use a script only for a concrete task: extraction/large-data processing, grounding records against real sources, calculations, or checking an artifact that already exists. Respect the agreed heavy-analysis choice. No speculative checker exploration, repeated whole-project scans, waiting commands, artificial FAILs or defect-injection tests during a user run.

After producing a phase's artifacts, use `validate_runs.py --run-dir <RUN_DIR> --phase <phase> --save-report --json` once. It checks outputs and saves the actual result, without moving the workflow. A FAIL is a diagnostic: explain the cause, repair within agreed scope or discuss a real choice; preserve failure history. After PASS write that phase's canonical marker from 10-artifact-contracts and completed event with file tools. For skipped business context use the checker's completion-status option and its matching marker. Never announce PASS without the observed tool result.

For Human Report, run only `validate_runs.py --run-dir <RUN_DIR> --pending-report --save-report --json`. After PASS write the final canonical marker, completion event, input status completed and run_state/ended_at. FAIL leaves the run unfinished. Final audit covers all existing contracts/source-bound checks, not source truth or market demand. Report recommendation, confidence, evidence limits and next action; link the HTML and actual validation result. A final service/product decision remains in dialogue.

Directly registered claims must satisfy the same grounded audit. Batch registration is useful after the relevant text exists; initialize/copy the empty audit templates only then, never as a startup prerequisite. Preserve archived timestamps and real tool failures. Historical runs are not evidence templates.
