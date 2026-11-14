import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from run_progress import snapshot, display_events, events


class PassiveMonitoring(unittest.TestCase):
    def test_incomplete_source_does_not_drop_good_events_or_complete_missing_phases(self):
        with tempfile.TemporaryDirectory() as temp:
            run=Path(temp)/'HYP-2026-11-14-002';out=run/'outputs';out.mkdir(parents=True)
            source=dict(id=5,kind='source',channel='internet',state='declined',at='2026-11-14T13:00:00+00:00',message='Internet disabled')
            phase=dict(id=6,kind='phase',phase='facilitator',state='running',at='2026-11-14T13:01:00+00:00',message='Roles in progress')
            path=out/'pipeline_events.jsonl'
            path.write_text(json.dumps(source)+'\n'+json.dumps(phase)+'\n{"id":7,',encoding='utf-8')
            original=path.read_bytes()
            rows,warnings=display_events(out)
            view=snapshot(run,rows,reader_warnings=warnings)
            self.assertEqual(2,len(view['events']))
            self.assertEqual('',view['events'][0]['phase'])
            self.assertNotIn('phase',rows[0])  # Projection never mutates its input either.
            self.assertEqual('declined',view['events'][0]['state'])
            states={p['id']:p['state'] for p in view['phases']}
            self.assertEqual('running',states['facilitator'])
            self.assertEqual('pending',states['intake']);self.assertEqual('pending',states['validation'])
            self.assertEqual(0,view['completed'])
            self.assertTrue(any('без этапа' in w for w in view['warnings']))
            self.assertTrue(any('строка' in w for w in view['warnings']))
            with self.assertRaises(ValueError):events(out)  # Audit/control parser was not weakened.
            self.assertEqual(original,path.read_bytes())

    def test_bad_phase_and_non_object_rows_cannot_change_completion(self):
        with tempfile.TemporaryDirectory() as temp:
            run=Path(temp);(run/'outputs').mkdir()
            view=snapshot(run,[None,[],dict(kind='phase',phase='human_report',state='completed',message='missing timestamp'),dict(kind='phase',phase='unknown',state='completed',message='bad phase',at='2026-11-14T13:00:00+00:00')])
            self.assertEqual([],view['events']);self.assertEqual(0,view['completed'])
            self.assertEqual(4,len(view['warnings']))

    def test_rich_view_accepts_unbound_source_without_repairing_it(self):
        try:
            from terminal_progress import validate_state
        except SystemExit:
            self.skipTest('Optional Rich/Click dependencies unavailable')
        source=dict(kind='source',channel='internet',state='declined',at='2026-11-14T13:00:00+00:00',message='Disabled')
        view=validate_state(dict(phases=[dict(id='intake',name='Input',state='pending')],events=[source]))
        self.assertEqual('',view['events'][0]['phase'])
        self.assertEqual('pending',view['phases'][0]['state'])
        self.assertNotIn('phase',source)
