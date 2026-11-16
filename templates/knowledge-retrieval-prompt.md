# Local Evidence Discovery — Manual Prompt

Read the current hypothesis and agreed source scope in run.md. Select a small set of relevant materials with available client tools. Do not inventory the entire project or use previous runs as templates.

Write `RUN_DIR/outputs/discovery_preview.md`: where you searched, the selected materials and why, unread candidates and limitations. Names and paths help selection but do not prove content.

Read the selected materials directly. For PDF/Word/Excel use the client's supported readers; if unavailable, disclose the gap and propose an export. Do not install parsers, write shell/PowerShell/Python extractors or text-checking commands, create temporary TXT exports, or serialize the KB before analysis. Before expensive processing or materially expanding scope, explain the cost and agree on depth.

Write `RUN_DIR/outputs/evidence_inventory.md` as useful Markdown. For each actual finding preserve the source path/URL, location when available, exact short quote or observation, relevance to the hypothesis and limitations. Include date/period/sample if known. Optional EVID IDs help later citations; no machine schema is required.

Do not treat metadata as reading, repeated copies as independent evidence, simulated roles as observations, or missing data as a negative result. Keep customer and provider evidence distinct. For service_business apply [the service profile](../profiles/service-business.md).

Show a short coverage summary and ask whether important material was missed at the agreed review point. Record the answer in run.md. Save substantive results and update progress.md. Then continue the agreed analysis; no completion marker or validation script is required.

Stop when decision-relevant questions have an answer or an explicit gap with its impact. Read a new source only for a named remaining question; do not automatically research adjacent hypotheses. Save sufficient short quotes and context once, so later stages reuse references; return to the original only for a concrete doubt or conflict. Do not inventory every unread file.
