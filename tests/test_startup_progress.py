import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from startup_progress import update, attach, pending_snapshot, read
from active_run import Follow, publish
from run_progress import events
import run_control


class StartupProgressTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def run_dir(self, name='HYP-2026-11-13-001'):
        run = self.root / 'runs' / name
        (run / 'input').mkdir(parents=True)
        (run / 'input/hypothesis.md').write_text('# draft awaiting validation', encoding='utf-8')
        return run

    def test_visible_before_run_exists_and_wait_has_no_completed_phases(self):
        first = update(self.root, stage='routing', message='Разбираю вход')
        self.assertFalse((self.root / 'runs').exists())
        update(self.root, session=first['session_id'], stage='confirmation', status='waiting_user', message='Жду подтверждения')
        view, issue, run = Follow(self.root).poll(lambda _: self.fail('No run to read yet'))
        self.assertIsNone(issue)
        self.assertIsNone(run)
        self.assertEqual(0, view['completed'])
        self.assertEqual('waiting_user', view['phases'][0]['state'])
        self.assertEqual('Жду подтверждения', view['events'][-1]['message'])

    def test_attach_preserves_early_time_and_does_not_validate_input(self):
        first = update(self.root)
        run = self.run_dir()
        attached = attach(self.root, first['session_id'], run)
        self.assertEqual('attached', attached['state'])
        self.assertIsNone(pending_snapshot(self.root))
        history = [json.loads(s) for s in (run / 'outputs/startup_events.jsonl').read_text().splitlines()]
        self.assertEqual(first['at'], history[0]['at'])
        rows = events(run / 'outputs')
        self.assertEqual([('intake', 'completed'), ('validation', 'running')], [(e['phase'], e['state']) for e in rows])
        self.assertFalse((run / 'run_config.json').exists())
        with self.assertRaises(ValueError):
            run_control.prepare(run, 'full')
        self.assertEqual('error', events(run / 'outputs')[-1]['state'])
        attach(self.root, first['session_id'], run)
        self.assertEqual(3, len(events(run / 'outputs')))

    def test_follows_attached_run_after_replacing_old_display(self):
        old = self.run_dir()
        (old / 'outputs').mkdir()
        publish(old)
        follower = Follow(self.root)
        first = update(self.root)
        self.assertTrue(follower.poll(lambda _: {})[0]['startup'])
        new = self.run_dir('HYP-2026-11-13-002')
        attach(self.root, first['session_id'], new)
        view, issue, target = follower.poll(lambda p: json.loads(p.read_text()))
        self.assertEqual(new, target)
        self.assertEqual(new.name, view['run'])

    def test_stale_session_cannot_overwrite_newer_start(self):
        first = update(self.root)
        second = update(self.root)
        with self.assertRaises(ValueError):
            update(self.root, session=first['session_id'])
        self.assertEqual(second['session_id'], read(self.root)['session_id'])
        self.assertEqual(2, len(list((self.root / '.hst/startups').glob('*.jsonl'))))

    def test_cancel_does_not_create_run_or_attach(self):
        first = update(self.root)
        update(self.root, session=first['session_id'], status='cancelled', message='Отменено')
        self.assertIsNone(pending_snapshot(self.root))
        self.assertFalse((self.root / 'runs').exists())
        with self.assertRaises(ValueError):
            attach(self.root, first['session_id'], self.run_dir())

    def test_symlinks_and_external_attach_rejected(self):
        (self.root / '.hst').symlink_to(self.root.parent, target_is_directory=True)
        with self.assertRaises(ValueError):
            update(self.root)
        (self.root / '.hst').unlink()
        first = update(self.root)
        with self.assertRaises(ValueError):
            attach(self.root, first['session_id'], ROOT / 'examples/example-005')
