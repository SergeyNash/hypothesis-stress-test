"""Machine-checkable service-profile contracts; no semantic validation or LLM."""
from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

PROFILES = {'digital_product', 'service_business'}
TYPES = {'new_service', 'service_offer', 'commercial_model', 'delivery_model',
         'service_improvement', 'renewal_expansion'}
STATUSES = {'supported', 'conditional', 'unknown', 'contradicted'}
CONTOURS = ('customer_value', 'buying_path', 'delivery_feasibility', 'provider_economics')
DECISIONS = {'limited_pilot', 'revise_offer', 'revise_price_scope', 'build_capability',
             'expand_sales', 'additional_research', 'reject'}


def fields(text):
    out = {}
    for line in text.splitlines():
        match = re.match(r'^\s*[-*]\s+([^:]+):\s*(.*?)\s*$', line)
        if match:
            key = match[1].strip().strip('*`').casefold()
            out[key] = match[2].strip().strip('*`')
    return out


def get(values, *aliases, default=''):
    return next((values[a.casefold()] for a in aliases if a.casefold() in values), default)


def machine_token(value):
    """Read one token with optional Markdown and a separated human explanation.

    Never salvage an invalid enum by searching for a valid word inside prose.
    """
    match = re.fullmatch(r"[*`]*([a-z_]+)[*`]*(?:\s+(?:[—–]|-)\s+[^\n]+)?", value.strip())
    return match[1] if match else None


PLAN_FIELDS = (
    ('вопрос', 'question', 'гипотеза', 'hypothesis'), ('метод', 'method'),
    ('выборка', 'sample'), ('база сравнения', 'baseline'), ('метрика', 'metric'),
    ('критерий успеха', 'success criterion'), ('критерий остановки', 'stop criterion'),
    ('срок', 'deadline'), ('владелец', 'owner'), ('доказательство', 'evidence'),
    ('развилки', 'branches', 'ветки'),
)


def plan_tables_complete(text):
    tables, current = [], []
    for line in text.splitlines() + ['']:
        if line.lstrip().startswith('|'):
            cells = [c.strip().strip('*`').casefold() for c in line.strip().strip('|').split('|')]
            if not all(re.fullmatch(r'[: -]+', c or '-') for c in cells):
                current.append(cells)
        elif current:
            tables.append(current); current = []
    found = False
    for table in tables:
        header = table[0]
        # Wide table: canonical columns; check every action row, not scattered labels.
        if any(any(a in c for a in PLAN_FIELDS[0]) for c in header):
            found = True
            indexes = [next((i for i,c in enumerate(header) if any(a in c for a in aliases)), None)
                       for aliases in PLAN_FIELDS]
            if None in indexes or len(table) < 2:
                return False
            if any(any(i >= len(row) or not usable(row[i]) for i in indexes) for row in table[1:]):
                return False
        # Vertical field/value table, one complete action per table.
        elif any(any(a in row[0] for a in PLAN_FIELDS[0]) for row in table[1:] if row):
            found = True
            for aliases in PLAN_FIELDS:
                if not any(len(row)>1 and any(a in row[0] for a in aliases) and usable(row[1])
                           for row in table[1:]):
                    return False
    return found


def usable(value):
    return bool(value.strip()) and not re.fullmatch(r'\[.*\]|<.*>|\.{3}|…|tbd|todo', value.strip(), re.I)


def profile_of(text):
    return get(fields(text), 'Application Profile', 'Профиль применения', default='digital_product')


def validate_service_input(text):
    values = fields(text)
    profile = profile_of(text)
    if profile not in PROFILES:
        return ['INVALID_PROFILE']
    if profile != 'service_business':
        return []
    codes = []
    if get(values, 'Hypothesis Type', 'Тип гипотезы') not in TYPES:
        codes.append('INVALID_HYPOTHESIS_TYPE')
    for aliases in [('Decision Owner','Владелец решения'), ('Baseline','Текущий способ'),
                    ('Customer Outcome','Результат заказчика'), ('Service Promise','Обещание услуги'),
                    ('Provider Change','Изменение у поставщика'), ('Role Bindings','Привязка ролей')]:
        if not usable(get(values, *aliases)):
            codes.append('MISSING_SERVICE_FIELD')
    if not re.search(r'^##\s+(service context|сервисный контекст)\s*$', text, re.M | re.I):
        codes.append('MISSING_SERVICE_FIELD')
    return sorted(set(codes))


class ServiceHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.section = False
        self.values = {}
        self.decision = None
        self.duplicates = False

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if data.get('id') == 'service-viability':
            self.section = True
            self.decision = data.get('data-service-decision')
        if self.section and data.get('data-service-field') in CONTOURS:
            key = data['data-service-field']
            self.duplicates |= key in self.values
            self.values[key] = data.get('data-status')

    def handle_endtag(self, tag):
        if tag == 'section':
            self.section = False


def validate_service_outputs(run_dir):
    run_dir = Path(run_dir)
    if profile_of((run_dir/'input/hypothesis.md').read_text(encoding='utf-8-sig')) != 'service_business':
        return []
    out = run_dir/'outputs'
    codes = []
    bc = out/'business_context_analysis.md'
    if not bc.exists():
        bc = out/'missing_business_context.md'
    required = [bc, out/'hypothesis_map.md', out/'decision_review.md']
    status_by_file = {}
    for path in required:
        if not path.exists():
            codes.append('MISSING_SERVICE_ASSESSMENT')
            continue
        values = fields(path.read_text(encoding='utf-8-sig'))
        statuses = {key: machine_token(values.get(key, '')) for key in CONTOURS}
        status_by_file[path.name] = statuses
        if any(value not in STATUSES for value in statuses.values()):
            codes.append('INVALID_SERVICE_STATUS')
    if bc.name == 'business_context_analysis.md' and bc.exists():
        heads = '\n'.join(re.findall(r'^#+\s+(.+)$', bc.read_text(encoding='utf-8-sig'), re.M)).casefold()
        for aliases in [('customer value','ценность заказчику'),('provider value','ценность поставщику'),
                        ('service promise and boundaries','обещание и границы'),
                        ('delivery feasibility','исполнимость'),('capacity and economics','мощность и экономика')]:
            if not any(a in heads for a in aliases):
                codes.append('MISSING_SERVICE_SECTION')
    decision = out/'decision_review.md'
    decision_text = decision.read_text(encoding='utf-8-sig') if decision.exists() else ''
    action = machine_token(fields(decision_text).get('service_decision', ''))
    if action not in DECISIONS:
        codes.append('INVALID_SERVICE_DECISION')
    token_line = re.search(r'^\s*(?:[-*]\s+)?(?:Токен рекомендации|Recommendation token):\s*(.+)$', decision_text, re.M | re.I)
    token = machine_token(token_line[1]) if token_line else None
    if token not in {'proceed','proceed_with_validation','additional_research','reject'}:
        codes.append('MISSING_RECOMMENDATION_TOKEN')
    if action == 'reject' and token != 'reject' or action == 'additional_research' and token != 'additional_research':
        codes.append('SERVICE_DECISION_MISMATCH')
    if action in DECISIONS - {'reject','additional_research','expand_sales'} and token not in {'proceed_with_validation','additional_research'}:
        codes.append('SERVICE_DECISION_MISMATCH')
    inventory = out/'evidence_inventory.md'
    synthetic = False
    if inventory.exists():
        for block in re.split(r'(?=^###\s+EVID-\d+)', inventory.read_text(encoding='utf-8-sig'), flags=re.M)[1:]:
            item = fields(block)
            if item.get('source_origin') not in {'customer_record','provider_record','external','synthetic'}:
                codes.append('MISSING_SERVICE_PROVENANCE')
            if item.get('evidence_status') not in {'observed','reported','assumed','synthetic'}:
                codes.append('MISSING_SERVICE_PROVENANCE')
            if item.get('source_origin') == 'synthetic':
                synthetic = True
                if item.get('evidence_status') != 'synthetic':
                    codes.append('SYNTHETIC_PROVENANCE_MISMATCH')
    if action == 'expand_sales':
        statuses = status_by_file.get('decision_review.md', {})
        high = re.search(r'(?:Уверенность|Confidence):\s*\**(?:Высокая|High)\b', decision_text, re.I)
        if synthetic or not statuses or any(v != 'supported' for v in statuses.values()) or token != 'proceed' or not high:
            codes.append('UNSUPPORTED_SALES_EXPANSION')
    plan = out/'customer_discovery_plan.md'
    if plan.exists() and not plan_tables_complete(plan.read_text(encoding='utf-8-sig')):
        codes.append('INCOMPLETE_SERVICE_VALIDATION_PLAN')
    html = out/'human_report.html'
    if html.exists():
        parser = ServiceHTML()
        parser.feed(html.read_text(encoding='utf-8-sig'))
        if (parser.values != status_by_file.get('decision_review.md') or parser.decision != action
                or parser.duplicates):
            codes.append('SERVICE_REPORT_MISMATCH')
    return sorted(set(codes))
