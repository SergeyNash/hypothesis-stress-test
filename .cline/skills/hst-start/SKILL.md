---
name: hst-start
description: Start an isolated HST run through dialogue in chat or TUI, without a controller preflight.
---

# New run: dialogue first

Use `FRAMEWORK_DIR/implementations/dialogue-run.md` for the small file bootstrap contract. FRAMEWORK_DIR is the installed framework, KB_ROOT the open workspace. Reading `.hst/workspace.json` is enough to resolve paths; do not inventory the workspace.

1. Distinguish a new hypothesis from explicit resume/comparison. A new request never reads previous `runs/*`, including inputs, reports, validation histories or ledgers. Only immediate folder NAMES may be listed to allocate a free ID. Do not recurse, count lines, inspect reference runs or copy their results. Repository historical examples are not runtime templates either. Use templates of the installed version.
2. Read the user's supplied hypothesis/settings and only intake/schema material needed for missing fields. Preserve their model label verbatim, or null if absent; Cline is a client, not a model. Do not guess provider/model/reasoning. Ask only essential missing questions. Show what is known, the choices and your recommendation. Accept an existing unambiguous authorization; no ritual confirmation phrase or repeated source question.
3. After authorization create a fresh run using native file tools, not shell/Python. Recheck that its name is unused. Save the confirmed card, minimal config, first journal event and explicit active pointer per dialogue-run.md immediately. This is preparation, not analysis completed. A TUI-submitted run already exists: use its supplied RUN_DIR, never allocate another.
4. Validate input meaning through `hypothesis-input-validation` using the card/schema, not by reading validator source. Record actual errors/waits in the new journal and ask a focused question. Never silently change the hypothesis. Record the three channel choices before any source access. Omitted choices are unknown, never consent.
5. Begin substantive work via hst-run. No `startup_progress`, `prepare`, `viewer`, `start`, `require-source` or audit initialization command is a prerequisite for a fresh dialogue run. Do not launch a server or read future checker code before work. Load each phase's instructions when needed.

Chat and TUI are two interfaces to the same dialogue. Honour an explicit preference for chat even when a bridge is installed. TUI transport may deliver settings/answers; it must not choose research steps. For submitted requests follow 55-tui-control; never claim acknowledged delivery before the real acknowledgement.

For explicit resume, read only the named RUN_DIR and its config. Dialogue runs continue through dialogue; lifecycle_version 1 archives retain their controller contract. Never upgrade/reset existing runs silently. Ask before replacing completed outputs or changing agreed scope.

Questions are for real choices: missing context, revised hypothesis, source scope, inventory review, heavy analysis or material blockers. Full-run authorization covers ordinary steps without per-phase approvals. On unavailable tools explain the actual limit and offer feasible alternatives.
