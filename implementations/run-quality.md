# Evidence and decision audit for protocol 2

Maintain `outputs/claim_ledger.json` during Business Context/Market/Synthesis, and complete `outputs/quality_review.json` after Decision Review and Human Report. Start from `templates/claim_ledger.json` and `templates/quality_review.json`; replace every placeholder, never approve a checklist without reading source anchors. These artifacts supplement existing Markdown and canonical markers. Preserve EVID/EXT IDs.

Audit all decision-driving claims, every quantitative claim carried into the decision/report, and every claim of independent confirmation. `targets` bind a claim to an exact quote in each affected output. When a claim changes, update all affected outputs and targets before completion. A machine verifies declared consistency; the agent must actually reconcile the source text. Unlisted semantic mistakes are still possible: do not describe this as automated fact verification.

Each source has `id`, `kind`, `independence_group`, `scopes`. Kinds: customer_record, provider_record, primary_public, secondary_public, internal_analysis, simulation, search_log. Use the same independence group for a tender spreadsheet, DOCX summary and wiki page derived from that spreadsheet. Website domains alone do not establish independence. Register every EVID/EXT/CONF reference appearing in decision-driving outputs, even if used only as context. A persona/role output is simulation; never relabel it empirical.

Numerical source `facts` have `id`, `value`, `unit`, `period`, `population`, `metric` and a human-readable source anchor. Each numerical claim copies these fields into `numbers` with `source_id` and `fact_id`. Distinguish count of lots vs contract value vs NMC; tender/award/executed payment; total period vs one year; partial vs complete year. Different periods require explicit `temporal_comparison: true` and a bounded rationale. It does not authorize mislabelling a single-period total. Check the actual anchor and EVID binding, not just whether an ID exists. A falling count in a keyword sample cannot prove a shrinking market; rising NMC and partial-year coverage must be disclosed.

Claims have `id`, `kind` (fact/inference/gap/proposal), `scope`, `status` (supported/conditional/unknown/contradicted), `basis` (observed/derived/missing_evidence/simulation), `rationale`, `evidence_ids`, `independent_sources`, `targets` (artifact relative to RUN_DIR, exact quote), and optional `numbers`. Primary empirical support must match the scope; provider records alone do not establish customer willingness to pay. Missing evidence is unknown, never refuted. Conditional is not confirmed. An observed operating problem, current paid support, purchase of a wider project and demand for a new integrated SLA are distinct claims. Do not promote role consensus or an operating problem into confirmed demand for the proposed offer.

Bound negative search claims to actual languages, segments, queries and dates. No found offer is not global category absence or proof there is no competitor/time-window risk. Search logs are not empirical customer evidence. Never claim confirmed whitespace from an incomplete search.

The quality review must include each check below, `status: pass | not_applicable`, a substantive `reason`, and the relevant `claim_ids`. Unresolved failures stay `fail` and block completion; repair claims or report the unresolved phase. Not-applicable requires an actual reason.

| Check ID | Review question |
| --- | --- |
| source_lineage | Are reused summaries grouped with their originals, with no invented independent confirmation? |
| claim_references | Does each decision-driving claim cite the correct source and anchor, rather than merely an existing ID? |
| numeric_scope | Are units, periods, population, totals, sample limits and procurement status preserved? |
| simulations_not_evidence | Are roles used for questions/risks rather than empirical validation? |
| unknown_not_refuted | Does absence of evidence remain unknown, with bounded negative search claims? |
| original_intent | Is the original hypothesis preserved verbatim in the report, without inventing immediate mass launch intent? |
| decision_logic | Are false positive/negative consequences separated from unmeasured probabilities; do decision branches require evidence for all four service contours? |
| commercial_behavior | Does commercial validation seek actual commitments, budget owner/procurement/access and paid behavior rather than willingness to discuss price? |

Decision Review must read the original input and actual evidence sources, challenge earlier summaries, and correct upstream errors before exporting. Low confidence is not a low false-positive probability. A competitor offer does not validate our delivery/economics or authorize full launch. Experiments may test commercial demand and delivery separately, with a baseline, observable success/stop criteria, owner/date and explicit decision branches. Interviews are not automatically the only next action. Preserve unknown strategy/OKR status instead of inventing fit.

Human Report compiles corrected artifacts. Include the original hypothesis quote and what changed with traceable reasons. Do not turn weak support into a stronger headline. The final message leads with the verdict, confidence, supported vs unknown conclusions, coverage/limitations, next action and links; avoid technical tag counts, unverified security claims and English boilerplate for Russian runs.

## Audit version 2: grounded source contract

New `prepare` creates `protocol_version: 2, audit_version: 2`. The old protocol-2 audit remains explicitly version 1 for historical runs; it does not gain source verification by passing an updated binary. `validate_runs.py --run-dir <RUN_DIR> --strict --json` applies the new checks read-only to an older protocol-2 run. Missing bindings are failures, not permission to manufacture provenance or replace the original run. Do not alter audit_version on resume just to avoid or enable a gate. Regenerate affected artifacts only through an authorized rerun.

### Capture and retrieve

Before creating EVIDs, capture bounded, deterministic fragments:

```text
python <FRAMEWORK_DIR>/scripts/source_snapshot.py --run-dir <RUN_DIR> --root <KB_ROOT> --path <relative-file> --max-units 1000 --max-chars 100000
```

Repeat `--path` for files. The helper writes `outputs/source_snapshot.json` with file hash, source root/path, extraction status and limits, stable anchor IDs, raw text and location. It never interprets or executes source contents. It preserves DOCX body order, table cells and actual hyperlink targets. XLSX distinguishes literal values, `formula_cached` (saved, possibly stale; not recalculated), and `formula_not_evaluated` (no saved value). A formula is not automatically missing data. For partial reading use the reported `next_unit` with `--start-unit`; pages merge only for the same file hash. Do not omit table/appendix coverage or say an unread section has no relevant data. Give the usual quick/deep/skip choice before costly additional analysis; accepting partial reading limits conclusions.

For web/Confluence content, save the actual returned text with URL/title/access date in a run input attachment, then capture that file. Preserve links to actual query/read events. Local byte/fragment verification does not authenticate the remote publication or validate its factual truth. Do not write a model paraphrase and label it a raw tool response.

Each non-simulation source in claim_ledger has:
- `anchor_ids`: IDs from the generated snapshot;
- `quote`: an exact excerpt of one bound fragment;
- `role`: `reported_fact`, `author_inference`, or `context` (simulation uses `simulation`);
- existing kind, independence_group, scopes and facts.

Each EVID block also records `- anchor_ids: ["..."]` and `- source_quote: <exact excerpt>` plus its actual source_path and location. The validator checks the mapping, raw quote, captured file hash and fragment text against the still-available original. If the original file is unavailable, source reverification fails explicitly. Snapshot edits cannot make a wrong number pass. A citation to the right filename but wrong EVID/cell is not valid evidence.

Numeric facts add `value_anchor` (must belong to that source), `context_anchors` (headers/period/sample notes), and `question` (the business question measured). Preserve value/unit/period/population/metric. Year claims require an anchored year context. A numeric reported observation cannot be dropped from the fact model just because it weakens the preferred narrative. Bind claims' numbers to sources actually cited by that claim. Decision-driving target quotes must contain the substantive conclusion, never just a contour status line.

### Counterevidence and review

All eight original review checks remain, plus `counterevidence`, `entity_scope`, `procurement`, `research_execution`, `experiment_consistency`. Each needs actual reasoning and claim IDs. Read the source again when reviewing; a completed checkbox is not evidence.

`quality_review.comparisons` compares multiple numeric facts for each shared `question`: `fact_refs` as `SOURCE-ID/fact-id`, `relationship` (`different_populations`, `different_periods`, `conflicting`, `consistent`), `reason`, `impact_claim_ids`. A project conversion rate and the share of companies operating a production solution are different denominators; they cannot by themselves estimate installed base, support spend or reachable market size. Resolve the effect on the decision rather than choosing the convenient percentage. The validator verifies coverage of declared fact groups; semantic completeness remains the reviewer's responsibility.

The original Formulation section, including failure conditions, must appear verbatim in Human Report (HTML escaping/whitespace may differ). Label proposed reframing as a hypothesis and tie it to validated premises. Do not invent intent to launch mass sales immediately. Narrow lints flag categorical market-absence and pilot-rate-as-market-size phrases, including when the claim status says conditional. These lints are bounded checks, not general language understanding.

`quality_review.context` records `provider`, `client_scope`, `scope_status: verified | unknown`, `entity_review`, and `anchor_ids` when verified. Resolve organization vs subsidiary vs business unit explicitly. If a provider label joins names as aliases/affiliations, bind affiliation_anchor_ids to an actual source establishing the relationship; a slash is not proof of affiliation. A client list from one account meeting is a subset until completeness is established. A provider's public AI portfolio is not automatically the service team's available competence/capacity. Do not conflate two companies because both occur in the KB.

### Procurement and money

If procurement sources are used, `quality_review.procurement` normally contains unique `records` and checked `aggregates`; otherwise state `status: not_applicable` with a reason. A procurement-scoped source prevents skipping reconciliation.

Records have `procedure_id`, `id_anchor`, `segment`, `allocation_reason`, `year`, `publication_anchor`, and optional `nmc`, `nmc_anchor`. One ID appearing in several files is one procedure. Preserve occurrences/source anchors and explain the owning segment. Do not classify by filename alone when a mixed equipment/software/service procurement crosses levels. An ambiguous allocation is a gap, never silent double counting.

Each aggregate has `segment`, `metric: count | nmc`, `period`, unique `procedure_ids` and `value`. The checker recomputes counts/sums from the referenced records and rejects missing amounts, wrong segment, duplicate IDs and out-of-period records. Distinguish raw row counts, deduplicated procedure counts and sums by manually labelled service category. Pure maintenance, implementation and mixed contracts are separate questions; total NMC is not the support market, and NMC is not contract price or payment. For quick/partial reading use `status: reported_only`, `reason`, `fact_refs` (SOURCE-ID/fact-id of the raw reported totals), and `limitation_target` (exact output quote explaining that deduplication/allocation was not independently recomputed). Raw values/year/segment remain bound to source anchors. This does not certify checked totals or market size. It avoids forcing expensive full-register reconciliation after the user chose quick/skip.

Claims using commercial evidence declare `commercial_level: announcement | contract | payment | none`; contract/payment requires the corresponding `contract_anchor`/`payment_anchor`. A named supplier, completed procurement stage, signed proposal or issued invoice alone cannot certify payment. A failed procedure can coexist with supplier/contract-price fields: retain the inconsistency and inspect the contract card; never infer no contract solely from that label.

### Search execution and experiments

`quality_review.research` has `status: covered | partial | unavailable | declined`, `reason`; for searched coverage, `tracks` maps offers/procurement/operations/counterexamples to actual internet query_started event IDs and `read_event_ids` points to real read/used events with URLs. Start from local reference links/competitor names and continue residual gaps after page failure. Successful searches with zero results, access failures, and unavailable tools are distinct. A single guessed URL/404 is not a search. No invented quota-filling calls.

Unavailable/declined coverage names `exception_event_ids`, a real `blocker` (search_tool_unavailable/network_unavailable/host_permission/authentication for unavailability), and `limitation_target` binding the disclosed gap in an output. Do not relabel a 404 as a tool outage. Partial coverage retains actual tracks and an explicit limitation. Unsupported category absence cannot appear in conclusions even when a run completes with a genuine coverage gap.

`quality_review.experiments` records each decision-driving action with `id`, `owner`, `duration_days`, `stop_after_days`, `tests`, `success_observation`, `decision_branch`, `target` (exact plan quote), and exact duration_quote/stop_quote/success_quote from that target. The stop horizon cannot exceed the action deadline. Literal days/weeks/months in the plan are checked against declared days (calendar-month bounds are used, not a fabricated fixed month). Fixing JSON while leaving a six-month stop in an eight-week plan still fails. Payment success means funds_received/paid_invoice/bank_receipt, never signed_invoice. Preserve the same criterion and horizon in plan, decision and report; compare the actual texts in the review.

`quality_review.decision` binds `action` to service_decision and `contour_claim_ids` to four claims whose scopes/statuses equal the canonical contour fields. For limited_pilot, state `execution_allowed` and `conditions`. A proposed experiment may retain unknown contours; an authorized delivery additionally requires access_anchor, cost_cap_anchor, capacity_anchor, approval_anchor and stop_conditions. The framework cannot authorize service obligations for the human.

### Completion and limits

Use `run_control.py start --run-dir <RUN_DIR> --phase <phase>` before every layer; it initializes or recovers the viewer and returns its URL. For audit-v2 runs the first facilitator start checks live HTTP, not only a saved ready flag. If the host cannot maintain the viewer, report the actual error and separate-terminal command, then record `viewer-unavailable --reason <reported failure>`; do not silently skip progress or pretend the page is live.

`finish` preserves every validation attempt in `outputs/validation_history.jsonl` and the latest result in run_validation.json. Repair causes and affected outputs, not audit flags. PASS states the applied audit version and its limits. Source-bound consistency is stronger than self-declared JSON consistency, but cannot prove truth of a study, completeness of discovery/search, or absence of unmodelled semantic errors.

## Source selection

New runs require an explicit per-run choice of local KB / Confluence / internet before collection. See `.clinerules/45-source-selection.md`. `prepare` initializes the viewer before asking, so the user can open progress immediately. `sources-options` returns the current selection and a workspace-local proposal; `sources-set` confirms all three booleans, optional local folders and an actual-response reason. `--remember` saves only a proposal for future confirmation. `require-source` is the preflight guard for direct tools. `start`/source events/discovery with `--run-dir`/source snapshots enforce the saved choice. Preserve settings on resume and preserve earlier evidence after changing sources. `outputs/source_selection.md` contains the choice history; the final HTML discloses every disabled channel. Historical runs are not migrated automatically.


## Verified lifecycle for new runs

`lifecycle_version: 1` is recorded only on new prepare; existing runs are not silently upgraded. See `.clinerules/50-run-lifecycle.md` for the canonical agent procedure. Start each stage with `run_control.py start`, finish it with `run_control.py complete --phase <phase>`. `check-phase` checks current outputs without declaring completion. A canonical marker alone cannot bypass a missing journal completion. After interruption rerun complete; it verifies again and avoids duplicate completion events.

Stages use scoped checks: Local Evidence checks source snapshots/registered inventory/retrieval review; Business Context/Market/Synthesis check existing claims, original source bindings, research and context; Customer Discovery adds experiment checks; Decision Review adds the full quality review and service-decision contracts. Future artifacts are not required at earlier stages. The final `finish` validates the whole current run, creates the Human Report marker after success, and writes run_validation.json plus validation_history.jsonl. Internal checker errors are saved as ERROR. Intermediate checks use phase_validation.json and the same history with scope=phase. Each attempt starts with a persisted running record, allowing interrupted attempts to be distinguished. Unwritable storage remains an explicit operating error.

`prepare` creates empty source_snapshot/claim_ledger and the pending quality_review template before work starts. `audit_records.py source --run-dir <RUN_DIR> --record <UTF8_JSON_FILE>` validates the source kind, origin and generated anchor/quote binding; EVID records additionally carry an `inventory` object containing observation, relevance, relevance_reason, source_origin and evidence_status. The helper emits separate inventory fields and appends the source to the ledger. Use `audit_records.py claim` for valid claim enums, registered source refs, original-group counts and substantive target quotes. Registration does not replace semantic review: verify source entity, database/system scope, date, metric and the exact EVID. Domain-controller backup findings are not automatically PostgreSQL backup findings. No quotas, quotes or snapshots are fabricated to satisfy a validator.

Inventory headings `## EVID-...` and `### EVID-...` are both recognized; generated headings use ###. Every inventory EVID must be registered before leaving Local Evidence. Missing evidence belongs in gap claims rather than invented evidence sources. Internet query tracks reference internet/query_started events with actual query text; local/Confluence reads cannot fill those slots. Source selection remains the authority for which channels to access.

The HTTP progress response and terminal reconstruct state from journal events rather than trusting a stale progress.json. They show marker/journal disagreement without inferring completion. The terminal polls the published loopback URL independently of new events; prepare persists starting/error viewer states. These mechanisms make the URL discoverable without waiting for a late Cline summary, but cannot force Cline to display a chat message. On Windows the viewer and Tasks still require environment verification.

## Preparation handoff and audit scope

New runs use `phase_handoff_version: 1`: in full mode, the first source selection records Facilitator preparation; complete records preparation of the next untouched phase. start is idempotent when it is already running. Errors, waits and invalidations require explicit continuation and are not reset by a source-choice change. Phase mode has no automatic advance. complete/finish require a start since the last invalidation. Preparation includes reading stage instructions and planning; it never fabricates data-access events. Historical timelines remain unchanged.

`audit_scope.py` defines artifact ownership. Incremental claim, source and language checks use only current/prior artifacts and their bound claims; a future map cannot invalidate an earlier business-context gate. The final audit remains global. The affiliation lint is intentionally bounded to explicit provider identity fields with company-like names; roles, contour tokens and common technology stacks with slashes are excluded. It remains a heuristic, not a general semantic proof of corporate relationships.

A finished terminal reads the current run's persisted validation status and shows the human-report link. It does not say it is waiting for data or that the completed pipeline will continue. Reports that exist before final PASS are labelled unverified. This does not diagnose model reasoning before RUN_DIR/prepare; that interval still needs the Cline conversation/tool history.


## TUI-managed launches

A run with tui_request_id must retain outputs/tui_launch.json, tui_control.json and tui_events.jsonl. The request hash binds its original configuration; initial source history must match the submitted three booleans. Until an actual Cline acknowledge clears tui_request_pending, source access and automatic phase preparation remain blocked. Pending/unconsumed questions prevent final PASS. Run-local records permit archived validation without requiring the original workspace .hst directory. They record protocol consistency, not proof that a model understood or correctly implemented the instructions. See .clinerules/55-tui-control.md for the executor procedure and prototypes/bubbletea/README.md for installation/limitations.


## Optimization and timing (2.8)

Normal completion is one complete per output phase and one finish for Human Report. check-phase is diagnostic; repeated successful checks are not a required ritual. complete returns next_phase/next_prepared; omit a second start when the next phase is already prepared. Commands revalidate current/prior artifacts across calls. Within a single checked commit, an expiring in-memory receipt avoids rerunning the same semantic gate during marker/event writes and next-phase preparation. Final finish still executes one whole-run audit, including source/claim and TUI gates.

Use audit_records.py batch-claims with a UTF-8 JSON list for a phase's claims: validation is the same as single-claim registration, all claims are checked before a single ledger write and an invalid batch makes no partial write. Existing source registration and original-source anchors remain mandatory.

Measurements are passive for new timing_version 1 runs: command_metrics.jsonl records command/action/phase, origin, wall and process CPU, exit code and nested validation sections; raw arguments, document text and credentials are not recorded. performance_summary.json unions overlapping script/wait intervals, lists actual validation attempts and keeps unobserved time unattributed. CPU excludes child processes/LLM; final timing-file write overhead is excluded. Measurements have their own short lock and do not set PASS. A timing-write failure is reported separately without changing the validation outcome. Long-lived viewer, control-poll processes and standalone read-only validate_runs are excluded; the full validator called inside finish is measured. Historical archives remain unchanged; run_control metrics is an optional read-only diagnostic, not a pipeline step.

Control scenario and protocol: [benchmarks/pipeline-001](../benchmarks/pipeline-001/README.md). Real model-speed improvement is unmeasured until controlled before/after runs are supplied.
