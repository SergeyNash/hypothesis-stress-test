---
name: external-business-research
description: Research public business and market evidence for an HST hypothesis during Business Context; investigate companies, demand triggers, procurement, alternatives and disconfirming facts with a source ledger.
---

# External business research

Run during Business Context after local-source review and before its completion marker. Full stress-test requests include passive public research unless the user explicitly excludes it. This does not authorize sending messages, purchases or access to private systems. Respect host tool permissions; do not invent an additional framework approval gate. If host approval is pending, show and log waiting_user; a missing answer is not refusal.

Read hypothesis, local inventory, role questions, and available business context. Write `RUN_DIR/outputs/external_research.md` in the input language. Never send confidential file contents or client identifiers in queries without authorization; derive generic topic queries. Use only available search/read tools. If unavailable, record unavailable, explain the gap and continue with limited coverage. Never replace search with model recollection.

## Research brief before searching

Record the question, decision it informs, geographic/segment/time scope, existing knowledge, key gaps, and confirming/disconfirming queries. Distinguish two tracks:

- Market: existing service offers and boundaries, buyer problems, actual procurement/contract status, current alternatives, prices only where comparable and dated. Do not infer demand from vendor marketing or add overlapping tender sums.
- Companies, where relevant to the hypothesis: use B2B infrastructure research. Resolve legal entity/group, domain, region and period. Investigate business change → IT requirements → infrastructure change → operational pressure → capability gap → possible service need. Validate each transition separately; identify internal resources and existing suppliers. A vacancy, technology mention, tender or growing infrastructure alone does not establish unmet demand.

For named companies use the installed `b2b-infrastructure-osint` skill if available, applying the same evidence contract. Otherwise use the company protocol above and report the bounded screening scope; do not claim to have run an unavailable skill. Market-level research is required even when no named companies are supplied. Do not demand company names to start a market hypothesis.

## Search execution and stop criteria

Start with primary sources (company disclosures, official procurement and award documents, product/service documentation, original research). Read pages, not search snippets alone. Search counterexamples and reasons a current supplier/internal team already solves the problem. Aim for two independent sources, at least one primary, for critical claims; reprints are one source. Stop when each critical question has evidence or a documented gap; default budget: 12 queries / 20 read pages. Record the actual budget and any truncation. No arbitrary market size extrapolations.

## Output

1. Research brief and actual coverage/status: searched, no_results, partial, unavailable, declined or waiting_approval.
2. Query/read log with actual timestamps and outcomes, including failed requests.
3. Source ledger: EXT-ID, claim, fact/indirect signal/inference/hypothesis, event date, publication date, accessed date, URL/title, quality, independence, relevance, limitations, what weakens the claim.
4. Market findings and alternatives; company signal table and causal chains when company screening was done. State confirmed/partial/assumed/refuted on each causal transition.
5. Two to four testable need hypotheses with evidence IDs, unconfirmed link, confidence and suitable interview role; five to eight neutral validation questions linked to those hypotheses when warranted.
6. Contradictions, unresolved questions, and handoff to Business Context/Market. Public evidence cannot establish our internal strategic priorities or replace customer validation.

Log actual tool calls and outcomes in the pipeline event journal; never record completed search before the tool returned. Report page discovery, page reading, and evidence use as separate actions. Market reuses EXT-IDs and sources; only search residual gaps instead of rerunning the same queries. Proposed interviews and pilots remain future work.
