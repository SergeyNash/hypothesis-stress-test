"""Source-bound audit v2. Deterministic checks plus explicit, bounded semantic review.

Checks anchors and declared relationships, never certifies source truth or complete markets.
"""
from collections import defaultdict
from decimal import Decimal, InvalidOperation
import hashlib
from html import unescape
import json
from pathlib import Path
import re

ARTIFACTS = ['business_context_analysis.md', 'external_research.md', 'market_analysis.md',
             'hypothesis_map.md', 'customer_discovery_plan.md', 'decision_review.md', 'human_report.html']
EXTRA_CHECKS = {'counterevidence', 'entity_scope', 'procurement', 'research_execution', 'experiment_consistency'}


def plain(value):
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', value))).strip()


def decimals(text):
    # Remove spaces only inside numbers; tolerate RU decimal and thin-space grouping.
    text = re.sub(r'(?<=\d)[ \u00a0\u202f](?=\d)', '', str(text))
    found = set()
    for token in re.findall(r'(?<![\w])[-+]?\d+(?:[.,]\d+)?', text):
        try:
            found.add(Decimal(token.replace(',', '.')))
        except InvalidOperation:
            pass
    return found


def inventory_blocks(run):
    text = (run/'outputs/evidence_inventory.md').read_text(encoding='utf-8-sig')
    return {m[1]: m[0] for m in re.finditer(r'^###\s+(EVID-\d+)\b.*?(?=^###\s+EVID-|\Z)', text, re.M|re.S)}


def target_text(run, target):
    path = (run/target['artifact']).resolve()
    if not path.is_relative_to(run/'outputs'):
        raise ValueError('target outside outputs')
    text = path.read_text(encoding='utf-8-sig')
    quote = target['quote']
    if plain(quote) not in plain(text):
        raise ValueError('target quote absent')
    return quote


def numeric_status_target(quote):
    return bool(re.fullmatch(r'\s*[-*]?\s*(?:customer_value|buying_path|delivery_feasibility|provider_economics)\s*:\s*[*`]*(?:supported|unknown|conditional|contradicted)[*`]*\s*', quote))


def validate_grounding(run, ledger, review):
    run = Path(run).resolve()
    errors = []
    try:
        snap = json.loads((run/'outputs/source_snapshot.json').read_text(encoding='utf-8-sig'))
        files = snap['files']
        if snap['schema_version'] != 1 or not isinstance(files, list):
            raise ValueError('snapshot schema')
        anchors = {}
        for file in files:
            for unit in file['units']:
                key = hashlib.sha256((file['source_path']+'\0'+file['sha256']+'\0'+unit['location']).encode()).hexdigest()[:24]
                if unit['anchor_id'] != key or key in anchors:
                    errors.append('INVALID_SNAPSHOT_ANCHOR')
                anchors[key] = dict(unit, source_path=file['source_path'], source_sha256=file['sha256'])
        inv = inventory_blocks(run)
    except (OSError, ValueError, KeyError, TypeError):
        errors.append('MISSING_OR_INVALID_SOURCE_SNAPSHOT')
        files, anchors = [], {}
        inv = inventory_blocks(run)
    errors.extend(verify_fragments(files))
    sources = {s['id']:s for s in ledger['sources']}
    claims = {c['id']:c for c in ledger['claims']}
    questions = defaultdict(list)
    fact_map = {}
    for sid, source in sources.items():
        if source.get('kind') == 'simulation':
            if source.get('role') != 'simulation':
                errors.append('SOURCE_ROLE_MISMATCH:'+sid)
            continue
        ids = source.get('anchor_ids', [])
        quote = source.get('quote', '')
        role = source.get('role')
        if role not in {'reported_fact','author_inference','context'}:
            errors.append('MISSING_SOURCE_ROLE:'+sid)
        if not ids or any(i not in anchors for i in ids):
            errors.append('SOURCE_ANCHOR_MISSING:'+sid); continue
        texts = [anchors[i]['text'] for i in ids]
        if not quote or not any(plain(quote) in plain(t) for t in texts):
            errors.append('SOURCE_QUOTE_MISMATCH:'+sid)
        if sid.startswith('EVID-'):
            block = inv.get(sid, '')
            match = re.search(r'^- anchor_ids:\s*(\[.*\])\s*$', block, re.M)
            try:
                if not match or set(json.loads(match[1])) != set(ids):
                    raise ValueError('inventory mapping differs')
                if not re.search(r'^- source_quote:\s*'+re.escape(quote)+r'\s*$',block,re.M):
                    raise ValueError('inventory quote differs')
                # Bind the declared inventory location to the snapshot file, not just its ID.
                path_line = re.search(r'^- source_path:\s*(.+)$',block,re.M)
                if not path_line or not all(a['source_path'].replace('\\','/') in path_line[1].replace('\\','/') for a in (anchors[i] for i in ids)):
                    raise ValueError('inventory source path differs')
            except (ValueError, TypeError):
                errors.append('EVIDENCE_BINDING_MISMATCH:'+sid)
        facts = source.get('facts', [])
        if role == 'reported_fact' and re.search(r'\d',quote) and not facts:
            errors.append('NUMERIC_EVIDENCE_NOT_MODELLED:'+sid)
        for fact in facts:
            fid = sid+'/'+str(fact.get('id'))
            fact_map[fid] = fact
            value_anchor = fact.get('value_anchor')
            contexts = fact.get('context_anchors', [])
            if value_anchor not in ids or any(i not in anchors for i in contexts):
                errors.append('NUMERIC_ANCHOR_MISMATCH:'+fid); continue
            value = str(fact.get('value',''))
            # An interval must bind both endpoints; never accept an arbitrary label.
            tokens = decimals(value)
            if not tokens or not tokens.issubset(decimals(anchors[value_anchor]['text'])):
                errors.append('SOURCE_VALUE_MISMATCH:'+fid)
            context = '\n'.join(anchors[i]['text'] for i in [value_anchor]+contexts)
            period_years = set(re.findall(r'\b20\d\d\b',str(fact.get('period',''))))
            if not period_years or not period_years.issubset(set(re.findall(r'\b20\d\d\b',context))):
                errors.append('SOURCE_PERIOD_MISMATCH:'+fid)
            if not all(fact.get(k) for k in ['metric','population','unit','question']):
                errors.append('INCOMPLETE_NUMERIC_CONTEXT:'+fid)
            if fact.get('question'):
                questions[fact['question']].append(fid)
    comparisons = review.get('comparisons', [])
    for question, refs in questions.items():
        if len(refs) < 2:
            continue
        match = next((x for x in comparisons if x.get('question') == question), None)
        if (not match or not set(refs).issubset(set(match.get('fact_refs',[]))) or
            match.get('relationship') not in {'different_populations','different_periods','conflicting','consistent'} or
            not match.get('reason') or not match.get('impact_claim_ids') or
            not set(match['impact_claim_ids']).issubset(claims)):
            errors.append('UNREVIEWED_COUNTEREVIDENCE:'+question)
    for cid, claim in claims.items():
        for target in claim.get('targets',[]):
            try:
                quote = target_text(run,target)
                if numeric_status_target(quote):
                    errors.append('STATUS_IS_NOT_CLAIM_TARGET:'+cid)
            except (OSError, ValueError, KeyError, TypeError):
                errors.append('CLAIM_TARGET_MISMATCH:'+cid)
        if claim.get('kind') in {'fact','inference'} and any(sources.get(s,{}).get('role') == 'author_inference' for s in claim.get('evidence_ids',[])):
            if claim.get('status') == 'supported' and not any(sources.get(s,{}).get('role') == 'reported_fact' for s in claim.get('evidence_ids',[])):
                errors.append('AUTHOR_CONCLUSION_IS_NOT_EMPIRICAL:'+cid)
        for number in claim.get('numbers',[]):
            if number.get('source_id') not in claim.get('evidence_ids',[]):
                errors.append('NUMERIC_SOURCE_NOT_CITED:'+cid)
        level = claim.get('commercial_level','none')
        if level not in {'none','announcement','contract','payment'}:
            errors.append('INVALID_COMMERCIAL_LEVEL:'+cid)
        if level in {'contract','payment'}:
            key = level+'_anchor'
            aid = claim.get(key)
            if aid not in anchors:
                errors.append('MISSING_COMMERCIAL_PROOF:'+cid)
            elif level == 'payment' and re.search(r'сч[её]т|proposal|invoice|коммерческ', anchors[aid]['text'], re.I) and not re.search(r'оплачен|зачислен|поступлен|received|paid',anchors[aid]['text'],re.I):
                errors.append('INVOICE_IS_NOT_PAYMENT:'+cid)
    # Exact original intent is a deterministic check, not a self-attested checkbox.
    input_text = (run/'input/hypothesis.md').read_text(encoding='utf-8-sig')
    match = re.search(r'^##\s+(?:Формулировка|Formulation|Statement|Hypothesis Statement)\s*\n(.*?)(?=^##\s|\Z)',input_text,re.M|re.S|re.I)
    report = run/'outputs/human_report.html'
    if not match or not report.exists() or plain(match[1]) not in plain(report.read_text(encoding='utf-8-sig')):
        errors.append('ORIGINAL_HYPOTHESIS_NOT_PRESERVED')
    errors.extend(validate_research(run, review.get('research',{})))
    errors.extend(validate_context(review.get('context',{}), anchors))
    errors.extend(validate_entity_language(run, review.get('context',{}), anchors))
    errors.extend(validate_decision(run, review.get('decision',{}), claims, anchors))
    errors.extend(validate_experiments(review.get('experiments',[]), anchors, run))
    procurement = review.get('procurement',{})
    if procurement.get('status') == 'not_applicable' and any('procurement' in s.get('scopes',[]) for s in sources.values()):
        errors.append('PROCUREMENT_REVIEW_CANNOT_BE_SKIPPED')
    if procurement.get('status') == 'reported_only':
        refs = procurement.get('fact_refs', [])
        if not procurement.get('reason') or not refs or any(r not in fact_map for r in refs):
            errors.append('UNBOUND_REPORTED_PROCUREMENT_TOTAL')
        try:target_text(run, procurement['limitation_target'])
        except (OSError,ValueError,KeyError,TypeError):errors.append('MISSING_PROCUREMENT_LIMITATION')
    else:
        errors.extend(validate_procurement(procurement, anchors))
    checks = {x.get('id'):x for x in review.get('checks',[])}
    for key in EXTRA_CHECKS:
        if key not in checks or checks[key].get('status') not in {'pass','not_applicable'} or not checks[key].get('reason'):
            errors.append('MISSING_GROUNDED_REVIEW:'+key)
    for name in ARTIFACTS:
        p=run/'outputs'/name
        if not p.exists():continue
        text=plain(p.read_text(encoding='utf-8-sig')) if p.suffix=='.html' else p.read_text(encoding='utf-8-sig')
        for line in text.splitlines():
            # Deliberately narrow lints, not a replacement for reading the claim.
            risky = re.search(r'окно свободно|публичного оффера[^.\n]{0,70}\bнет\b|нет публичного оффера|рынком[^.\n]{0,70}не закупается|публично не закупается|не занято и не востребовано',line,re.I)
            bounded = re.search(r'не доказан|не подтвержд|не следует|нельзя|не означает|в изученн|не найден|не установлен|гипотез[аыу]:',line,re.I)
            if re.search(r'вместо немедленных продаж|вместо немедленного запуска',line,re.I) and not re.search(r'немедленн|сразу.{0,30}продаж',input_text,re.I):
                errors.append('UNSUPPORTED_ORIGINAL_INTENT:'+name)
            if re.search(r'компетенц[^.\n]{0,100}\bнет\b',line,re.I) and not re.search(r'нет данных|не подтверж|не описан|на фактах|доказательств',line,re.I):
                errors.append('UNKNOWN_IS_NOT_ABSENCE:'+name)
            if risky and not bounded:
                errors.append('UNBOUNDED_MARKET_NEGATIVE:'+name)
            if not bounded and re.search(r'рын[оа]к[^.\n]{0,100}(?:уз[ко]|мал)[^.\n]{0,100}\d+\s*[–-]\s*\d+\s*%',line,re.I):
                errors.append('PILOT_RATE_IS_NOT_MARKET_SIZE:'+name)
    return sorted(set(errors))


def validate_research(run, research):
    if research.get('status') not in {'covered','partial','unavailable','declined'} or not research.get('reason'):
        return ['MISSING_RESEARCH_EXECUTION_REVIEW']
    try:
        events=[json.loads(l) for l in (run/'outputs/pipeline_events.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]
    except (OSError,ValueError):return ['MISSING_RESEARCH_EVENTS']
    internet={x['id']:x for x in events if x.get('channel')=='internet'}
    status=research['status'];errors=[]
    if status in {'unavailable','declined'}:
        ids=research.get('exception_event_ids',[])
        expected={'unavailable','auth_error','error'} if status=='unavailable' else {'declined'}
        if not ids or not research.get('limitation_target') or any(i not in internet or internet[i].get('state') not in expected for i in ids):
            errors.append('UNSUPPORTED_RESEARCH_EXCEPTION')
        try:target_text(run,research['limitation_target'])
        except (OSError,ValueError,KeyError,TypeError):errors.append('MISSING_RESEARCH_LIMITATION')
        if any(re.search(r'\b404\b',internet[i].get('message','')) for i in ids if i in internet):
            errors.append('PAGE_FAILURE_IS_NOT_SEARCH_FAILURE')
        # A 404 page is not an unavailable search tool. Require the actual tool-level blocker.
        if status=='unavailable' and research.get('blocker') not in {'search_tool_unavailable','network_unavailable','host_permission','authentication'}:
            errors.append('PAGE_FAILURE_IS_NOT_SEARCH_FAILURE')
    else:
        tracks=research.get('tracks',{})
        for track in ['offers','procurement','operations','counterexamples']:
            ids=tracks.get(track,[])
            if not ids or any(i not in internet or internet[i].get('state')!='query_started' or not internet[i].get('query') for i in ids):
                errors.append('MISSING_SEARCH_TRACK:'+track)
        reads=research.get('read_event_ids',[])
        if status=='covered' and (not reads or any(i not in internet or internet[i].get('state') not in {'read','used'} or not internet[i].get('urls') for i in reads)):
            errors.append('SEARCH_WITHOUT_READ_SOURCES')
    if not (run/'outputs/external_research.md').is_file():errors.append('MISSING_EXTERNAL_RESEARCH')
    return errors


def validate_context(context, anchors):
    if not context.get('provider') or not context.get('client_scope') or not context.get('entity_review'):
        return ['MISSING_ENTITY_SCOPE_REVIEW']
    if context.get('scope_status') not in {'verified','unknown'}:return ['INVALID_CLIENT_SCOPE']
    if context['scope_status']=='verified' and (not context.get('anchor_ids') or any(i not in anchors for i in context['anchor_ids'])):
        return ['UNSUPPORTED_CLIENT_SCOPE']
    return []


def validate_experiments(experiments, anchors, run=None):
    if not experiments:return ['MISSING_EXPERIMENT_REVIEW']
    errors=[]
    for x in experiments:
        if not x.get('id') or not x.get('owner') or not x.get('decision_branch'):
            errors.append('INCOMPLETE_EXPERIMENT')
        if not isinstance(x.get('duration_days'),int) or not isinstance(x.get('stop_after_days'),int) or not 0 < x['stop_after_days'] <= x['duration_days']:
            errors.append('EXPERIMENT_DEADLINE_CONFLICT')
        if not x.get('target') or not x.get('success_observation'):
            errors.append('MISSING_EXPERIMENT_TARGET')
        if run is not None:
            try:
                actual=target_text(run,x['target'])
                for text_key,days_key in [('duration_quote','duration_days'),('stop_quote','stop_after_days')]:
                    literal=x.get(text_key,'')
                    bounds=duration_bounds(literal)
                    if not literal or literal not in actual or not bounds or not bounds[0] <= x[days_key] <= bounds[1]:
                        errors.append('EXPERIMENT_TEXT_HORIZON_MISMATCH')
                if not x.get('success_quote') or x['success_quote'] not in actual:
                    errors.append('EXPERIMENT_SUCCESS_TEXT_MISMATCH')
                elif x.get('tests') == 'payment' and re.search(r'подписан|signed|выставлен|issued',x['success_quote'],re.I) and not re.search(r'оплат|поступ|received|paid',x['success_quote'],re.I):
                    errors.append('INVOICE_IS_NOT_PAYMENT')
            except (OSError,ValueError,KeyError,TypeError):errors.append('EXPERIMENT_TARGET_MISMATCH')
        if x.get('tests')=='payment' and x.get('success_observation') not in {'funds_received','paid_invoice','bank_receipt'}:
            errors.append('INVOICE_IS_NOT_PAYMENT')
    return errors


def validate_procurement(procurement, anchors):
    if procurement.get('status')=='not_applicable' and procurement.get('reason'):return []
    records=procurement.get('records',[]);aggregates=procurement.get('aggregates',[])
    if not records or not aggregates:return ['MISSING_PROCUREMENT_RECONCILIATION']
    errors=[];index={}
    for row in records:
        pid=row.get('procedure_id');aid=row.get('id_anchor')
        if not pid or pid in index:errors.append('DUPLICATE_PROCEDURE');continue
        index[pid]=row
        if aid not in anchors or str(pid) not in anchors[aid]['text']:
            errors.append('PROCEDURE_ID_NOT_IN_SOURCE')
        if not row.get('segment') or not row.get('allocation_reason'):
            errors.append('AMBIGUOUS_PROCUREMENT_SEGMENT')
        year_anchor = row.get('publication_anchor')
        if year_anchor not in anchors or str(row.get('year')) not in anchors[year_anchor]['text']:
            errors.append('PROCUREMENT_PERIOD_NOT_IN_SOURCE')
        if 'nmc' in row:
            aid=row.get('nmc_anchor')
            if aid not in anchors or Decimal(str(row['nmc'])) not in decimals(anchors[aid]['text']):
                errors.append('PROCUREMENT_AMOUNT_MISMATCH')
    for aggregate in aggregates:
        ids=aggregate.get('procedure_ids',[])
        selected=[index[i] for i in ids if i in index]
        if len(ids)!=len(set(ids)) or len(selected)!=len(ids):errors.append('AGGREGATE_DUPLICATE_OR_UNKNOWN_PROCEDURE');continue
        if any(x.get('segment')!=aggregate.get('segment') for x in selected):errors.append('AGGREGATE_SEGMENT_MISMATCH')
        period = [int(y) for y in re.findall(r'\b20\d\d\b', str(aggregate.get('period','')))]
        if not period or any(not isinstance(x.get('year'),int) or not min(period) <= x['year'] <= max(period) for x in selected):
            errors.append('PROCUREMENT_AGGREGATE_PERIOD_MISMATCH')
        metric=aggregate.get('metric')
        if metric=='count':expected=Decimal(len(ids))
        elif metric=='nmc':
            if any('nmc' not in x for x in selected):errors.append('AGGREGATE_MISSING_AMOUNTS');continue
            expected=sum((Decimal(str(x['nmc'])) for x in selected),Decimal(0))
        else:errors.append('INVALID_PROCUREMENT_METRIC');continue
        if abs(expected-Decimal(str(aggregate.get('value','NaN'))))>Decimal('.01'):
            errors.append('PROCUREMENT_AGGREGATE_MISMATCH')
    return errors


def verify_fragments(files):
    from extract_evidence import units
    errors = []
    for file in files:
        if not file.get('units'):
            continue
        try:
            root = Path(file['root']).resolve()
            path = (root/file['source_path']).resolve()
            if not path.is_relative_to(root) or not path.is_file() or path.is_symlink():
                raise ValueError('source unavailable')
            if path.stat().st_size > 2*1024*1024:
                raise ValueError('source exceeds verification bound')
            if hashlib.sha256(path.read_bytes()).hexdigest() != file['sha256']:
                errors.append('SOURCE_CHANGED:'+file['source_path']);continue
            expected = {x['location']:x['text'] for x in file['units']}
            for _, location, text in units(path):
                if location in expected:
                    if text != expected.pop(location):
                        errors.append('SNAPSHOT_TEXT_CHANGED:'+file['source_path'])
                if not expected:break
            if expected:errors.append('SNAPSHOT_LOCATION_ABSENT:'+file['source_path'])
        except (OSError,ValueError,KeyError,ImportError):
            errors.append('SOURCE_NOT_REVERIFIED:'+str(file.get('source_path','?')))
    return errors


def validate_decision(run, decision, claims, anchors):
    from service_profile import fields, machine_token, profile_of, CONTOURS
    input_text=(run/'input/hypothesis.md').read_text(encoding='utf-8-sig')
    if profile_of(input_text)!='service_business':return []
    text=(run/'outputs/decision_review.md').read_text(encoding='utf-8-sig')
    values=fields(text);action=machine_token(values.get('service_decision',''))
    if decision.get('action')!=action:return ['DECISION_AUDIT_MISMATCH']
    errors=[]
    for key in CONTOURS:
        cid=decision.get('contour_claim_ids',{}).get(key)
        c=claims.get(cid,{})
        if c.get('scope')!=key or c.get('status')!=machine_token(values.get(key,'')):
            errors.append('DECISION_CONTOUR_CLAIM_MISMATCH:'+key)
    if action=='limited_pilot':
        if not isinstance(decision.get('execution_allowed'),bool) or not decision.get('conditions'):
            errors.append('MISSING_PILOT_ADMISSION_CONDITIONS')
        elif decision['execution_allowed']:
            for key in ['access_anchor','cost_cap_anchor','capacity_anchor','approval_anchor']:
                if decision.get(key) not in anchors:errors.append('PILOT_ADMISSION_NOT_EVIDENCED:'+key)
            if not decision.get('stop_conditions'):errors.append('MISSING_PILOT_STOP_CONDITIONS')
    return errors


def duration_bounds(text):
    m=re.fullmatch(r'\s*(\d+)\s*(days?|weeks?|months?|дн(?:ей|я|и)?|нед(?:ели|ель|еля)?|мес(?:яцев|яца|яц)?)[.]?\s*',text,re.I)
    if not m:return None
    n=int(m[1]);unit=m[2].lower()
    if unit.startswith(('day','дн')):return n,n
    if unit.startswith(('week','нед')):return n*7,n*7
    # Bounds catch impossible horizons without pretending every calendar month has 30 days.
    return n*28,n*31


def validate_entity_language(run, context, anchors):
    errors=[]
    for name in ARTIFACTS:
        p=run/'outputs'/name
        if not p.exists():continue
        text=p.read_text(encoding='utf-8-sig')
        for line in text.splitlines():
            # A slash in a provider identity asserts an alias/affiliation, unlike a technology stack.
            merge=re.search(r'(?:провайдер|поставщик|внутри|provider|supplier)[^\n]{0,80}?([A-Za-zА-Яа-яЁё0-9_.-]+/[A-Za-zА-Яа-яЁё0-9_.-]+)',line,re.I)
            if merge:
                proof=context.get('affiliation_anchor_ids',[])
                if not proof or any(a not in anchors for a in proof):
                    errors.append('UNVERIFIED_PROVIDER_AFFILIATION:'+name)
            census=re.search(r'база\s+[A-Za-zА-Яа-яЁё0-9_.-]+\s*(?:=|—|:|\()\s*\d+\s+банк',line,re.I)
            if census and context.get('scope_status')!='verified' and not re.search(r'выборк|подмнож|часть|из заметк|одного ДК|one account',line,re.I):
                errors.append('CLIENT_SUBSET_IS_NOT_COMPLETE_BASE:'+name)
    return errors
