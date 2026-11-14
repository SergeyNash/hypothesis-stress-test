"""Stage-scoped gates. Does not infer completion from file existence."""
import json
from runtime_metrics import timed
from pathlib import Path

INPUTS = {
    'facilitator': ['outputs/role_outputs/*','outputs/hypothesis_summary.md','outputs/validation_questions.md'],
    'local_evidence': ['outputs/discovery_preview.md','outputs/evidence_inventory.md'],
    'business_context': ['outputs/business_context_analysis.md'],
    'market': ['outputs/market_analysis.md'],
    'synthesis': ['outputs/hypothesis_map.md','outputs/hypothesis_digest.txt'],
    'customer_discovery_planning': ['outputs/customer_discovery_plan.md'],
    'decision_review': ['outputs/decision_review.md'],
    'human_report': ['outputs/human_report.html'],
}


def spec_for(phase):
    from validate_runs import MARKER_REGISTRY
    return next((name,spec) for name,spec in MARKER_REGISTRY.items() if spec['completed_phase']==phase)


def payload(phase, status='completed'):
    _,spec=spec_for(phase)
    required=['outputs/missing_business_context.md'] if phase=='business_context' and status=='skipped_missing_context' else INPUTS[phase]
    return dict(status=status,completed_phase=phase,next_phase=spec['next_phase'],inputs=required)


def enabled(run):
    from source_selection import config
    return config(run).get('lifecycle_version')==1


@timed('phase_validation', phase_argument=1)
def check(run,phase,*,marker=True,status='completed'):
    from validate_runs import validate_marker,validate_evidence,validate_market
    run=Path(run).resolve();errors=[]
    name,spec=spec_for(phase)
    if marker:
        errors.extend(validate_marker(run/'outputs'/name,spec))
    else:
        if status not in spec['status']:errors.append('INVALID_MARKER_STATUS')
        for pattern in payload(phase,status)['inputs']:
            matches=list(run.glob(pattern))
            if not matches or any(not p.is_file() or not p.resolve().is_relative_to(run) or not p.stat().st_size for p in matches):
                errors.append('MISSING_MARKER_ARTIFACT:'+pattern)
    if phase=='local_evidence':
        errors.extend(validate_evidence(run/'outputs/evidence_inventory.md'))
        from validate_runs import find_section,parse_sections,field_map
        inventory=run/'outputs/evidence_inventory.md'
        if inventory.exists():
            review=find_section(parse_sections(inventory.read_text(encoding='utf-8-sig')),('retrieval review','проверка полноты'))
            if review is None or field_map(review).get('status') not in {'accepted','waived'}:
                errors.append('INCOMPLETE_RETRIEVAL_REVIEW')
    if phase=='market':errors.extend(validate_market(run/'outputs/market_analysis.md'))
    from validate_runs import validate_synthesis,validate_digest,validate_decision
    if phase=='synthesis':
        errors.extend(validate_synthesis(run/'outputs/hypothesis_map.md'))
        errors.extend(validate_digest(run/'outputs/hypothesis_digest.txt'))
    if phase=='decision_review':errors.extend(validate_decision(run/'outputs/decision_review.md'))
    if phase not in {'facilitator','human_report'}:
        from run_quality import validate_quality
        errors.extend(validate_quality(run,phase=phase))
    if phase in {'decision_review','human_report'}:
        from service_profile import validate_service_outputs
        # The service validator tolerates missing HTML until export; validate the plan/decision now.
        errors.extend(validate_service_outputs(run))
    if phase=='human_report':
        from validate_runs import check_run
        errors.extend(check_run(run,pending_human_report=not marker))
    return sorted(set(errors))


@timed('prerequisite_validation', phase_argument=1)
def require_previous(run,phase,*,verify_artifacts=True):
    from run_progress import PHASES,events
    if not enabled(run):return
    rows=events(Path(run)/'outputs')
    for earlier in PHASES[:PHASES.index(phase)]:
        last=next((e for e in reversed(rows) if e['kind']=='phase' and e['phase']==earlier),None)
        if last is None or last['state']!='completed':
            raise ValueError('Previous phase not completed in journal: '+earlier+'; use run_control.py complete after verification')
        if verify_artifacts and earlier in INPUTS:
            errors=check(run,earlier)
            if errors:raise ValueError('Previous phase failed verification: '+earlier+': '+', '.join(errors))


def diagnose(run,rows):
    """Warn about divergence; never count a marker as journal completion."""
    run=Path(run);warnings=[]
    for phase in INPUTS:
        name,_=spec_for(phase)
        marker=run/'outputs'/name
        last=next((r for r in reversed(rows) if r['kind']=='phase' and r['phase']==phase),None)
        try:
            data=json.loads(marker.read_text(encoding='utf-8-sig'))
            claimed=data.get('status') in {'completed','skipped_missing_context'}
        except (OSError,ValueError,AttributeError):claimed=False
        if claimed and (not last or last['state']!='completed'):
            warnings.append('Маркер '+phase+' есть, но завершение не записано в журнале; нужна проверка complete.')
        elif last and last['state']=='completed' and not claimed:
            warnings.append('Журнал отмечает '+phase+' завершённым, но маркер отсутствует или некорректен.')
    return warnings


class _VerifiedTransition:
    """An in-process receipt, usable only during one checked controller commit."""
    def __init__(self, run, phase):
        self.run = Path(run).resolve()
        self.phase = phase
        self.active = True


def accepts(receipt, run, phase, state):
    if not isinstance(receipt, _VerifiedTransition) or not receipt.active or receipt.run != Path(run).resolve():
        return False
    if state == 'completed':
        return phase == receipt.phase
    if state == 'running':
        return phase == payload(receipt.phase)['next_phase']
    return False


from contextlib import contextmanager

@contextmanager
def verified_transition(run, phase):
    """Only the controller calls this after real checks; never serialize receipts."""
    receipt = _VerifiedTransition(run, phase)
    try:
        yield receipt
    finally:
        receipt.active = False
