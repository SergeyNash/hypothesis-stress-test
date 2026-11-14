# New dialogue runs: precedence

For execution_driver `dialogue`, follow implementations/dialogue-run.md. Native file operations record the card/config, source consent, real journal events and canonical markers after actual checks. Do not run controller prepare/start/complete or a per-operation require-source command. Inspect the saved channel choice and local scope before every native/tool/source operation; extraction helpers still enforce scope internally. Use read-only artifact checks after writing the relevant output; --save-report records only their real diagnostic, never advances a phase. No technical PASS decides the business outcome. Chat and TUI carry the same focused questions, recommendations and answers. Do not ask again for already-agreed work. Monitoring is optional and independent; absence of HTTP must not block analysis. For a TUI-bound run, the existing acknowledge/ask/consume calls are delivery operations, not analytical phase prerequisites or decisions. No startup/controller loop is added around them.

The section below documents compatibility for existing lifecycle_version 1 archives and legacy tools. It is not the startup procedure for fresh dialogue runs.

# Run quality and completion

Applies to every new full run. Read `FRAMEWORK_DIR/implementations/run-quality.md` before Business Context and again before Decision Review/Human Report. New runs use protocol 2 with audit_version 2 and the source-bound contract in implementations/run-quality.md. Historical audit_version 1 checks declared consistency only. Do not retrofit the protocol into old completed runs or silently rewrite their conclusions. Historical checks cover structural contracts only.

A full-run request authorizes continuation through Human Report. Phase summaries are progress updates, never invitations to approve the next ordinary layer. Pause only for an actual missing input, the initial source selection, inventory completeness review, a user choice about heavy analysis, host permission, or an invalid prerequisite. Record the reason and resume the remaining full run afterwards. Use the input language for all user messages and reports.

Immediately after confirmed bootstrap and valid input run:
`python <FRAMEWORK_DIR>/scripts/run_control.py prepare --run-dir <RUN_DIR> --mode full`
Show the returned live URL immediately, before roles/retrieval. It verifies HTML and progress JSON over HTTP and run identity. If the host cannot keep the server alive, report that fact and give a separate-terminal serve command. Never silently omit the URL or claim an unverified viewer. On resume preserve configuration/history; use `viewer` to verify/restart the viewer. Do not change a legacy run to protocol 2 without an authorized upgrade.

Use `run_control.py start --run-dir <RUN_DIR> --phase <phase>` BEFORE starting each phase; it returns/rechecks the viewer. Record `running` BEFORE starting each phase, source operations during work, and completion after gates. During long processing log meaningful milestones (file/sheet/batch and bounded counts), including whether waiting on a tool or the user. Do not emit fake percentage or estimated completion. Keep messages short, Russian for Russian input, technical tool output separate from user-facing progress. Continue the next layer without asking again.

For lifecycle_version 1, complete each phase via run_control.py complete as specified in 50-run-lifecycle.md. After generating Human Report, execute:
`python <FRAMEWORK_DIR>/scripts/run_control.py finish --run-dir <RUN_DIR>`
This writes `outputs/run_validation.json` with the actual target and errors. FAIL means repair that phase and stale downstream claims, then recheck; do not report 10/10 or completed. PASS covers contracts and declared audit consistency; it does not certify source truth or demand. A standalone `run_progress event` for Human Report completion performs the same current-run check. Finish updates the input status only on PASS.

Repository CI is a different check: `python scripts/validate_runs.py --examples`. Never cite that result as validation of a user run. For an explicit read-only check use `python <FRAMEWORK_DIR>/scripts/validate_runs.py --run-dir <RUN_DIR> --json`. Always report scope/target and material limits with PASS.
