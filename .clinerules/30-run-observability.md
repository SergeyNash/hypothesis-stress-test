# Run observability

Resolve FRAMEWORK_DIR by its actual location (may be nested/renamed); KB_ROOT is the open workspace. Use absolute paths or a resolved prefix for scripts, templates, profiles, layers and contracts. A copied `.cline`/`.clinerules` directory does not make templates/scripts exist at KB root.

For new chat-first runs, hst-start must first publish `.hst/startup.json` through `startup_progress.py start` before intake/profile analysis. Record actual preparation, confirmation waits, errors and cancellation there. No HYP folder or fictional phase completion is required. After confirmed bootstrap use startup_progress.py attach before input validation; it preserves early timestamps and activates the new run. See hst-start for commands.

For validated new runs use `run_control.py prepare` as required by `40-run-quality.md`; it initializes the viewer and verifies HTTP/JSON before returning its URL. For manual/legacy recovery, once a run is bootstrapped, initialize `python <FRAMEWORK_DIR>/scripts/run_progress.py init --run-dir <RUN_DIR>`. Start `serve` in a host-supported background terminal bound only to 127.0.0.1; show the actual URL printed by it. No external server/deployment. Do not block pipeline execution waiting for a foreground server process. If the host cannot keep a background terminal, give the command for a separate terminal and continue updating the journal. Do not claim live view is running until the URL is observed.

For lifecycle_version 1, use run_control start/complete for stage transitions (50-run-lifecycle.md); do not hand-write completion markers. For milestone updates, waits, failures, and legacy transitions use:

```text
python <FRAMEWORK_DIR>/scripts/run_progress.py event --run-dir <RUN_DIR> --phase <phase> --state running|waiting_user|completed|error|invalidated --message "<short localized action>"
```

Phases: intake, validation, facilitator, local_evidence, business_context, market, synthesis, customer_discovery_planning, decision_review, human_report. Workspace startup status precedes bootstrap; run-local journal initialization follows confirmed bootstrap, before validation. Show waits in chat and update the corresponding startup/run state. Record intake completed only after confirmed input exists. Record completed only after checking artifacts and canonical markers; the helper rejects missing/invalid markers. At the inventory review write local_evidence waiting_user; after user's continuation write running, then completed after its marker is verified. Source errors need not fail the entire phase, but must remain explicit gaps.

For every actual source operation, log before and after:

```text
python <FRAMEWORK_DIR>/scripts/run_progress.py event --run-dir <RUN_DIR> --phase market --channel confluence --state query_started --query "<actual query>" --message "Ищу внутренние материалы"
python <FRAMEWORK_DIR>/scripts/run_progress.py event --run-dir <RUN_DIR> --phase market --channel confluence --state found --query "<actual query>" --message "Найдено 3 страницы" --url "https://..."
```

Channels: local, confluence, internet. States: query_started, found, read, used, completed, no_results, partial, unavailable, auth_error, error, waiting_approval, declined. Record `read` only after opening/reading a document and `used` only with its EVID/EXT reference to the actual analysis. Include counts/paths in the message, URLs in --url (repeat as needed), and the real query. Never log secrets, credentials, headers or raw private document content. Never claim planned calls are executed. A tool unavailable, a 401 and zero results are distinct outcomes. No events means “not recorded”, not “no results”.

If host approval is needed, log waiting_approval and explain the blocking operation. Declined requires actual refusal. Notify about 401/403 immediately, stop repeated authentication attempts and offer restore-or-continue. Do not request credentials in chat.

Resume: load existing events, preserve history. Do not replay completed phases as new searches. Existing canonical markers without journal history are legacy completion claims: verify artifacts, then record phase completion with message “Verified prior artifacts; source call history unavailable”. Do not invent source events. For an authorized rerun mark affected downstream phases invalidated before execution, invalidate their canonical markers through the existing safe-write flow, and preserve old files until replacement is authorized. With no authorization, keep old completion and stop without changes.

If a progress write fails, say the viewer is stale and show current action in chat; do not imply the log is complete. Do not use progress JSON as a replacement for canonical markers. The viewer shows time since last event; elapsed time is not proof of a hung process or an ETA.

Final response: lead with the verdict, confidence, evidence coverage/limitations and next action; link human_report.html and progress view/journal. Distinguish execution completed from research completeness. Marker counts and HTML tag checks are technical validation, not the main result.

## Dedicated VS Code terminal viewer

If installed with `setup_workspace.py --terminal`, the workspace has the task `HST · Прогресс`. It runs `terminal_progress.py --workspace <KB_ROOT>` and waits for `.hst/active-run.json`. The startup session is visible before any pointer exists. After confirmed bootstrap, attach publishes the pointer before input validation; normal prepare republishes it after validation, before HTTP startup. Do not start another foreground watch loop inside Cline's command terminal or spawn external PowerShell windows. For the first launch in an already-open workspace, tell the user Terminal → Run Task → HST · Прогресс; later folder-open launches depend on the user's normal VS Code automatic-task permission. Do not claim that Python launched a VS Code tab or that an installed task is running without observation.

When explicitly selecting/resuming a run, use `run_control.py activate --run-dir <RUN_DIR>` once (custom layouts: --workspace <KB_ROOT>). Never guess the active run from directory timestamps. A new selection clears old state while waiting for its journal; a stopped terminal does not stop the run. Installation and recovery: implementations/terminal-progress.md. `.hst` contains runtime state/environment and is excluded from evidence discovery.
