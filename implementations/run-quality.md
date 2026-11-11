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
