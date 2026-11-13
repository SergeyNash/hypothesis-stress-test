"""Artifact ownership for incremental audits; final audits always inspect everything."""
PHASES=['local_evidence','business_context','market','synthesis','customer_discovery_planning','decision_review','human_report']
OUTPUTS={
    'local_evidence':['discovery_preview.md','evidence_inventory.md'],
    'business_context':['business_context_analysis.md','missing_business_context.md','external_research.md'],
    'market':['market_analysis.md'],
    'synthesis':['hypothesis_map.md','hypothesis_digest.txt'],
    'customer_discovery_planning':['customer_discovery_plan.md'],
    'decision_review':['decision_review.md'],
    'human_report':['human_report.html'],
}


def artifacts_for(phase):
    if phase is None:return [name for p in PHASES for name in OUTPUTS[p]]
    return [name for p in PHASES[:PHASES.index(phase)+1] for name in OUTPUTS[p]]


def ledger_for_phase(run,ledger,phase):
    """Only conclusions in current/prior artifacts belong to this phase's gate."""
    import re
    from pathlib import PurePosixPath
    visible=set(artifacts_for(phase));claims=[];ids=set()
    for claim in ledger.get('claims',[]):
        declared=claim.get('targets',[])
        malformed=not isinstance(declared,list) or not declared or any(not isinstance(t,dict) or 'artifact' not in t or 'quote' not in t or str(PurePosixPath(t['artifact']).parent)!='outputs' for t in declared)
        targets=[] if malformed else [t for t in declared if PurePosixPath(t['artifact']).name in visible]
        if targets or malformed:
            claims.append(dict(claim,targets=targets) if not malformed else claim)
            ids.update(claim.get('evidence_ids',[]))
    for name in visible:
        path=run/'outputs'/name
        if path.is_file():ids.update(re.findall(r'\b(?:EVID|EXT|CONF|CONL)-\d+\b',path.read_text(encoding='utf-8-sig')))
    return {'sources':[s for s in ledger.get('sources',[]) if s.get('id') in ids], 'claims':claims}
