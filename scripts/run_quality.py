"""Consistency checks for declared evidence/claim audit; never proves source truth."""
import json
import re
from pathlib import Path
from html import unescape

CHECKS = {'source_lineage', 'claim_references', 'numeric_scope', 'simulations_not_evidence',
          'unknown_not_refuted', 'original_intent', 'decision_logic', 'commercial_behavior'}
KINDS = {'customer_record', 'provider_record', 'primary_public', 'secondary_public',
         'internal_analysis', 'simulation', 'search_log'}
EMPIRICAL = {'customer_record', 'provider_record', 'primary_public'}
SCOPES_REQUIRING_PRIMARY = {'customer_need', 'willingness_to_pay', 'delivery_capacity', 'provider_economics'}


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def protocol(run):
    p = Path(run) / 'run_config.json'
    if not p.exists():
        return 1
    value = read_json(p)
    if not isinstance(value, dict) or value.get('protocol_version') != 2:
        raise ValueError('unsupported run protocol')
    return 2


def normalized(text):
    return re.sub(r'\s+', ' ', unescape(text)).strip()


def validate_quality(run):
    run = Path(run).resolve()
    try:
        if protocol(run) < 2:
            return []
        ledger = read_json(run / 'outputs/claim_ledger.json')
        review = read_json(run / 'outputs/quality_review.json')
    except (OSError, UnicodeError, ValueError, TypeError):
        return ['MISSING_OR_INVALID_QUALITY_AUDIT']
    errors = []
    if not isinstance(ledger, dict) or not isinstance(review, dict):
        return ['INVALID_QUALITY_SCHEMA']
    sources, claims = ledger.get('sources'), ledger.get('claims')
    if not isinstance(sources, list) or not isinstance(claims, list) or not claims:
        return ['INVALID_CLAIM_LEDGER']
    if not all(isinstance(x, dict) for x in sources + claims):
        return ['INVALID_CLAIM_LEDGER']
    registry = {s.get('id'): s for s in sources if isinstance(s.get('id'), str)}
    claim_ids = {c.get('id') for c in claims if isinstance(c.get('id'), str)}
    if len(registry) != len(sources) or len(claim_ids) != len(claims):
        errors.append('DUPLICATE_OR_MISSING_AUDIT_ID')
    for source in sources:
        sid = source.get('id', '?')
        if source.get('kind') not in KINDS or not source.get('independence_group') or not isinstance(source.get('scopes'), list) or not source['scopes']:
            errors.append('INVALID_SOURCE_RECORD:' + str(sid))
        # EVID IDs must actually exist; a model persona cannot be relabelled empirical.
        if str(sid).startswith('EVID-'):
            inv = (run / 'outputs/evidence_inventory.md').read_text(encoding='utf-8-sig')
            blocks = re.split(r'(?=^###\s+EVID-\d+)', inv, flags=re.M)
            block = next((b for b in blocks if re.match(r'###\s+' + re.escape(sid) + r'\b', b.strip())), None)
            if block is None:
                errors.append('UNRESOLVED_SOURCE:' + sid)
            elif re.search(r'source_origin:\s*synthetic\b', block) and source.get('kind') != 'simulation':
                errors.append('SYNTHETIC_SOURCE_RELABELLED:' + sid)
    for claim in claims:
        cid = str(claim.get('id', '?'))
        refs = claim.get('evidence_ids', [])
        if not isinstance(refs, list) or not all(isinstance(x, str) for x in refs):
            errors.append('INVALID_CLAIM_REFS:' + cid); continue
        selected = [registry[x] for x in refs if x in registry]
        if len(selected) != len(refs):
            errors.append('UNRESOLVED_CLAIM_REFERENCE:' + cid)
        if claim.get('status') not in {'supported', 'conditional', 'unknown', 'contradicted'}:
            errors.append('INVALID_CLAIM_STATUS:' + cid)
        if claim.get('kind') not in {'fact', 'inference', 'gap', 'proposal'} or not claim.get('rationale'):
            errors.append('INVALID_CLAIM_RECORD:' + cid)
        basis, status, scope = claim.get('basis'), claim.get('status'), claim.get('scope')
        if basis not in {'observed', 'derived', 'missing_evidence', 'simulation'}:
            errors.append('INVALID_CLAIM_BASIS:' + cid)
        if basis == 'missing_evidence' and status in {'supported', 'contradicted'}:
            errors.append('ABSENCE_IS_NOT_PROOF:' + cid)
        if status in {'supported', 'contradicted'}:
            if not selected:
                errors.append('CLAIM_WITHOUT_EVIDENCE:' + cid)
            if selected and all(s.get('kind') == 'simulation' for s in selected):
                errors.append('SIMULATION_IS_NOT_EVIDENCE:' + cid)
            if scope in SCOPES_REQUIRING_PRIMARY and not any(
                    s.get('kind') in EMPIRICAL and scope in s.get('scopes', []) for s in selected):
                errors.append('EMPIRICAL_SCOPE_NOT_SUPPORTED:' + cid)
            if scope == 'global_market_absence':
                errors.append('UNBOUNDED_ABSENCE_CLAIM:' + cid)
        groups = {s['independence_group'] for s in selected
                  if s.get('kind') != 'simulation' and s.get('independence_group')}
        if claim.get('independent_sources') != len(groups):
            errors.append('INDEPENDENCE_OVERCOUNT:' + cid)
        targets = claim.get('targets', [])
        if not isinstance(targets, list) or not targets:
            errors.append('MISSING_CLAIM_TARGET:' + cid)
        else:
            for target in targets:
                try:
                    p = (run / target['artifact']).resolve()
                    if not p.is_relative_to(run / 'outputs') or not target['quote'].strip():
                        raise ValueError('invalid target')
                    text = p.read_text(encoding='utf-8-sig')
                    if p.suffix == '.html':
                        text = re.sub(r'<[^>]+>', ' ', text)
                    if normalized(target['quote']) not in normalized(text):
                        raise ValueError('quote absent')
                except (KeyError, TypeError, OSError, ValueError, AttributeError):
                    errors.append('CLAIM_TARGET_MISMATCH:' + cid)
        numbers = claim.get('numbers', [])
        if not isinstance(numbers, list):
            errors.append('INVALID_NUMERIC_RECORD:' + cid); continue
        periods = set()
        for number in numbers:
            try:
                source = registry[number['source_id']]
                fact = next(f for f in source.get('facts', []) if f['id'] == number['fact_id'])
                for key in ['value', 'unit', 'period', 'population', 'metric']:
                    if key not in fact or not str(fact[key]).strip() or number[key] != fact[key]:
                        raise ValueError('numeric scope differs')
                periods.add(number['period'])
            except (KeyError, TypeError, ValueError, StopIteration, AttributeError):
                errors.append('NUMERIC_SCOPE_MISMATCH:' + cid)
        if len(periods) > 1 and claim.get('temporal_comparison') is not True:
            errors.append('MIXED_NUMERIC_PERIODS:' + cid)
    # Catch dangling references even when a claim was omitted from the ledger.
    for name in ['business_context_analysis.md', 'external_research.md', 'market_analysis.md',
                 'hypothesis_map.md', 'decision_review.md', 'human_report.html']:
        p = run / 'outputs' / name
        if p.exists():
            ids = set(re.findall(r'\b(?:EVID|EXT|CONF)-\d+\b', p.read_text(encoding='utf-8-sig')))
            for sid in ids - registry.keys():
                errors.append('UNREGISTERED_REFERENCE:' + name + ':' + sid)
    checks = review.get('checks', [])
    if not isinstance(checks, list) or not all(isinstance(x, dict) for x in checks):
        return sorted(set(errors + ['INVALID_QUALITY_REVIEW']))
    if {x.get('id') for x in checks} != CHECKS or len(checks) != len(CHECKS):
        errors.append('INCOMPLETE_QUALITY_REVIEW')
    for check in checks:
        if check.get('status') not in {'pass', 'not_applicable'} or not isinstance(check.get('reason'), str) or not check.get('reason', '').strip():
            errors.append('QUALITY_REVIEW_FAILED:' + str(check.get('id')))
        if not isinstance(check.get('claim_ids'), list) or not all(isinstance(c, str) and c in claim_ids for c in check['claim_ids']):
            errors.append('INVALID_REVIEW_CLAIM_IDS')
    return sorted(set(errors))
