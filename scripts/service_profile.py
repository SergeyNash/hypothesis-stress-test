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
    if profile_of((run_dir/'input/hypothesis.md').read_text()) != 'service_business':
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
        values = fields(path.read_text())
        statuses = {key: values.get(key) for key in CONTOURS}
        status_by_file[path.name] = statuses
        if any(value not in STATUSES for value in statuses.values()):
            codes.append('INVALID_SERVICE_STATUS')
    if bc.name == 'business_context_analysis.md' and bc.exists():
        heads = '\n'.join(re.findall(r'^#+\s+(.+)$', bc.read_text(), re.M)).casefold()
        for aliases in [('customer value','ценность заказчику'),('provider value','ценность поставщику'),
                        ('service promise and boundaries','обещание и границы'),
                        ('delivery feasibility','исполнимость'),('capacity and economics','мощность и экономика')]:
            if not any(a in heads for a in aliases):
                codes.append('MISSING_SERVICE_SECTION')
    decision = out/'decision_review.md'
    decision_text = decision.read_text() if decision.exists() else ''
    action = fields(decision_text).get('service_decision')
    if action not in DECISIONS:
        codes.append('INVALID_SERVICE_DECISION')
    recommendation = re.search(r'(?:Токен рекомендации|Recommendation token):\s*\**([a-z_]+)', decision_text)
    token = recommendation.group(1) if recommendation else None
    if token not in {'proceed','proceed_with_validation','additional_research','reject'}:
        codes.append('MISSING_RECOMMENDATION_TOKEN')
    if action == 'reject' and token != 'reject' or action == 'additional_research' and token != 'additional_research':
        codes.append('SERVICE_DECISION_MISMATCH')
    if action in DECISIONS - {'reject','additional_research','expand_sales'} and token not in {'proceed_with_validation','additional_research'}:
        codes.append('SERVICE_DECISION_MISMATCH')
    inventory = out/'evidence_inventory.md'
    synthetic = False
    if inventory.exists():
        for block in re.split(r'(?=^###\s+EVID-\d+)', inventory.read_text(), flags=re.M)[1:]:
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
    if plan.exists():
        rows = [line.casefold() for line in plan.read_text().splitlines() if line.startswith('|')]
        for aliases in [('вопрос','question'),('метод','method'),('выборка','sample'),('база сравнения','baseline'),
                        ('метрика','metric'),('критерий успеха','success criterion'),('критерий остановки','stop criterion'),
                        ('срок','deadline'),('владелец','owner'),('доказательство','evidence'),('развилки','branches')]:
            if not any(any(alias in row for alias in aliases) for row in rows):
                codes.append('INCOMPLETE_SERVICE_VALIDATION_PLAN')
    html = out/'human_report.html'
    if html.exists():
        parser = ServiceHTML()
        parser.feed(html.read_text())
        if (parser.values != status_by_file.get('decision_review.md') or parser.decision != action
                or parser.duplicates):
            codes.append('SERVICE_REPORT_MISMATCH')
    return sorted(set(codes))
