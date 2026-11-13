import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import run_control as control
import run_progress as progress
from phase_checks import diagnose
from audit_records import put


class Lifecycle(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.run=self.root/'runs/HYP-2026-11-09-001'
        shutil.copytree(ROOT/'examples/example-005',self.run)
        shutil.rmtree(self.run/'outputs');(self.run/'outputs').mkdir()
        for name in ['hypothesis_summary.md','validation_questions.md','role_outputs']:
            source=ROOT/'examples/example-005/outputs'/name
            if source.is_dir():shutil.copytree(source,self.run/'outputs'/name)
            else:shutil.copyfile(source,self.run/'outputs'/name)
        with patch.object(control,'viewer',return_value='http://127.0.0.1:8787/outputs/progress.html'):
            control.prepare(self.run,'full')
        # These tests isolate the original lifecycle; handoff v1 has its own cases below.
        config=control.load_config(self.run);config.pop('phase_handoff_version',None);control.save_config(self.run,config)
    def tearDown(self):self.tmp.cleanup()

    def test_single_completion_command_and_idempotent_recovery(self):
        self.assertEqual('PASS',control.complete(self.run,'facilitator')['status'])
        rows=progress.events(self.run/'outputs')
        self.assertEqual('completed',rows[-1]['state'])
        self.assertEqual([],diagnose(self.run,rows))
        self.assertEqual('PASS',control.complete(self.run,'facilitator')['status'])
        self.assertEqual(rows,progress.events(self.run/'outputs'))
        # Simulate interruption after marker write, before durable event append.
        p=self.run/'outputs/pipeline_events.jsonl'
        p.write_text('\n'.join(json.dumps(r) for r in rows[:-1])+'\n')
        self.assertTrue(diagnose(self.run,rows[:-1]))
        self.assertEqual('PASS',control.complete(self.run,'facilitator')['status'])
        self.assertEqual([],diagnose(self.run,progress.events(self.run/'outputs')))

    def test_marker_alone_cannot_start_next_phase(self):
        from source_selection import select
        select(self.run,dict(local=True,confluence=False,internet=False),[],reason='Synthetic user choice')
        shutil.copyfile(ROOT/'examples/example-005/outputs/ready_for_synthesis.marker',self.run/'outputs/ready_for_synthesis.marker')
        with self.assertRaisesRegex(ValueError,'journal'):
            progress.record(self.run,phase='local_evidence',state='running',message='must not start')

    def test_missing_sources_fail_at_local_stage_not_final_report(self):
        from source_selection import select
        control.complete(self.run,'facilitator')
        select(self.run,dict(local=True,confluence=False,internet=False),[],reason='Synthetic choice')
        for name in ['discovery_preview.md','evidence_inventory.md']:
            shutil.copyfile(ROOT/'examples/example-005/outputs'/name,self.run/'outputs'/name)
        result=control.complete(self.run,'local_evidence')
        self.assertEqual('FAIL',result['status'])
        self.assertTrue(any('UNREGISTERED_EVIDENCE' in e for e in result['errors']),result)
        self.assertFalse((self.run/'outputs/knowledge_retrieval_complete.marker').exists())
        self.assertTrue((self.run/'outputs/phase_validation.json').exists())

    def test_finish_exception_leaves_diagnostic_not_false_completion(self):
        # Legacy mode isolates unexpected checker exceptions from prerequisite validation.
        (self.run/'run_config.json').write_text(json.dumps({'protocol_version':2}))
        with patch.object(control,'check_run',side_effect=RuntimeError('synthetic checker crash')):
            result=control.finish(self.run)
        self.assertEqual('ERROR',result['status'])
        self.assertIn('synthetic checker crash',result['errors'][0])
        stored=json.loads((self.run/'outputs/run_validation.json').read_text())
        self.assertEqual('ERROR',stored['status'])
        self.assertFalse((self.run/'outputs/human_report_complete.marker').exists())
        self.assertEqual('error',progress.events(self.run/'outputs')[-1]['state'])

    def test_viewer_failure_is_visible_before_roles(self):
        with patch.object(control,'viewer',side_effect=ValueError('synthetic host failure')):
            with self.assertRaises(ValueError):control.prepare(self.run,'full')
        self.assertEqual('error',control.load_config(self.run)['viewer']['status'])
        self.assertEqual('error',json.loads((self.run/'outputs/progress.json').read_text())['viewer']['status'])

    def test_record_helper_rejects_invented_source_anchors_and_claim_enums(self):
        source={'id':'EVID-001','kind':'customer_record','independence_group':'test','scopes':['operations'],
                'anchor_ids':['EVID-001'],'role':'reported_fact','quote':'text'}
        with self.assertRaisesRegex(ValueError,'anchor IDs'):put(self.run,'source',source)
        with self.assertRaisesRegex(ValueError,'kind/basis'):
            put(self.run,'claim',{'id':'CL-001','kind':'observation','basis':'partial_evidence'})

    def test_generated_evid_and_snapshot_pass_local_gate(self):
        from source_selection import select
        from source_snapshot import capture
        control.complete(self.run,'facilitator')
        select(self.run,dict(local=True,confluence=False,internet=False),[],reason='Synthetic user selection')
        source=self.root/'note.txt';source.write_text('Scheduled restores have not been tested.',encoding='utf-8')
        snap=capture(self.run,self.root,['note.txt'])
        anchor=snap['files'][0]['units'][0]['anchor_id']
        put(self.run,'source',{'id':'EVID-001','kind':'provider_record','role':'reported_fact',
            'independence_group':'synthetic-source','scopes':['operations'],'anchor_ids':[anchor],
            'quote':source.read_text(),'facts':[],
            'inventory':{'observation':source.read_text(),'relevance':'backup operations','relevance_reason':'An operating observation, not paid demand.',
                         'source_origin':'provider_record','evidence_status':'reported'}})
        (self.run/'outputs/discovery_preview.md').write_text('Synthetic source found; no claim of live customer research.')
        with (self.run/'outputs/evidence_inventory.md').open('a') as f:f.write('\n## Retrieval Review\n- status: accepted\n')
        result=control.complete(self.run,'local_evidence')
        self.assertEqual('PASS',result['status'],result)
        self.assertEqual('completed',progress.events(self.run/'outputs')[-1]['state'])

    def test_terminal_rebuilds_from_journal_when_snapshot_is_stale(self):
        try:from terminal_progress import read_state
        except SystemExit:self.skipTest('optional terminal deps missing')
        (self.run/'outputs/progress.json').write_text('{stale')
        self.assertEqual(2,read_state(self.run/'outputs/progress.json')['completed'])

    def enable_handoff(self,mode='full'):
        config=control.load_config(self.run)
        config.update(phase_handoff_version=1,execution_mode=mode,
                      viewer={'status':'unavailable','notified':True,'reason':'Synthetic host limitation disclosed'})
        control.save_config(self.run,config)

    def test_full_run_starts_preparation_before_model_output_and_does_not_duplicate(self):
        from source_selection import select
        self.enable_handoff()
        select(self.run,dict(local=False,confluence=False,internet=False),[],reason='Synthetic choice')
        rows=progress.events(self.run/'outputs')
        self.assertEqual(('facilitator','running'),(rows[-1]['phase'],rows[-1]['state']))
        self.assertIn('Подготовка',rows[-1]['message'])
        with patch.object(control,'viewer',return_value='http://127.0.0.1:1/'):
            control.start(self.run,'facilitator')
        self.assertEqual(rows,progress.events(self.run/'outputs'))
        self.assertEqual('PASS',control.complete(self.run,'facilitator')['status'])
        rows=progress.events(self.run/'outputs')
        self.assertEqual(('local_evidence','running'),(rows[-1]['phase'],rows[-1]['state']))
        self.assertEqual(('facilitator','completed'),(rows[-2]['phase'],rows[-2]['state']))

    def test_phase_mode_does_not_auto_start_and_completion_requires_start(self):
        from source_selection import select
        self.enable_handoff(mode='phase')
        select(self.run,dict(local=False,confluence=False,internet=False),[],reason='Synthetic choice')
        result=control.complete(self.run,'facilitator')
        self.assertEqual('FAIL',result['status'])
        self.assertIn('no recorded start',result['errors'][0])
        self.assertFalse((self.run/'outputs/ready_for_synthesis.marker').exists())
        control.start(self.run,'facilitator')
        self.assertEqual('PASS',control.complete(self.run,'facilitator')['status'])
        self.assertEqual('facilitator',progress.events(self.run/'outputs')[-1]['phase'])

    def test_changed_sources_do_not_reset_a_waiting_phase(self):
        from source_selection import select
        self.enable_handoff()
        select(self.run,dict(local=False,confluence=False,internet=False),[],reason='First choice')
        control.complete(self.run,'facilitator')
        progress.record(self.run,phase='local_evidence',state='waiting_user',message='Inventory review')
        select(self.run,dict(local=True,confluence=False,internet=False),[],reason='Changed local channel')
        last=next(e for e in reversed(progress.events(self.run/'outputs')) if e['kind']=='phase')
        self.assertEqual('waiting_user',last['state'])

if __name__=='__main__':unittest.main()
