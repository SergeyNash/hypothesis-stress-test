import contextlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import run_control as control
import run_progress as progress
from run_quality import CHECKS, validate_quality
from service_profile import machine_token, plan_tables_complete
import validate_runs as validator


class RunQuality(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.run = Path(self.temp.name) / 'HYP-2026-11-09-001'
        shutil.copytree(ROOT / 'examples/example-005', self.run)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, path, value):
        (self.run / path).write_text(json.dumps(value), encoding='utf-8')

    def audit(self):
        self.write('run_config.json', {'protocol_version': 2})
        # Separate synthetic audit target; no private customer data in fixtures.
        with (self.run / 'outputs/decision_review.md').open('a', encoding='utf-8') as f:
            f.write('\nNeed remains unknown. 12 lots in 2025.\n')
        self.ledger = {'sources': [{'id':'SRC-001', 'kind':'primary_public',
            'independence_group':'study-a', 'scopes':['operations'],
            'facts':[{'id':'count','value':12,'unit':'lots','period':'2025',
                      'population':'sample A','metric':'count'}]}],
            'claims':[{'id':'CL-001','kind':'gap','scope':'customer_need','status':'unknown',
                       'basis':'missing_evidence','rationale':'No customer baseline measured.',
                       'evidence_ids':[], 'independent_sources':0,
                       'targets':[{'artifact':'outputs/decision_review.md','quote':'Need remains unknown.'}]}]}
        self.review = {'checks':[{'id':c,'status':'pass','reason':'Reviewed bounded synthetic fixture.',
                                  'claim_ids':['CL-001']} for c in CHECKS]}
        self.save()
        # validate_quality also requires all old example refs in source registry.
        import re
        ids = set()
        for name in ['business_context_analysis.md','hypothesis_map.md','decision_review.md','human_report.html']:
            ids.update(re.findall(r'\b(?:EVID|EXT|CONF)-\d+\b', (self.run/'outputs'/name).read_text()))
        for sid in sorted(ids):
            self.ledger['sources'].append({'id':sid,'kind':'simulation',
                'independence_group':'demo','scopes':['simulation']})
        self.save()

    def save(self):
        self.write('outputs/claim_ledger.json', self.ledger)
        self.write('outputs/quality_review.json', self.review)

    def codes(self):
        self.save()
        return '\n'.join(validate_quality(self.run))

    def test_cli_requires_explicit_scope(self):
        p = subprocess.run([sys.executable, str(ROOT/'scripts/validate_runs.py')], capture_output=True)
        self.assertEqual(2, p.returncode)

    def test_cli_checks_requested_run_and_reports_target(self):
        (self.run/'outputs/human_report.html').unlink()
        capture = io.StringIO()
        with contextlib.redirect_stdout(capture):
            result = validator.main(['--run-dir',str(self.run),'--json'])
        report = json.loads(capture.getvalue())
        self.assertEqual(1,result)
        self.assertEqual(str(self.run),report['target'])
        self.assertEqual('run',report['scope'])
        self.assertEqual('FAIL',report['status'])

    def test_formatted_token_does_not_salvage_prose(self):
        self.assertEqual('unknown',machine_token('**unknown** — not measured'))
        self.assertEqual('additional_research',machine_token('`additional_research`'))
        self.assertIsNone(machine_token('probably unknown'))
        self.assertIsNone(machine_token('supported or unknown'))

    def test_vertical_plan_every_action_complete(self):
        from service_profile import PLAN_FIELDS
        table = '| Поле | Значение |\n|---|---|\n' + '\n'.join('| '+aliases[0]+' | measured value |' for aliases in PLAN_FIELDS)
        self.assertTrue(plan_tables_complete(table))
        self.assertFalse(plan_tables_complete(table+'\n\n| Поле | Значение |\n|---|---|\n| Гипотеза | incomplete |'))

    def test_protocol_requires_audit_but_legacy_remains_readable(self):
        self.assertEqual([],validate_quality(self.run))
        self.write('run_config.json',{'protocol_version':2})
        self.assertIn('MISSING_OR_INVALID_QUALITY_AUDIT',validator.check_run(self.run))

    def test_valid_declared_audit(self):
        self.audit()
        self.assertEqual([],validate_quality(self.run))
        self.assertEqual([],validator.check_run(self.run))

    def test_missing_evidence_cannot_be_refutation(self):
        self.audit();self.ledger['claims'][0]['status']='contradicted'
        self.assertIn('ABSENCE_IS_NOT_PROOF',self.codes())

    def test_role_simulation_cannot_confirm_customer_need(self):
        self.audit();c=self.ledger['claims'][0]
        c.update(status='supported',basis='simulation',evidence_ids=['EVID-001'])
        self.assertIn('SIMULATION_IS_NOT_EVIDENCE',self.codes())
        self.assertIn('EMPIRICAL_SCOPE_NOT_SUPPORTED',self.codes())

    def test_reprints_are_one_independent_source(self):
        self.audit();s=dict(self.ledger['sources'][0]);s['id']='SRC-002'
        self.ledger['sources'].append(s)
        self.ledger['claims'][0].update(evidence_ids=['SRC-001','SRC-002'],independent_sources=2)
        self.assertIn('INDEPENDENCE_OVERCOUNT',self.codes())

    def test_number_period_binding_and_correct_id(self):
        self.audit();fact=self.ledger['sources'][0]['facts'][0]
        c=self.ledger['claims'][0]
        c['numbers']=[dict(fact,source_id='SRC-001',fact_id='count')]
        self.assertEqual('',self.codes())
        c['numbers'][0]['period']='2024–2026'
        self.assertIn('NUMERIC_SCOPE_MISMATCH',self.codes())

    def test_changed_quote_or_missing_review_blocks_completion(self):
        self.audit();self.ledger['claims'][0]['targets'][0]['quote']='Need confirmed.'
        self.assertIn('CLAIM_TARGET_MISMATCH',self.codes())
        self.review['checks'].pop()
        self.assertIn('INCOMPLETE_QUALITY_REVIEW',self.codes())

    def test_global_market_absence_cannot_be_supported(self):
        self.audit();self.ledger['claims'][0].update(scope='global_market_absence',status='supported',
            basis='observed',evidence_ids=['SRC-001'],independent_sources=1)
        self.assertIn('UNBOUNDED_ABSENCE_CLAIM',self.codes())

    def test_finish_cannot_publish_completed_with_failed_actual_run(self):
        progress.init(self.run)
        (self.run/'outputs/decision_review.md').unlink()
        self.assertEqual('FAIL',control.finish(self.run)['status'])
        state=json.loads((self.run/'outputs/progress.json').read_text())
        self.assertEqual('error',state['phases'][-1]['state'])
        with self.assertRaises(ValueError):
            progress.record(self.run,phase='human_report',state='completed',message='done')

    def test_deep_analysis_requires_matching_user_choice(self):
        self.write('run_config.json',{'protocol_version':2,'analysis_choices':[]})
        with self.assertRaises(ValueError):control.require_deep(self.run,['file.xlsx'])
        control.analysis_choice(self.run,'quick',['file.xlsx'],'bounded view')
        with self.assertRaises(ValueError):control.require_deep(self.run,['file.xlsx'])
        control.analysis_choice(self.run,'deep',['file.xlsx'],'join sheets')
        control.require_deep(self.run,['file.xlsx'])
        with self.assertRaises(ValueError):control.require_deep(self.run,['other.xlsx'])

    def test_virtual_environment_is_excluded(self):
        from discover_sources import EXCLUDED
        self.assertTrue({'.venv','venv','site-packages'}.issubset(EXCLUDED))

    def test_viewer_verifies_real_http_and_run_identity(self):
        from functools import partial
        from http.server import ThreadingHTTPServer
        import threading
        progress.init(self.run)
        self.write('outputs/.viewer-identity.json',{'token':'test-only'})
        server=ThreadingHTTPServer(('127.0.0.1',0),partial(progress.Viewer,directory=str(self.run)))
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        url=f'http://127.0.0.1:{server.server_port}/'
        try:
            self.assertEqual(url+'outputs/progress.html',control.verify_viewer(url,self.run))
            with self.assertRaises(ValueError):control.verify_viewer('https://example.com/',self.run)
        finally:
            server.shutdown();server.server_close();thread.join()

    # Reuse the synthetic audited fixture, then exercise actual server startup.
    def test_prepare_viewer_reuse_and_successful_finish(self):
        from unittest.mock import patch
        real_popen = subprocess.Popen
        children=[]
        def launch(*args,**kwargs):
            child=real_popen(*args,**kwargs);children.append(child);return child
        self.audit()
        # Prepare may repeat intake/validation; it must preserve audit/config.
        with patch.object(control.subprocess,'Popen',side_effect=launch):
            try:
                url=control.prepare(self.run,'full')
                self.assertIn('/outputs/progress.html',url)
                self.assertEqual(url,control.viewer(self.run))
                self.assertEqual(1,len(children))
                self.assertEqual('PASS',control.finish(self.run)['status'])
                self.assertEqual('run',json.loads((self.run/'outputs/run_validation.json').read_text())['scope'])
                self.assertEqual([],validator.check_run(self.run))
            finally:
                for child in children:
                    child.terminate();child.wait(timeout=5)

    def test_legacy_viewer_does_not_silently_upgrade_protocol(self):
        real_popen=subprocess.Popen
        from unittest.mock import patch
        children=[]
        def launch(*args,**kwargs):
            child=real_popen(*args,**kwargs);children.append(child);return child
        progress.init(self.run)
        with patch.object(control.subprocess,'Popen',side_effect=launch):
            try:
                control.viewer(self.run)
                self.assertFalse((self.run/'run_config.json').exists())
                self.assertEqual([],validator.check_run(self.run))
            finally:
                for child in children:
                    child.terminate();child.wait(timeout=5)


if __name__=='__main__': unittest.main()
