#!/usr/bin/env python3
"""Static contract checks for hypothesis-stress-test RUN_DIR examples.

Stdlib only. No LLM. No network.
"""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HYP_ID_RE = re.compile(r"^HYP-\d{4}-\d{2}-\d{2}-\d{3}$")
RUN_ID_RE = re.compile(r"^RUN-\d{4}-\d{2}-\d{2}-\d{3}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EVID_RE = re.compile(r"^###\s+(EVID-\d+)", re.M)
FIELD_RE = re.compile(r"^[-*]\s+([A-Za-z_]+)\s*:\s*(.+)$")

STATUSES = {"draft", "running", "completed", "archived"}
STATUS_ALIASES = {
    "черновик": "draft",
    "выполняется": "running",
    "в работе": "running",
    "завершён": "completed",
    "завершено": "completed",
    "архив": "archived",
    "архивирован": "archived",
}

SECTION_ALIASES = {
    "metadata": ("metadata", "метаданные"),
    "statement": ("statement", "формулировка"),
    "roles": ("relevant roles", "релевантные роли", "затронутые роли"),
    "context": ("research context", "контекст исследования"),
}

CONTEXT_ALIASES = {
    "domain": ("domain", "домен"),
    "audience": ("target audience", "целевая аудитория"),
    "scenario": ("scenario", "сценарий"),
}

META_ALIASES = {
    "hypothesis_id": ("hypothesis id", "id гипотезы"),
    "created_at": ("created at", "дата создания"),
    "run_id": ("run id", "id прогона"),
    "status": ("status", "статус"),
}

EVIDENCE_TYPES = {
    "quote",
    "transcript_excerpt",
    "image_observation",
    "metadata_only",
    "observation",
}
REQUIRED_EVID_FIELDS = {
    "source_path",
    "source_kind",
    "evidence_type",
    "observation",
    "relevance",
    "relevance_reason",
    "retrieved_by",
}

ALLOWED_OUTPUTS = {
    "role_outputs",
    "hypothesis_summary.md",
    "validation_questions.md",
    "discovery_preview.md",
    "evidence_inventory.md",
    "business_context_analysis.md",
    "missing_business_context.md",
    "market_analysis.md",
    "hypothesis_map.md",
    "hypothesis_digest.txt",
    "customer_discovery_plan.md",
    "decision_review.md",
    "human_report.html",
    "ready_for_synthesis.marker",
    "knowledge_retrieval_complete.marker",
    "business_context_complete.marker",
    "market_analysis_complete.marker",
    "synthesis_complete.marker",
    "customer_discovery_planning_complete.marker",
    "decision_review_complete.marker",
    "human_report_complete.marker",
}

MARKER_REGISTRY = {
    "ready_for_synthesis.marker": {
        "status": {"completed"},
        "completed_phase": "facilitator",
        "next_phase": "local_evidence",
    },
    "knowledge_retrieval_complete.marker": {
        "status": {"completed"},
        "completed_phase": "local_evidence",
        "next_phase": "business_context",
    },
    "business_context_complete.marker": {
        "status": {"completed", "skipped_missing_context"},
        "completed_phase": "business_context",
        "next_phase": "market",
    },
    "market_analysis_complete.marker": {
        "status": {"completed"},
        "completed_phase": "market",
        "next_phase": "synthesis",
    },
    "synthesis_complete.marker": {
        "status": {"completed"},
        "completed_phase": "synthesis",
        "next_phase": "customer_discovery_planning",
    },
    "customer_discovery_planning_complete.marker": {
        "status": {"completed"},
        "completed_phase": "customer_discovery_planning",
        "next_phase": "decision_review",
    },
    "decision_review_complete.marker": {
        "status": {"completed"},
        "completed_phase": "decision_review",
        "next_phase": "human_report",
    },
    "human_report_complete.marker": {
        "status": {"completed"},
        "completed_phase": "human_report",
        "next_phase": "human_decision",
    },
}

PHASE_ORDER = [
    "ready_for_synthesis.marker",
    "knowledge_retrieval_complete.marker",
    "business_context_complete.marker",
    "market_analysis_complete.marker",
    "synthesis_complete.marker",
    "customer_discovery_planning_complete.marker",
    "decision_review_complete.marker",
    "human_report_complete.marker",
]

MARKET_SECTIONS = [
    ("mcp", ("mcp status", "статус mcp")),
    ("local", ("local signals", "локальные сигналы")),
    ("confluence", ("confluence signals", "сигналы confluence")),
    ("external", ("external", "внешние")),
    ("inferred", ("inferred", "выведенные")),
    ("summary", ("signal summary", "сводка сигналов")),
]

SYNTHESIS_SECTIONS = [
    "подтверждённ",
    "внутренн",
    "упущенн",
    "ловушк",
    "дивергенц",
    "слеп",
    "новая информация",
    "границ",
    "влияние",
    "приоритет",
]

DECISION_SECTIONS = [
    ("резюме", "executive summary"),
    ("evidence", "качества evidence"),
    ("допущен", "assumption"),
    ("валидац", "validation plan"),
    ("рекомендац", "recommendation"),
]


class HrefParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        for key, value in attrs:
            if key == "href" and value:
                self.hrefs.append(value)


def heading_blob(text: str) -> str:
    heads = []
    for line in text.splitlines():
        if line.startswith("#"):
            heads.append(line.lstrip("#").strip().lower())
    return "\n".join(heads)


def parse_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = ""
    for line in text.splitlines():
        if line.startswith("#"):
            current = line.lstrip("#").strip().lower()
            sections[current] = []
        elif current:
            sections[current].append(line)
    return {key: "\n".join(val) for key, val in sections.items()}


def find_section(sections: dict[str, str], aliases: tuple[str, ...]) -> str | None:
    for name, body in sections.items():
        if any(alias in name for alias in aliases):
            return body
    return None


def field_map(body: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in body.splitlines():
        match = FIELD_RE.match(line.strip())
        if not match:
            continue
        values[match.group(1).lower()] = match.group(2).strip().strip("`")
    return values


def load_json_marker(path: Path) -> tuple[dict | None, str | None]:
    raw = path.read_text(encoding="utf-8").strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None, "NON_CANONICAL_MARKER"
    if not isinstance(data, dict):
        return None, "NON_CANONICAL_MARKER"
    return data, None


def validate_input(run_dir: Path, *, check_folder_id: bool) -> list[str]:
    codes: list[str] = []
    path = run_dir / "input" / "hypothesis.md"
    if not path.exists():
        return ["MISSING_SECTION"]
    text = path.read_text(encoding="utf-8")
    sections = parse_sections(text)

    def has(aliases: tuple[str, ...]) -> bool:
        return find_section(sections, aliases) is not None

    for key, aliases in SECTION_ALIASES.items():
        if not has(aliases):
            codes.append("MISSING_SECTION")

    meta = find_section(sections, SECTION_ALIASES["metadata"]) or ""
    meta_l = meta.lower()
    hid = None
    for line in meta.splitlines():
        low = line.lower()
        if "hypothesis id" in low or "id гипотезы" in low:
            hid = line.split(":", 1)[-1].strip()
        if "run id" in low or "id прогона" in low:
            rid = line.split(":", 1)[-1].strip()
            if not RUN_ID_RE.match(rid):
                codes.append("INVALID_HYPOTHESIS_ID")
        if "created at" in low or "дата создания" in low:
            created = line.split(":", 1)[-1].strip()
            if not DATE_RE.match(created):
                codes.append("MISSING_SECTION")
        if "status" in low or "статус" in low:
            status_raw = line.split(":", 1)[-1].strip().lower()
            status = STATUS_ALIASES.get(status_raw, status_raw)
            if status not in STATUSES:
                codes.append("INVALID_STATUS")

    if hid is None or not HYP_ID_RE.match(hid):
        codes.append("INVALID_HYPOTHESIS_ID")
    elif check_folder_id and run_dir.name != hid:
        codes.append("RUN_DIR_ID_MISMATCH")

    statement = (find_section(sections, SECTION_ALIASES["statement"]) or "").strip()
    low = statement.lower()
    weak = ("улучшить" in low and "опыт" in low) or (
        "improve" in low and "experience" in low
    )
    # If…then / Если…то are recommended, not required (see input-validation skill).
    dimensions = 0
    if re.search(r"если|if\b", statement, re.I):
        dimensions += 1
    if re.search(
        r"\bто\b|then\b|будет|будут|сократ|быстрее|выраст|получит",
        statement,
        re.I,
    ):
        dimensions += 1
    if len(statement.split()) >= 12:
        dimensions += 1
    if weak or dimensions < 3:
        codes.append("VAGUE_STATEMENT")

    roles = find_section(sections, SECTION_ALIASES["roles"]) or ""
    role_items = [line for line in roles.splitlines() if re.match(r"^[-*]", line.strip())]
    if not role_items:
        codes.append("MISSING_ROLES")
    elif len(role_items) > 5:
        codes.append("TOO_MANY_ROLES")

    context = (find_section(sections, SECTION_ALIASES["context"]) or "").lower()
    for aliases in CONTEXT_ALIASES.values():
        if not any(alias in context for alias in aliases):
            codes.append("MISSING_CONTEXT_FIELD")

    return sorted(set(codes))


def validate_marker(path: Path, expected: dict) -> list[str]:
    codes: list[str] = []
    data, err = load_json_marker(path)
    if err:
        return [err]
    if data.get("status") not in expected["status"]:
        codes.append("INVALID_MARKER_STATUS")
    if data.get("completed_phase") != expected["completed_phase"]:
        codes.append("INVALID_MARKER_PHASE")
    if data.get("next_phase") != expected["next_phase"]:
        codes.append("INVALID_MARKER_NEXT")
    if "inputs" not in data or not isinstance(data["inputs"], list):
        codes.append("INVALID_MARKER_INPUTS")
    return codes


def validate_evidence(path: Path) -> list[str]:
    if not path.exists():
        return ["MISSING_EVIDENCE_INVENTORY"]
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r"(?=^###\s+EVID-\d+)", text, flags=re.M)
    codes: list[str] = []
    found = False
    for block in blocks:
        match = re.match(r"###\s+(EVID-\d+)", block.strip())
        if not match:
            continue
        found = True
        fields = field_map(block)
        missing = REQUIRED_EVID_FIELDS - set(fields)
        if missing:
            codes.append("EVIDENCE_FIELDS")
        if fields.get("evidence_type") not in EVIDENCE_TYPES:
            codes.append("EVIDENCE_TYPE")
        if fields.get("evidence_type") == "image_observation" and "extraction_note" not in fields:
            codes.append("EVIDENCE_FIELDS")
    if not found and "gap" not in text.lower() and "нет extractable" not in text.lower():
        codes.append("EVIDENCE_FIELDS")
    return sorted(set(codes))


def validate_market(path: Path) -> list[str]:
    if not path.exists():
        return ["MISSING_MARKET"]
    blob = heading_blob(path.read_text(encoding="utf-8"))
    codes: list[str] = []
    for key, aliases in MARKET_SECTIONS:
        if not any(alias in blob for alias in aliases):
            codes.append(f"MARKET_SECTION_{key.upper()}")
    return codes


def validate_synthesis(path: Path) -> list[str]:
    if not path.exists():
        return ["MISSING_SYNTHESIS"]
    text = path.read_text(encoding="utf-8").lower()
    missing = [token for token in SYNTHESIS_SECTIONS if token not in text]
    return ["SYNTHESIS_SECTIONS"] if missing else []


def validate_decision(path: Path) -> list[str]:
    if not path.exists():
        return ["MISSING_DECISION"]
    blob = heading_blob(path.read_text(encoding="utf-8"))
    codes: list[str] = []
    for aliases in DECISION_SECTIONS:
        if not any(alias in blob for alias in aliases):
            codes.append("DECISION_SECTIONS")
            break
    return codes


def validate_digest(path: Path) -> list[str]:
    if not path.exists():
        return ["MISSING_DIGEST"]
    words = path.read_text(encoding="utf-8").split()
    return ["DIGEST_TOO_LONG"] if len(words) > 150 else []


def validate_html_links(path: Path) -> list[str]:
    if not path.exists():
        return ["MISSING_HUMAN_REPORT"]
    parser = HrefParser()
    parser.feed(path.read_text(encoding="utf-8"))
    codes: list[str] = []
    for href in parser.hrefs:
        if href.startswith("#") or href.startswith("http"):
            continue
        target = (path.parent / href).resolve()
        if not target.exists():
            codes.append("BROKEN_HTML_LINK")
    return sorted(set(codes))


def validate_outputs_allowlist(run_dir: Path) -> list[str]:
    outputs = run_dir / "outputs"
    if not outputs.exists():
        return ["MISSING_OUTPUTS"]
    codes: list[str] = []
    for child in outputs.iterdir():
        if child.name.startswith("."):
            continue
        if child.name not in ALLOWED_OUTPUTS:
            codes.append(f"UNKNOWN_OUTPUT:{child.name}")
    return codes


def validate_complete_run(run_dir: Path) -> list[str]:
    codes = validate_input(run_dir, check_folder_id=False)
    codes.extend(validate_outputs_allowlist(run_dir))
    outputs = run_dir / "outputs"
    for name, expected in MARKER_REGISTRY.items():
        marker = outputs / name
        if not marker.exists():
            codes.append(f"MISSING_MARKER:{name}")
            continue
        codes.extend(validate_marker(marker, expected))

    bc = outputs / "business_context_complete.marker"
    if bc.exists():
        data, err = load_json_marker(bc)
        if not err and data:
            if data.get("status") == "completed" and not (outputs / "business_context_analysis.md").exists():
                codes.append("MISSING_BUSINESS_CONTEXT_ANALYSIS")
            if data.get("status") == "skipped_missing_context" and not (
                outputs / "missing_business_context.md"
            ).exists():
                codes.append("MISSING_BUSINESS_CONTEXT_GAP")
    market_marker = outputs / "market_analysis_complete.marker"
    if market_marker.exists() and not bc.exists():
        codes.append("MISSING_BUSINESS_CONTEXT_GATE")

    codes.extend(validate_evidence(outputs / "evidence_inventory.md"))
    codes.extend(validate_market(outputs / "market_analysis.md"))
    codes.extend(validate_synthesis(outputs / "hypothesis_map.md"))
    codes.extend(validate_decision(outputs / "decision_review.md"))
    codes.extend(validate_digest(outputs / "hypothesis_digest.txt"))
    codes.extend(validate_html_links(outputs / "human_report.html"))
    return sorted(set(codes))


def validate_docs_drift() -> list[str]:
    codes: list[str] = []
    facilitator = (ROOT / ".cline/skills/hypothesis-facilitator/SKILL.md").read_text(
        encoding="utf-8"
    )
    retrieval = (ROOT / ".cline/skills/local-knowledge-retrieval/SKILL.md").read_text(
        encoding="utf-8"
    )
    if "Ready for Market Layer" in facilitator:
        codes.append("DOCS_DRIFT_FACILITATOR_NEXT")
    if "Ready for Market Layer" in retrieval:
        codes.append("DOCS_DRIFT_RETRIEVAL_NEXT")
    contract = (ROOT / "implementations/cline-contract.md").read_text(encoding="utf-8")
    run_doc = (ROOT / "examples/run.md").read_text(encoding="utf-8")
    if "business-context-value-check" not in contract or "business-context-value-check" not in run_doc:
        codes.append("DOCS_DRIFT_BUSINESS_CONTEXT")
    return codes


def validate_fixture(run_dir: Path, expected: list[str]) -> list[str]:
    name = run_dir.name
    found: list[str] = []
    if (run_dir / "input" / "hypothesis.md").exists():
        found.extend(validate_input(run_dir, check_folder_id=(name == "id-mismatch")))
    if name == "missing-marker":
        outputs = run_dir / "outputs"
        if (outputs / "market_analysis_complete.marker").exists() and not (
            outputs / "business_context_complete.marker"
        ).exists():
            found.append("MISSING_BUSINESS_CONTEXT_GATE")
    if name == "empty-kb":
        inv = run_dir / "outputs" / "evidence_inventory.md"
        prev = run_dir / "outputs" / "discovery_preview.md"
        if not prev.exists() or not inv.exists():
            found.append("EMPTY_KB_MISSING_PREVIEW")
    if name == "mcp-unavailable":
        text = (run_dir / "outputs" / "market_analysis.md").read_text(encoding="utf-8").lower()
        if "not configured" not in text and "не настроен" not in text:
            found.append("MCP_STATUS_MISSING")
    if name == "external-research-declined":
        text = (run_dir / "outputs" / "market_analysis.md").read_text(encoding="utf-8").lower()
        if "skipped" not in text:
            found.append("EXTERNAL_SKIP_MISSING")
    unexpected = sorted(set(found) - set(expected))
    missing_expected = sorted(set(expected) - set(found))
    codes: list[str] = []
    if unexpected:
        codes.append("UNEXPECTED:" + ",".join(unexpected))
    if missing_expected:
        codes.append("MISSING_EXPECTED:" + ",".join(missing_expected))
    return codes


def main() -> int:
    failures: list[str] = []

    for docs_code in validate_docs_drift():
        failures.append(f"docs :: {docs_code}")

    for example in sorted((ROOT / "examples").glob("example-00*")):
        if not example.is_dir():
            continue
        codes = validate_complete_run(example)
        for code in codes:
            failures.append(f"{example.relative_to(ROOT).as_posix()} :: {code}")

    manifest_path = ROOT / "examples/fixtures/manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for item in manifest["fixtures"]:
        run_dir = ROOT / "examples/fixtures" / item["path"]
        codes = validate_fixture(run_dir, item.get("expect", []))
        for code in codes:
            failures.append(f"{run_dir.relative_to(ROOT).as_posix()} :: {code}")

    if failures:
        print("validate_runs: FAIL")
        for line in failures:
            print(f"  - {line}")
        return 1
    print("validate_runs: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
