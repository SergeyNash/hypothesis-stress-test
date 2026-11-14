import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'scripts'), str(ROOT / 'tests')]
import runtime_metrics as metrics
import run_control as control
import run_progress as progress
import phase_checks
from audit_records import put_claims
import test_lifecycle as lifecycle_fixture
import test_run_quality as quality_fixture
from benchmark_policy import input_digest


class GateOptimization(unittest.TestCase):
    def setUp(self):
        self.fixture = lifecycle_fixture.Lifecycle(); self.fixture.setUp()
        self.run = self.fixture.run
        self.fixture.enable_handoff()
        from source_selection import select
        select(self.run,dict(local=False,confluence=False,internet=False),[],reason='Controlled regression fixture')
    def tearDown(self): self.fixture.tearDown()

    def test_complete_checks_current_phase_once_and_next_call_catches_changes(self):
        with patch.object(phase_checks,'check',wraps=phase_checks.check) as checks:
            result=control.complete(self.run,'facilitator')
        self.assertEqual('PASS',result['status'])
        self.assertEqual(['facilitator'],[c.args[1] for c in checks.call_args_list])
        self.assertEqual('local_evidence',result['next_phase'])
        self.assertTrue(result['next_prepared'])
        (self.run/'outputs/hypothesis_summary.md').write_text('',encoding='utf-8')
        self.assertEqual('FAIL',control.complete(self.run,'local_evidence')['status'])

    def test_receipt_cannot_escape_its_command_or_cover_another_run(self):
        with phase_checks.verified_transition(self.run,'facilitator') as receipt:
            self.assertTrue(phase_checks.accepts(receipt,self.run,'facilitator','completed'))
            self.assertFalse(phase_checks.accepts(receipt,self.run.parent/'other','facilitator','completed'))
        with self.assertRaisesRegex(ValueError,'expired'):
            progress.record(self.run,phase='facilitator',state='completed',message='must reject',_transition=True,_verified=receipt)
        with self.assertRaisesRegex(ValueError,'receipt'):
            progress.record(self.run,phase='facilitator',state='completed',message='must reject',_transition=True,_verified=True)

    def test_claim_batch_is_single_write_and_validation_failure_is_not_partial(self):
        target=self.run/'outputs/hypothesis_summary.md'
        first='There is no customer evidence for the scheduled discussion.'
        second='The preparation cost has not been measured.'
        target.write_text(first+'\n'+second,encoding='utf-8')
        def item(identifier,quote):
            return dict(id=identifier,kind='gap',basis='missing_evidence',status='unknown',scope='operations',
                        rationale='No observations available in this controlled fixture.',evidence_ids=[],independent_sources=0,
                        targets=[{'artifact':'outputs/hypothesis_summary.md','quote':quote}])
        path=self.run/'outputs/claim_ledger.json';before=path.read_bytes()
        with self.assertRaises(ValueError):put_claims(self.run,[item('CL-001',first),item('CL-002','not in the artifact')])
        self.assertEqual(before,path.read_bytes())
        import audit_records
        with patch.object(audit_records,'atomic',wraps=audit_records.atomic) as writes:
            put_claims(self.run,[item('CL-001',first),item('CL-002',second)])
        self.assertEqual(1,len([c for c in writes.call_args_list if c.args[0]==path]))
        with self.assertRaises(ValueError):put_claims(self.run,[item('CL-003',first),item('CL-003',second)])
        self.assertEqual(2,len(json.loads(path.read_text(encoding='utf-8'))['claims']))


    def test_normal_complete_cli_emits_metrics_without_a_second_command(self):
        output=subprocess.check_output([sys.executable,str(ROOT/'scripts/run_control.py'),'complete','--run-dir',str(self.run),'--phase','facilitator'],encoding='utf-8')
        report=json.loads(output)
        self.assertEqual('PASS',report['status']);self.assertTrue(report['next_prepared'])
        result=json.loads((self.run/'outputs/performance_summary.json').read_text(encoding='utf-8'))
        self.assertEqual(1,result['instrumented_command_calls'])
        self.assertEqual(1,result['validation_sections']['phase_validation:facilitator']['calls'])



class FullAuditOnce(unittest.TestCase):
    def test_finish_performs_real_full_audit_once_and_still_rejects_bad_report(self):
        fixture=quality_fixture.RunQuality();fixture.setUp()
        try:
            fixture.audit()
            import validate_runs
            original=validate_runs.check_run
            calls=[]
            def counted(*args,**kwargs):calls.append(True);return original(*args,**kwargs)
            with patch.object(control,'check_run',side_effect=counted),patch.object(progress,'check_run',side_effect=counted):
                result=control.finish(fixture.run)
            self.assertEqual('PASS',result['status']);self.assertEqual(1,len(calls))
            (fixture.run/'outputs/human_report.html').write_text('broken report',encoding='utf-8')
            self.assertEqual('FAIL',control.finish(fixture.run)['status'])
        finally:fixture.tearDown()


class TimingSummary(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.run=Path(self.temp.name)/'HYP-2026-11-14-001'
        (self.run/'outputs').mkdir(parents=True)
    def tearDown(self):self.temp.cleanup()
    def write(self,name,value):
        path=self.run/name;path.write_text(json.dumps(value),encoding='utf-8')
    def lines(self,name,rows):
        (self.run/name).write_text(''.join(json.dumps(r)+'\n' for r in rows),encoding='utf-8')

    def test_waits_and_overlapping_processes_are_unioned_not_double_counted(self):
        base=datetime(2026,11,14,tzinfo=timezone.utc)
        at=lambda seconds:(base+timedelta(seconds=seconds)).isoformat()
        events=[dict(at=at(0),kind='phase',phase='intake',state='completed'),
                dict(at=at(2),kind='phase',phase='local_evidence',state='waiting_user'),
                dict(at=at(4),kind='source',phase='business_context',channel='internet',state='waiting_approval'),
                dict(at=at(8),kind='phase',phase='local_evidence',state='running'),
                dict(at=at(10),kind='source',phase='business_context',channel='internet',state='read'),
                dict(at=at(12),kind='phase',phase='human_report',state='completed')]
        self.lines('outputs/pipeline_events.jsonl',events)
        self.lines('outputs/command_metrics.jsonl',[dict(script='run_control',action='complete',started_at=at(a),ended_at=at(b),duration_ms=(b-a)*1000,cpu_ms=10,exit_code=0) for a,b in [(1,5),(4,7)]])
        result=metrics.summarize(self.run)
        self.assertEqual(12,result['elapsed_seconds']);self.assertEqual(8,result['registered_wait_seconds'])
        self.assertEqual(6,result['observed_script_wall_union_seconds']);self.assertEqual(3,result['unattributed_seconds'])
        self.assertEqual(2,result['instrumented_command_calls'])

    def test_unrecorded_gap_is_not_invented_as_wait_or_reasoning(self):
        self.lines('outputs/pipeline_events.jsonl',[dict(at='2026-11-14T00:00:00Z',kind='phase',phase='intake',state='completed'),dict(at='2026-11-14T00:10:00Z',kind='phase',phase='human_report',state='completed')])
        result=metrics.summarize(self.run)
        self.assertEqual(0,result['registered_wait_seconds']);self.assertEqual(600,result['unattributed_seconds'])
        self.assertEqual('journal_only',result['coverage'])

    def test_existing_cli_records_success_and_failure_without_extra_model_call(self):
        self.write('run_config.json',{'protocol_version':2,'timing_version':1})
        command=[sys.executable,str(ROOT/'scripts/audit_records.py'),'init','--run-dir',str(self.run)]
        subprocess.run(command,check=True,capture_output=True)
        bad=subprocess.run(command[:2]+['claim','--run-dir',str(self.run)],capture_output=True)
        self.assertNotEqual(0,bad.returncode)
        records=metrics.read_lines(self.run/'outputs/command_metrics.jsonl')
        self.assertEqual(2,len(records));self.assertEqual([0,2],[r['exit_code'] for r in records])
        self.assertTrue(all(r['duration_ms']>=0 and r['cpu_ms']>=0 for r in records))
        self.assertTrue((self.run/'outputs/performance_summary.json').is_file())

    def test_historical_cli_and_diagnostic_summary_do_not_create_metrics(self):
        self.write('run_config.json',{'protocol_version':2})
        subprocess.run([sys.executable,str(ROOT/'scripts/audit_records.py'),'init','--run-dir',str(self.run)],check=True,capture_output=True)
        before={p.name:p.read_bytes() for p in (self.run/'outputs').iterdir()}
        subprocess.run([sys.executable,str(ROOT/'scripts/run_control.py'),'metrics','--run-dir',str(self.run)],check=True,capture_output=True)
        self.assertEqual(before,{p.name:p.read_bytes() for p in (self.run/'outputs').iterdir()})


    def test_standalone_validator_remains_read_only_for_timed_runs(self):
        self.write('run_config.json',{'protocol_version':2,'timing_version':1})
        before={str(p.relative_to(self.run)):p.read_bytes() for p in self.run.rglob('*') if p.is_file()}
        subprocess.run([sys.executable,str(ROOT/'scripts/validate_runs.py'),'--run-dir',str(self.run),'--json'],capture_output=True)
        after={str(p.relative_to(self.run)):p.read_bytes() for p in self.run.rglob('*') if p.is_file()}
        self.assertEqual(before,after)


    def test_timing_failure_does_not_change_command_result(self):
        import contextlib, io, time
        stderr=io.StringIO()
        with patch.object(sys,'argv',['audit_records.py','init','--run-dir',str(self.run)]),patch.object(metrics,'persist',side_effect=OSError('synthetic timing storage failure')),contextlib.redirect_stderr(stderr):
            result=metrics.execute(lambda:0,'audit_records',time.perf_counter(),time.process_time())
        self.assertEqual(0,result)
        self.assertIn('Timing unavailable',stderr.getvalue())


class FixedBenchmark(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.run=self.root/'runs/HYP-2026-11-14-001';(self.run/'input').mkdir(parents=True)
        text=(ROOT/'benchmarks/pipeline-001/hypothesis.md').read_text(encoding='utf-8')
        self.text=text.replace('{{HYPOTHESIS_ID}}',self.run.name).replace('{{DATE}}','2026-11-14').replace('{{RUN_ID}}','RUN-2026-11-14-001')
        (self.run/'input/hypothesis.md').write_text(self.text,encoding='utf-8')
    def tearDown(self):self.temp.cleanup()
    def prepare(self):
        with patch.object(control,'viewer',return_value='http://127.0.0.1:8787/outputs/progress.html'):
            return control.prepare(self.run,'full',benchmark_case='pipeline-001',model_label='controlled-model / fixed reasoning')

    def test_identity_changes_are_allowed_but_substantive_changes_rejected(self):
        self.assertEqual(input_digest(self.text),input_digest(self.text.replace('Статус: draft','Статус: completed')))
        (self.run/'input/hypothesis.md').write_text(self.text.replace('15-минутный','30-минутный'),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'differs'):self.prepare()
        self.assertFalse((self.run/'run_config.json').exists())

    def test_model_and_channels_are_pinned_and_no_silent_metadata_relabel(self):
        self.prepare();config=control.load_config(self.run)
        self.assertEqual('pipeline-001',config['benchmark']['case_id'])
        self.assertEqual('controlled-model / fixed reasoning',config['model_label'])
        from source_selection import select
        with self.assertRaisesRegex(ValueError,'fixed'):select(self.run,dict(local=False,confluence=False,internet=True),[],reason='would break comparison')
        select(self.run,dict(local=False,confluence=False,internet=False),[],reason='Fixed benchmark user authorization')
        with self.assertRaisesRegex(ValueError,'relabelled'):
            control.prepare(self.run,'full',benchmark_case='pipeline-001',model_label='other-model')

    def test_changed_benchmark_input_is_rejected_on_resume_and_final_audit(self):
        self.prepare()
        from source_selection import select
        select(self.run,dict(local=False,confluence=False,internet=False),[],reason='Fixed benchmark choice')
        (self.run/'input/hypothesis.md').write_text(self.text.replace('15-минутный','30-минутный'),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'differs'):control.prepare(self.run,'full')
        from benchmark_policy import validate
        self.assertIn('BENCHMARK_INPUT_CHANGED',validate(self.run))
