import contextlib
from datetime import datetime, timezone, timedelta
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'tests')]
import validate_runs
import run_progress
from run_clock import clock, display
import test_grounded_audit as grounded_fixture
import test_tui_control as tui_fixture


class DialogueRun(unittest.TestCase):
    def test_tui_bootstrap_never_prepares_viewer_or_auto_starts_analysis(self):
        fixture=tui_fixture.TUIControlTests(); fixture.setUp()
        try:
            fixture.payload['model_label']='Local model X / reasoning high'
            with patch('run_control.prepare', side_effect=AssertionError('controller used')), patch('run_control.viewer', side_effect=AssertionError('viewer used')), patch('run_control.auto_enter', side_effect=AssertionError('automatic handoff')):
                request, run=fixture.accept()
            cfg=json.loads((run/'run_config.json').read_text(encoding='utf-8'))
            self.assertEqual('dialogue',cfg['execution_driver'])
            self.assertEqual(2,cfg['audit_version'])
            self.assertEqual('Local model X / reasoning high',cfg['model_label'])
            self.assertNotIn('lifecycle_version',cfg)
            self.assertFalse(any(e['phase']=='facilitator' for e in run_progress.events(run/'outputs')))
            from source_selection import require
            old=fixture.root/'runs/HYP-2026-11-13-002';old.mkdir()
            with self.assertRaisesRegex(ValueError,'isolation'):require(run,'local',old)
            require(run,'local',fixture.root/'materials')
        finally:fixture.tearDown()

    def test_missing_model_is_unknown_not_inferred(self):
        fixture=tui_fixture.TUIControlTests();fixture.setUp()
        try:
            _,run=fixture.prepare()
            self.assertIsNone(json.loads((run/'run_config.json').read_text(encoding='utf-8'))['model_label'])
        finally:fixture.tearDown()

    def test_full_grounded_audit_preserves_startup_and_has_no_transition(self):
        fixture=grounded_fixture.GroundedAudit();fixture.setUp()
        try:
            cfg=fixture.config|{'execution_driver':'dialogue','model_label':None}
            fixture.write('run_config.json',cfg)
            (fixture.run/'outputs/startup_events.jsonl').write_text('{"at":"2026-11-14T13:00:00+00:00"}\n',encoding='utf-8')
            marker=fixture.run/'outputs/human_report_complete.marker';marker.unlink()
            journal=(fixture.run/'outputs/pipeline_events.jsonl').read_bytes()
            before={p.relative_to(fixture.run):p.read_bytes() for p in fixture.run.rglob('*') if p.is_file()}
            with contextlib.redirect_stdout(io.StringIO()):
                result=validate_runs.main(['--run-dir',str(fixture.run),'--pending-report','--json'])
            self.assertEqual(0,result)
            self.assertEqual(before,{p.relative_to(fixture.run):p.read_bytes() for p in fixture.run.rglob('*') if p.is_file()})
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(0,validate_runs.main(['--run-dir',str(fixture.run),'--pending-report','--save-report','--json']))
            self.assertFalse(marker.exists())
            self.assertEqual(journal,(fixture.run/'outputs/pipeline_events.jsonl').read_bytes())
            self.assertEqual('PASS',json.loads((fixture.run/'outputs/run_validation.json').read_text(encoding='utf-8'))['status'])
            (fixture.run/'outputs/human_report.html').write_text('broken',encoding='utf-8')
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(1,validate_runs.main(['--run-dir',str(fixture.run),'--pending-report','--save-report','--json']))
            history=[json.loads(l) for l in (fixture.run/'outputs/validation_history.jsonl').read_text(encoding='utf-8').splitlines()]
            self.assertEqual(['PASS','FAIL'],[h['status'] for h in history])
        finally:fixture.tearDown()

    def test_dialogue_cannot_silently_downgrade_the_final_audit(self):
        fixture=grounded_fixture.GroundedAudit();fixture.setUp()
        try:
            fixture.write('run_config.json',fixture.config|{'execution_driver':'dialogue','audit_version':1})
            self.assertIn('DIALOGUE_REQUIRES_AUDIT_V2',validate_runs.check_run(fixture.run))
            fixture.write('run_config.json',fixture.config|{'execution_driver':'dialogue','lifecycle_version':1})
            self.assertIn('DIALOGUE_CONTROLLER_CONFLICT',validate_runs.check_run(fixture.run))
        finally:fixture.tearDown()

    def test_phase_checker_saves_diagnostic_without_marker_or_start(self):
        fixture=grounded_fixture.GroundedAudit();fixture.setUp()
        try:
            marker=fixture.run/'outputs/ready_for_synthesis.marker';marker.unlink()
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(0,validate_runs.main(['--run-dir',str(fixture.run),'--phase','facilitator','--save-report','--json']))
            self.assertFalse(marker.exists())
            report=json.loads((fixture.run/'outputs/phase_validation.json').read_text(encoding='utf-8'))
            self.assertEqual('facilitator',report['phase'])
        finally:fixture.tearDown()

    def test_elapsed_includes_preparation_freezes_and_recovers_without_writes(self):
        t=datetime(2026,11,14,12,tzinfo=timezone.utc)
        events=[dict(at=(t+timedelta(minutes=5)).isoformat(),kind='phase',phase='intake',state='running')]
        cfg={'started_at':t.isoformat()}
        value=clock(cfg,events,now=t+timedelta(minutes=10))
        self.assertEqual('00:10:00',display(value,now=t+timedelta(minutes=10)))
        events.append(dict(at=(t+timedelta(minutes=11)).isoformat(),kind='phase',phase='human_report',state='completed'))
        frozen=clock(cfg,events,now=t+timedelta(hours=1))
        self.assertEqual('00:11:00',display(frozen,now=t+timedelta(hours=2)))
        cfg.update(run_state='cancelled',ended_at=(t+timedelta(minutes=3)).isoformat())
        self.assertEqual('00:03:00',display(clock(cfg,events),now=t+timedelta(hours=2)))
        fallback=clock({},events,now=t+timedelta(hours=1))
        self.assertEqual('first_recorded_event',fallback['source'])
        self.assertEqual('00:06:00',display(fallback))
