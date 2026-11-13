from decimal import Decimal
from html import escape
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from extract_evidence import extract
from grounded_audit import EXTRA_CHECKS, validate_procurement, validate_experiments, decimals
from run_quality import CHECKS, validate_quality
from source_snapshot import capture
import run_control
import run_progress
import validate_runs


class GroundedAudit(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.run=self.root/'HYP-2026-11-09-001'
        shutil.copytree(ROOT/'examples/example-005',self.run)
        self.source=self.root/'research.txt'
        self.source.write_text('12% of sampled projects reached production in 2025.\n53% of sampled companies have production in 2025.\nInvoice issued, awaiting payment.\n',encoding='utf-8')
        self.snapshot=capture(self.run,self.root,['research.txt'])
        self.a,self.b,self.invoice=[u['anchor_id'] for u in self.snapshot['files'][0]['units']]
        self.config={'protocol_version':2,'audit_version':2}
        self.write('run_config.json',self.config)
        self.claim_text='The measures use different populations; market size remains unknown.'
        with (self.run/'outputs/decision_review.md').open('a',encoding='utf-8') as f:f.write('\n'+self.claim_text+'\n')
        self.limit='Internet search was unavailable; competitor coverage is unknown.'
        (self.run/'outputs/external_research.md').write_text(self.limit,encoding='utf-8')
        self.write_events([{'id':1,'kind':'source','channel':'internet','state':'unavailable','message':'Search tool absent in synthetic fixture','query':''}])
        self.ledger={'sources':[],'claims':[{'id':'CL-001','kind':'inference','scope':'operations',
            'status':'conditional','basis':'derived','rationale':'Different denominators.',
            'evidence_ids':['SRC-001','SRC-002'],'independent_sources':2,
            'targets':[{'artifact':'outputs/decision_review.md','quote':self.claim_text}],
            'numbers':[]}]}
        for sid,anchor,value,pop in [('SRC-001',self.a,12,'projects'),('SRC-002',self.b,53,'companies')]:
            quote=next(u['text'] for u in self.snapshot['files'][0]['units'] if u['anchor_id']==anchor)
            self.ledger['sources'].append({'id':sid,'kind':'secondary_public','role':'reported_fact',
                'independence_group':sid,'scopes':['operations'],'anchor_ids':[anchor],'quote':quote,
                'facts':[{'id':'production','value':value,'unit':'%','period':'2025','population':pop,
                    'metric':'production_rate','question':'production_readiness','value_anchor':anchor,'context_anchors':[]}]})
        ids=set()
        for name in ['business_context_analysis.md','hypothesis_map.md','decision_review.md','human_report.html']:
            ids.update(re.findall(r'\bEVID-\d+\b',(self.run/'outputs'/name).read_text()))
        self.ledger['sources'] += [{'id':i,'kind':'simulation','role':'simulation','independence_group':'demo','scopes':['simulation']} for i in sorted(ids)]
        self.review={'checks':[{'id':c,'status':'pass','reason':'Checked synthetic fixture anchors.','claim_ids':['CL-001']} for c in sorted(CHECKS|EXTRA_CHECKS)],
            'comparisons':[{'question':'production_readiness','fact_refs':['SRC-001/production','SRC-002/production'],
                'relationship':'different_populations','reason':'Projects versus companies; percentages cannot bound market size.','impact_claim_ids':['CL-001']}],
            'research':{'status':'unavailable','reason':'No search tool in synthetic fixture.',
                'blocker':'search_tool_unavailable','exception_event_ids':[1],
                'limitation_target':{'artifact':'outputs/external_research.md','quote':self.limit}},
            'context':{'provider':'Example service firm','client_scope':'Client subset in one meeting',
                'scope_status':'unknown','entity_review':'No corporate affiliation or complete client census asserted.'},
            'experiments':[{'id':'EXP-1','owner':'Service owner','duration_days':14,'stop_after_days':14,
                'tests':'payment','success_observation':'funds_received','decision_branch':'Research before any service promise.',
                'target':{'artifact':'outputs/decision_review.md','quote':self.claim_text}}],
            'procurement':{'status':'not_applicable','reason':'No procurement data in this fixture.'}}
        text=(self.run/'input/hypothesis.md').read_text()
        original=re.search(r'^## Формулировка\n(.*?)(?=^## |\Z)',text,re.M|re.S)[1]
        p=self.run/'outputs/human_report.html';p.write_text(p.read_text().replace('</body>','<blockquote>'+escape(original)+'</blockquote></body>'),encoding='utf-8')
        for i,(scope,status) in enumerate([('customer_value','conditional'),('buying_path','unknown'),('delivery_feasibility','conditional'),('provider_economics','conditional')],2):
            self.ledger['claims'].append({'id':f'CL-00{i}','kind':'gap','scope':scope,'status':status,
                'basis':'missing_evidence','rationale':'Unmeasured synthetic contour.', 'evidence_ids':[], 'independent_sources':0,
                'targets':[{'artifact':'outputs/decision_review.md','quote':self.claim_text}]})
        self.review['decision']={'action':'limited_pilot','execution_allowed':False,'conditions':['Confirm access, capacity and bounded cost before a promise.'],
            'contour_claim_ids':{scope:f'CL-00{i}' for i,scope in enumerate(['customer_value','buying_path','delivery_feasibility','provider_economics'],2)}}
        experiment_text='Experiment duration 14 days; stop after 14 days without funds received.'
        with (self.run/'outputs/customer_discovery_plan.md').open('a',encoding='utf-8') as f:f.write('\n'+experiment_text+'\n')
        self.review['experiments'][0].update(target={'artifact':'outputs/customer_discovery_plan.md','quote':experiment_text},
            duration_quote='14 days',stop_quote='14 days',success_quote='funds received')
        self.save()

    def tearDown(self):self.tmp.cleanup()
    def write(self,name,data): (self.run/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    def write_events(self,events):
        for x in events:
            x.setdefault('at','2026-01-01T00:00:00+00:00');x.setdefault('phase','business_context');x.setdefault('message','Synthetic fixture event')
        (self.run/'outputs/pipeline_events.jsonl').write_text('\n'.join(json.dumps(x) for x in events)+'\n',encoding='utf-8')
    def save(self):
        self.write('outputs/claim_ledger.json',self.ledger);self.write('outputs/quality_review.json',self.review)
    def codes(self):self.save();return '\n'.join(validate_quality(self.run))

    def test_valid_source_grounded_audit_and_actual_run(self):
        self.assertEqual('',self.codes())
        self.assertEqual([],validate_runs.check_run(self.run))

    def test_snapshot_cannot_be_rewritten_to_match_wrong_number(self):
        f=self.snapshot['files'][0];f['units'][0]['text']='393 projects in 2025.'
        self.write('outputs/source_snapshot.json',self.snapshot)
        self.assertIn('SNAPSHOT_TEXT_CHANGED',self.codes())

    def test_consistent_jsons_with_wrong_value_still_fail(self):
        self.ledger['sources'][0]['facts'][0]['value']=393
        self.assertIn('SOURCE_VALUE_MISMATCH',self.codes())

    def test_source_year_cannot_be_invented(self):
        self.ledger['sources'][0]['facts'][0]['period']='2026'
        self.assertIn('SOURCE_PERIOD_MISMATCH',self.codes())

    def test_evid_id_must_bind_inventory_source_and_exact_quote(self):
        source=self.ledger['sources'][0];source['id']='EVID-999'
        self.ledger['claims'][0]['evidence_ids'][0]='EVID-999'
        self.assertIn('EVIDENCE_BINDING_MISMATCH',self.codes())
        inv=self.run/'outputs/evidence_inventory.md'
        inv.write_text(inv.read_text()+f'\n### EVID-999\n- source_path: research.txt\n- source_origin: external\n- anchor_ids: ["{self.a}"]\n- source_quote: {source["quote"]}\n')
        self.assertNotIn('EVIDENCE_BINDING_MISMATCH',self.codes())

    def test_project_company_counterevidence_requires_comparison(self):
        self.review['comparisons']=[]
        self.assertIn('UNREVIEWED_COUNTEREVIDENCE',self.codes())

    def test_cannot_omit_numeric_evidence_from_fact_model(self):
        self.ledger['sources'][1]['facts']=[]
        self.assertIn('NUMERIC_EVIDENCE_NOT_MODELLED',self.codes())

    def test_status_token_cannot_substitute_for_claim_quote(self):
        self.ledger['claims'][0]['targets'][0]['quote']='customer_value: conditional'
        # Insert exactly matching token to rule out simple absent-string failure.
        p=self.run/'outputs/decision_review.md';p.write_text(p.read_text()+'\ncustomer_value: conditional\n')
        self.assertIn('STATUS_IS_NOT_CLAIM_TARGET',self.codes())

    def test_conditional_status_cannot_hide_categorical_market_absence(self):
        p=self.run/'outputs/market_analysis.md';p.write_text(p.read_text()+'\nПубличного оффера на рынке нет.\n')
        self.assertIn('UNBOUNDED_MARKET_NEGATIVE',self.codes())

    def test_author_assessment_is_not_empirical_confirmation(self):
        self.ledger['claims'][0]['status']='supported'
        for s in self.ledger['sources'][:2]:s['role']='author_inference'
        self.assertIn('AUTHOR_CONCLUSION_IS_NOT_EMPIRICAL',self.codes())

    def test_reframing_cannot_invent_original_launch_intent_or_absent_competence(self):
        p=self.run/'outputs/decision_review.md'
        p.write_text(p.read_text()+'\nОграниченный пилот вместо немедленных продаж.\nКомпетенций и резерва нет.\n')
        self.assertIn('UNSUPPORTED_ORIGINAL_INTENT',self.codes())
        self.assertIn('UNKNOWN_IS_NOT_ABSENCE',self.codes())

    def test_original_hypothesis_must_be_exactly_preserved(self):
        p=self.run/'outputs/human_report.html';p.write_text(re.sub(r'<blockquote>.*?</blockquote>','',p.read_text(),flags=re.S))
        self.assertIn('ORIGINAL_HYPOTHESIS_NOT_PRESERVED',self.codes())

    def test_single_404_is_not_search_execution(self):
        self.review['research']['blocker']='page_404'
        self.assertIn('PAGE_FAILURE_IS_NOT_SEARCH_FAILURE',self.codes())
        self.review['research'].update(status='covered',tracks={},read_event_ids=[])
        self.assertIn('MISSING_SEARCH_TRACK:offers',self.codes())
        self.assertIn('SEARCH_WITHOUT_READ_SOURCES',self.codes())

    def test_actual_query_tracks_and_read_sources(self):
        events=[{'id':i,'kind':'source','channel':'internet','state':'query_started','query':q} for i,q in enumerate(['offers','procurement','operations','counterexamples'],1)]
        events += [{'id':5,'kind':'source','channel':'internet','state':'read','urls':['https://example.com/service']}]
        self.write_events(events)
        self.review['research'].update(status='covered',tracks={k:[i] for i,k in enumerate(['offers','procurement','operations','counterexamples'],1)},read_event_ids=[5])
        self.assertEqual('',self.codes())

    def test_payment_is_not_signed_invoice_and_experiment_deadline(self):
        c=self.ledger['claims'][0];c.update(commercial_level='payment',payment_anchor=self.invoice)
        self.assertIn('INVOICE_IS_NOT_PAYMENT',self.codes())
        e=self.review['experiments'][0];e.update(duration_days=56,stop_after_days=180,success_observation='signed_invoice')
        self.assertIn('EXPERIMENT_DEADLINE_CONFLICT',self.codes())
        self.assertIn('INVOICE_IS_NOT_PAYMENT',self.codes())

    def test_experiment_metadata_cannot_hide_six_month_stop_in_eight_week_plan(self):
        e=self.review['experiments'][0]
        text='Duration 8 weeks; stop after 6 months without funds received.'
        p=self.run/'outputs/customer_discovery_plan.md';p.write_text(p.read_text()+'\n'+text+'\n')
        e.update(duration_days=56,stop_after_days=56,duration_quote='8 weeks',stop_quote='6 months',
                 target={'artifact':'outputs/customer_discovery_plan.md','quote':text})
        self.assertIn('EXPERIMENT_TEXT_HORIZON_MISMATCH',self.codes())

    def test_provider_affiliation_and_client_subset_must_not_be_invented(self):
        p=self.run/'outputs/business_context_analysis.md'
        p.write_text(p.read_text()+'\nПоставщик — сервисная линия внутри ExampleAlpha/ExampleBeta.\nБаза UNIT5 = 5 банков.\n')
        self.assertIn('UNVERIFIED_PROVIDER_AFFILIATION',self.codes())
        self.assertIn('CLIENT_SUBSET_IS_NOT_COMPLETE_BASE',self.codes())

    def test_unknown_client_scope_cannot_be_promoted_to_verified(self):
        self.review['context']['scope_status']='verified'
        self.assertIn('UNSUPPORTED_CLIENT_SCOPE',self.codes())

    def test_changed_source_requires_invalidation_not_silent_capture_merge(self):
        self.source.write_text('changed',encoding='utf-8')
        self.assertIn('SOURCE_CHANGED',self.codes())
        with self.assertRaises(ValueError):capture(self.run,self.root,['research.txt'])

    def test_pilot_cannot_be_authorized_without_access_cost_capacity_approval(self):
        self.review['decision']['execution_allowed']=True
        self.assertIn('PILOT_ADMISSION_NOT_EVIDENCED',self.codes())

    def test_low_pilot_success_rate_does_not_bound_market(self):
        p=self.run/'outputs/decision_review.md';p.write_text(p.read_text()+'\nРынок эксплуатации узкий: 7–10% пилотов доходят до продакшена.\n')
        self.assertIn('PILOT_RATE_IS_NOT_MARKET_SIZE',self.codes())

    def test_paged_capture_preserves_first_fragment(self):
        p=self.root/'pages.txt';p.write_text('first\nsecond\nthird')
        first=capture(self.run,self.root,['pages.txt'],max_units=1)
        f=next(f for f in first['files'] if f['source_path']=='pages.txt')
        second=capture(self.run,self.root,['pages.txt'],start_unit=f['next_unit'],max_units=2)
        f=next(f for f in second['files'] if f['source_path']=='pages.txt')
        self.assertEqual(['first','second','third'],[u['text'] for u in f['units']])

    def test_reported_procurement_totals_require_bound_facts_and_disclosure(self):
        self.ledger['sources'][0]['scopes'].append('procurement')
        self.review['procurement']={'status':'reported_only','reason':'User accepted bounded reading; no full deduplication.',
            'fact_refs':['SRC-001/production'],'limitation_target':{'artifact':'outputs/decision_review.md','quote':self.claim_text}}
        self.assertEqual('',self.codes())
        self.review['procurement']['fact_refs']=['SRC-001/invented']
        self.assertIn('UNBOUND_REPORTED_PROCUREMENT_TOTAL',self.codes())

    def test_new_prepare_starts_and_verifies_viewer_before_facilitator(self):
        import subprocess
        new=self.root/'new'/'HYP-2026-11-09-001';(new/'input').mkdir(parents=True)
        shutil.copyfile(self.run/'input/hypothesis.md',new/'input/hypothesis.md')
        children=[];real_popen=subprocess.Popen
        def launch(*a,**kw):
            child=real_popen(*a,**kw);children.append(child);return child
        with patch.object(run_control.subprocess,'Popen',side_effect=launch):
            try:
                url=run_control.prepare(new,'full')
                config=json.loads((new/'run_config.json').read_text())
                self.assertEqual(2,config['audit_version']);self.assertEqual('ready',config['viewer']['status'])
                self.assertEqual(url,run_control.start(new,'facilitator'))
                self.assertEqual(1,len(children))
                state=json.loads((new/'outputs/progress.json').read_text())
                self.assertEqual('running',next(p['state'] for p in state['phases'] if p['id']=='facilitator'))
            finally:
                for child in children:child.terminate();child.wait(timeout=5)

    def test_procurement_dedup_and_allocation(self):
        anchors={'id':{'text':'Tender-001'},'nmc':{'text':'12345.67'},'date':{'text':'2025-01-01'}}
        row={'procedure_id':'Tender-001','segment':'software','allocation_reason':'One owning segment after cross-file duplicate review.',
             'id_anchor':'id','year':2025,'publication_anchor':'date','nmc':12345.67,'nmc_anchor':'nmc'}
        p={'records':[row], 'aggregates':[{'segment':'software','metric':'count','period':'2024–2026','procedure_ids':['Tender-001'],'value':1}]}
        self.assertEqual([],validate_procurement(p,anchors))
        p['aggregates'][0]['procedure_ids'].append('Tender-001')
        self.assertIn('AGGREGATE_DUPLICATE_OR_UNKNOWN_PROCEDURE',validate_procurement(p,anchors))
        p['aggregates'][0].update(procedure_ids=['Tender-001'],segment='infrastructure')
        self.assertIn('AGGREGATE_SEGMENT_MISMATCH',validate_procurement(p,anchors))

    def test_viewer_cannot_be_silently_skipped_before_facilitator(self):
        with self.assertRaisesRegex(ValueError,'progress URL'):
            run_progress.record(self.run,phase='facilitator',state='running',message='start')
        self.config['viewer']={'status':'unavailable','notified':True,'reason':'Actual host background-process error reported to user.'}
        self.write('run_config.json',self.config)
        run_progress.record(self.run,phase='facilitator',state='running',message='start with disclosed viewer gap')

    def test_validation_history_retains_failed_attempts(self):
        run_progress.init(self.run)
        self.ledger['sources'][0]['facts'][0]['value']=393;self.save()
        self.assertEqual('FAIL',run_control.finish(self.run)['status'])
        self.ledger['sources'][0]['facts'][0]['value']=12;self.save()
        self.assertEqual('PASS',run_control.finish(self.run)['status'])
        history=[json.loads(x)['status'] for x in (self.run/'outputs/validation_history.jsonl').read_text().splitlines()]
        self.assertEqual(['running','FAIL','running','PASS'],history)

    def test_full_lifecycle_with_real_viewer_and_grounded_synthetic_artifacts(self):
        import subprocess
        from urllib.request import urlopen
        from phase_checks import INPUTS
        self.config['lifecycle_version']=1  # Explicit opt-in for this synthetic integration fixture.
        self.write('run_config.json',self.config)
        from grounded_audit import inventory_blocks
        registered={s['id'] for s in self.ledger['sources']}
        self.ledger['sources'].extend({'id':sid,'kind':'simulation','role':'simulation','independence_group':'demo','scopes':['simulation']} for sid in inventory_blocks(self.run) if sid not in registered)
        self.save()
        with (self.run/'outputs/evidence_inventory.md').open('a') as f:
            f.write('\n## Retrieval Review\n- status: waived\n- reason: Synthetic integration fixture, no live research.\n')
        for marker in (self.run/'outputs').glob('*.marker'):marker.unlink()
        children=[];real_popen=subprocess.Popen
        def launch(*args,**kwargs):
            child=real_popen(*args,**kwargs);children.append(child);return child
        with patch.object(run_control.subprocess,'Popen',side_effect=launch):
            try:
                url=run_control.prepare(self.run,'full',workspace=self.root)
                with urlopen(url) as response:self.assertEqual(200,response.status)
                for phase in INPUTS:
                    run_control.start(self.run,phase)
                    result=run_control.complete(self.run,phase)
                    self.assertEqual('PASS',result['status'],(phase,result))
                with urlopen(url.replace('progress.html','progress.json')) as response:
                    live=json.load(response)
                self.assertEqual((10,10),(live['completed'],live['total']))
                self.assertEqual([],live['warnings'])
                self.assertEqual([],validate_runs.check_run(self.run))
            finally:
                for child in children:child.terminate();child.wait(timeout=5)


if __name__=='__main__':unittest.main()
