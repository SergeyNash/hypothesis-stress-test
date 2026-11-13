import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from source_selection import select,require,options,validate
from run_progress import init,record,snapshot,events
from run_control import prepare,load_config,start
from source_snapshot import capture


class SourceSelection(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.run=self.root/'runs/HYP-2026-11-09-001'
        shutil.copytree(ROOT/'examples/example-005',self.run)
        # Fresh input, not a retrofitted complete example.
        shutil.rmtree(self.run/'outputs');(self.run/'outputs').mkdir()
        with patch('run_control.viewer',return_value='http://127.0.0.1:8787/outputs/progress.html'):
            prepare(self.run,'full')
        (self.root/'allowed').mkdir();(self.root/'outside').mkdir()
        (self.root/'allowed/note.txt').write_text('source')
        (self.root/'outside/note.txt').write_text('source')
    def tearDown(self):self.tmp.cleanup()
    def choose(self,local=True,confluence=True,internet=False,paths=None,remember=False):
        return select(self.run,dict(local=local,confluence=confluence,internet=internet),paths or [],remember=remember,reason='Actual synthetic user selection')

    def test_new_run_blocks_collection_until_choice_but_has_progress(self):
        self.assertTrue((self.run/'outputs/progress.json').exists())
        self.assertTrue(options(self.run)['confirmation_required'])
        with self.assertRaises(ValueError):start(self.run,'business_context')
        with self.assertRaises(ValueError):record(self.run,phase='market',state='query_started',channel='internet',message='search')

    def test_selected_channels_guard_events_and_capture(self):
        self.choose()
        require(self.run,'confluence')
        with self.assertRaises(ValueError):require(self.run,'internet')
        with self.assertRaises(ValueError):record(self.run,phase='market',state='read',channel='internet',message='not allowed')
        record(self.run,phase='business_context',channel='confluence',state='query_started',message='allowed',query='catalog')
        capture(self.run,self.root,['allowed/note.txt'])
        self.assertEqual([],validate(self.run))

    def test_restricts_paths_before_reading_and_remote_origin_not_local_scope(self):
        self.choose(paths=['allowed'])
        require(self.run,'local',self.root/'allowed/note.txt')
        for p in [self.root,self.root/'outside/note.txt']:
            with self.assertRaises(ValueError):require(self.run,'local',p)
        with self.assertRaises(ValueError):capture(self.run,self.root,['outside/note.txt'])
        self.assertEqual([],json.loads((self.run/'outputs/source_snapshot.json').read_text())['files'])
        capture(self.run,self.root,['outside/note.txt'],channel='confluence')
        with self.assertRaises(ValueError):self.choose(paths=['../'])

    def test_preferences_are_proposals_and_not_automatic_consent(self):
        self.choose(remember=True)
        second=self.root/'runs/HYP-2026-11-09-002';second.mkdir()
        (second/'run_config.json').write_text(json.dumps({'source_selection_version':1}))
        proposed=options(second)
        self.assertFalse(proposed['proposal']['channels']['internet'])
        self.assertTrue(proposed['confirmation_required'])
        with self.assertRaises(ValueError):require(second,'local')
        self.assertFalse((second/'outputs').exists())

    def test_switch_preserves_prior_evidence_and_validates_against_effective_choice(self):
        self.choose(internet=True)
        record(self.run,phase='market',channel='internet',state='read',message='read before disable')
        self.choose(internet=False)
        self.assertEqual([],validate(self.run))
        self.choose(internet=True)
        require(self.run,'internet')
        self.assertEqual([],validate(self.run))
        self.assertEqual(3,len(load_config(self.run)['source_selection_history']))
        state=snapshot(self.run,events(self.run/'outputs'))
        self.assertTrue(state['source_selection']['channels']['internet'])
        self.assertTrue(any(e['message']=='read before disable' for e in state['events']))

    def test_all_disabled_is_valid_but_report_must_disclose(self):
        self.choose(False,False,False)
        self.assertEqual([],validate(self.run))
        (self.run/'outputs/human_report.html').write_text('<html>summary</html>')
        self.assertEqual(3,len(validate(self.run)))
        (self.run/'outputs/human_report.html').write_text('Локальная база знаний — отключён пользователем\nConfluence — отключён пользователем\nИнтернет — отключён пользователем',encoding='utf-8')
        self.assertEqual([],validate(self.run))

    def test_historical_run_is_not_migrated_on_resume(self):
        (self.run/'run_config.json').write_text('{}')
        require(self.run,'internet')
        self.assertEqual([],validate(self.run))

    def test_tampered_event_while_disabled_fails_audit(self):
        self.choose()
        path=self.run/'outputs/pipeline_events.jsonl';rows=events(self.run/'outputs')
        rows.append(dict(id=len(rows)+1,phase='market',kind='source',channel='internet',state='read',message='bypass',at='2026-11-12T00:00:00Z'))
        path.write_text('\n'.join(json.dumps(e) for e in rows))
        self.assertIn('SOURCE_OPERATION_WITHOUT_PERMISSION:internet',validate(self.run))

if __name__=='__main__':unittest.main()
