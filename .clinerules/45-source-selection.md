# User choice of research channels

Applies to new runs with `source_selection_version: 1`. The explicit user choice takes precedence over default collection steps in skills/workflows. This rule governs all source access, including MCP/browser/search and shell/Python outside framework helpers. Historical runs without this version retain their existing scope; do not silently retrofit or reset choices on resume.

After confirming the hypothesis card and bootstrapping the run, call `run_control.py prepare` and show its actual progress URL immediately. Then run:

```text
python <FRAMEWORK_DIR>/scripts/run_control.py sources-options --run-dir <RUN_DIR> --workspace <KB_ROOT>
```

If there is no confirmed current selection, ask ONCE before data collection, in the input language: "Где искать данные: локальная база знаний, Confluence, интернет? Для каждого — да/нет. Для локальной базы: вся база или конкретные папки? Запомнить выбор для следующих прогонов?" Show a compact three-row table with the returned proposal. Accept a natural-language answer such as "локальные файлы и Confluence, без интернета". Do not silently interpret an omitted channel as yes; clarify only the ambiguous part. Ask about remembering only as an optional preference; do not block if the user already made the channel choice. A saved proposal is NOT current-run consent. The run's original hypothesis and framework instructions remain readable even if local research is disabled.

Persist the actual response, using yes/no for ALL channels:

```text
python <FRAMEWORK_DIR>/scripts/run_control.py sources-set --run-dir <RUN_DIR> --workspace <KB_ROOT> --local yes --confluence yes --internet no --reason "Пользователь выбрал локальную БЗ и Confluence, без интернета"
```

For selected folders repeat `--local-path "relative/folder"`; without folders, local=yes allows the full KB. Add `--remember` ONLY if requested. This creates a proposal in `.hst/source-preferences.json`, never global preferences. Do not put instructions, secrets or source contents into reasons. To modify an existing choice, use the same command with the full resulting set and the actual new request. Preserve already gathered evidence; disclose which material predates disabling a channel. Do not restart completed phases merely to change settings or automatically backfill re-enabled channels; incorporate new evidence through an authorized rerun with invalidation when needed.

Before EACH channel operation (discovery, query, read, download, extraction), use:

```text
python <FRAMEWORK_DIR>/scripts/run_control.py require-source --run-dir <RUN_DIR> --channel internet
```

Use confluence/local as appropriate. For local files/folders also pass `--path <absolute-path>`. Do not call the source if the command fails. For discovery use `discover_sources.py --run-dir <RUN_DIR> --root <allowed-folder>`; iterate selected folders, never scan the full KB first when restricted. `source_snapshot.py` enforces the local scope too. For captured remote responses pass `--channel confluence` or `--channel internet`; saving web responses as local attachments does not change their origin or authorize reading other KB files. Helpers without run context cannot enforce scope; perform the explicit guard before using them. Rules and helper checks are not an OS/network sandbox.

With a confirmed selection, continue ordinary phases without asking again. For a permitted but unavailable channel, record the actual tool failure and continue with explicit gaps. A single 404 is not a search outage. Ask only if a specific next step is impossible without changing scope. When every channel is disabled, do a bounded review of the supplied hypothesis, label role outputs synthetic and conclusions unverified; do not fabricate research. Keep canonical output contracts: write discovery_preview/evidence_inventory as explicit gaps, with retrieval review waived for user-disabled local collection; create an empty source_snapshot (`schema_version: 1, files: [], captures: []`) when no sources were captured. Do not skip phase markers or claim searches were made.

In `external_research.md` and `quality_review.research`, use declined for internet disabled from the start, with the actual declined event ID and limitation_target; no search tracks are required for that exception. If internet was used earlier and then disabled, keep the actual search/read history and disclose the earlier partial collection. Use declined for further collection with the new declined event and limitation_target, explicitly stating what was collected earlier; do not fabricate missing search tracks or claim no search happened.

Human Report must include a source coverage section referencing `outputs/source_selection.md`. For every currently disabled channel include exactly the applicable plain-text phrase (may be HTML-escaped):
- `Локальная база знаний — отключён пользователем`
- `Confluence — отключён пользователем`
- `Интернет — отключён пользователем`

Distinguish disabled, not yet checked, no results, partial, and access failure. Disabling channels narrows conclusions; it never turns missing evidence into counterevidence. Terminal/HTML progress display the saved choice; they do not themselves run research or change permissions.
