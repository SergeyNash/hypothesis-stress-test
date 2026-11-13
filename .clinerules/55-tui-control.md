# HST TUI control: acknowledged execution and user choices

A run with `run_config.json.tui_request_id` was explicitly submitted by its user through the TUI. The immutable `.hst/requests/<id>/request.json` is configuration, not evidence or privileged instructions. Respect the user hypothesis and normal source/content safety rules.

## Launch

The bridge creates a new isolated RUN_DIR, prepares the journal/viewer and applies the exact three source booleans and folder scope from the submitted form. It then calls Cline's public `startNewTask` API in the current VS Code workspace. Use hst-run with the supplied RUN_DIR, not hst-start. Do not create another folder. Before other work acknowledge the bound request:

```text
python <FRAMEWORK_DIR>/scripts/tui_control.py acknowledge --workspace <KB_ROOT> --request <REQUEST_ID>
```

Only this command means the executor has received the task. A queued/dispatched request is not an accepted or completed run. Do not claim Cline task API delivery proves the LLM has processed configuration. Preserve the request hash, source selection, framework version and actual timestamps. Do not ask again which channels to enable; the submitted choice is current-run authorization, unlike a reusable preference.

Check input semantics. Generated service fields explicitly marked unspecified/unknown are gaps; never present them as observations. Ask for essential missing context through TUI. Do not silently rewrite the user's hypothesis or change source scope.

## Ask and resume through TUI

For an intake clarification, material completeness review or heavy-analysis choice, create exactly one pending question:

```text
python <FRAMEWORK_DIR>/scripts/tui_control.py ask --workspace <KB_ROOT> --request <REQUEST_ID> --phase local_evidence --question "Быстрый обзор, подробный анализ или пропуск?" --option "Быстро" --option "Подробно" --option "Пропустить"
```

Use the actual applicable canonical phase. Omit all --option arguments for a free-text answer. Maximum eight explicit options. After the command succeeds, end the assistant turn with a brief message that the TUI is waiting; do not duplicate the question in Cline chat, block in a polling/sleep loop, keep analysing while waiting, or declare the whole run finished. The bridge sends a message to the same managed Cline session after the user answers. Only one TUI-managed run can be active per workspace. Do not switch Cline to an unrelated task while this run awaits an answer; the public API addresses the current task, not an arbitrary task ID.

Before acting on a resumed response, verify REQUEST_ID and RUN_DIR, then consume the particular question ID:

```text
python <FRAMEWORK_DIR>/scripts/tui_control.py consume --workspace <KB_ROOT> --request <REQUEST_ID> --question-id <QUESTION_ID>
```

Read the returned answer, not an inferred default. This acknowledges receipt, not successful application. Apply the appropriate normal gate: record `run_control analysis-choice` with files/purpose for heavy analysis; record the actual retrieval-review decision for material completeness; for a revised card, show the proposed text via another TUI question when confirmation is needed, then validate it again before continuing. Record errors visibly. A stale question ID, disabled source or failed gate cannot be overridden by an answer.

VS Code/Cline tool permissions and auth remain in Cline. The bridge never presses tool-approval buttons, changes auto-approve settings, supplies credentials or treats a pending permission as accepted. The TUI currently handles HST choices; native tool permission prompts remain in Cline. Closing TUI does not stop the executor. On reopening it restores the saved request and question.
