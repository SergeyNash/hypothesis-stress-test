# Run quality and completion

Applies to every new full run. Read `FRAMEWORK_DIR/implementations/run-quality.md` before Business Context and again before Decision Review/Human Report. New runs use protocol 2 and a declared claim audit. Do not retrofit the protocol into old completed runs or silently rewrite their conclusions. Historical checks cover structural contracts only.

A full-run request authorizes continuation through Human Report. Phase summaries are progress updates, never invitations to approve the next ordinary layer. Pause only for an actual missing input, inventory completeness review, a user choice about heavy analysis, host permission, or an invalid prerequisite. Record the reason and resume the remaining full run afterwards. Use the input language for all user messages and reports.

Immediately after confirmed bootstrap and valid input run:
`python <FRAMEWORK_DIR>/scripts/run_control.py prepare --run-dir <RUN_DIR> --mode full`
Show the returned live URL immediately, before roles/retrieval. It verifies HTML and progress JSON over HTTP and run identity. If the host cannot keep the server alive, report that fact and give a separate-terminal serve command. Never silently omit the URL or claim an unverified viewer. On resume preserve configuration/history; use `viewer` to verify/restart the viewer. Do not change a legacy run to protocol 2 without an authorized upgrade.

Record `running` BEFORE starting each phase, source operations during work, and completion after gates. During long processing log meaningful milestones (file/sheet/batch and bounded counts), including whether waiting on a tool or the user. Do not emit fake percentage or estimated completion. Keep messages short, Russian for Russian input, technical tool output separate from user-facing progress. Continue the next layer without asking again.

After Human Report, write its canonical marker, then execute:
`python <FRAMEWORK_DIR>/scripts/run_control.py finish --run-dir <RUN_DIR>`
This writes `outputs/run_validation.json` with the actual target and errors. FAIL means repair that phase and stale downstream claims, then recheck; do not report 10/10 or completed. PASS covers contracts and declared audit consistency; it does not certify source truth or demand. A standalone `run_progress event` for Human Report completion performs the same current-run check. Finish updates the input status only on PASS.

Repository CI is a different check: `python scripts/validate_runs.py --examples`. Never cite that result as validation of a user run. For an explicit read-only check use `python <FRAMEWORK_DIR>/scripts/validate_runs.py --run-dir <RUN_DIR> --json`. Always report scope/target and material limits with PASS.
