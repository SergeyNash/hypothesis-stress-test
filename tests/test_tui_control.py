import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import tui_control as control
from source_selection import require
from run_control import load_config
from run_progress import events
from install_tui import package


class TUIControlTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        (self.root / '.hst').mkdir()
        self.heartbeat()
        (self.root / 'materials').mkdir()
        self.payload = {'statement': 'Если добавить ежемесячный разбор повторных запросов к сопровождению, заказчики смогут выявлять причины инцидентов и согласовывать превентивные работы.',
                        'profile': 'digital_product', 'hypothesis_type': '', 'domain': 'Сопровождение системного ПО',
                        'audience': 'Заказчики сопровождения', 'scenario': 'Регулярные повторные запросы', 'roles': 'CIO; Инженер заказчика',
                        'channels': {'local': True, 'confluence': False, 'internet': False}, 'local_paths': ['materials']}

    def tearDown(self): self.tmp.cleanup()

    def heartbeat(self, **extra):
        value = {'schema_version': 1, 'at': control.now(), 'workspace': str(self.root.resolve()), 'ready': True} | extra
        (self.root / '.hst/tui-bridge.json').write_text(json.dumps(value))

    def prepare(self):
        item = control.submit(self.root, self.payload)
        with patch('run_control.viewer', return_value='http://127.0.0.1:8787/outputs/progress.html'):
            value = control.bootstrap(self.root, item['request_id'])
        return item['request_id'], self.root / value['run_dir']

    def accept(self):
        request, run = self.prepare()
        control.change(self.root, request, 'dispatching')
        control.acknowledge(self.root, request)
        return request, run

    def test_form_does_not_create_run_before_submit_and_bridge(self):
        self.assertFalse((self.root / 'runs').exists())
        item = control.submit(self.root, self.payload)
        self.assertEqual('queued', item['state'])
        self.assertFalse((self.root / 'runs').exists())
        self.assertEqual(self.payload, control.read(self.root / '.hst/requests' / item['request_id'] / 'request.json')['config'])

    def test_unavailable_or_stale_bridge_blocks_submission(self):
        for extra in [{'ready': False}, {'at': '2000-01-01T00:00:00+00:00'}]:
            self.heartbeat(**extra)
            with self.assertRaises(ValueError): control.submit(self.root, self.payload)
        self.assertFalse((self.root / 'runs').exists())

    def test_bootstrap_applies_exact_sources_but_does_not_fake_executor_ack(self):
        request, run = self.prepare()
        cfg = load_config(run)
        self.assertTrue(cfg['tui_request_pending'])
        self.assertEqual(self.payload['channels'], cfg['source_selection']['channels'])
        self.assertEqual(['materials'], cfg['source_selection']['local_paths'])
        self.assertEqual('prepared', control.status(self.root, request)['state'])
        with self.assertRaises(ValueError): require(run, 'local')
        self.assertFalse(any(e['phase'] == 'facilitator' for e in events(run / 'outputs')))
        control.change(self.root, request, 'dispatching')
        control.acknowledge(self.root, request)
        control.change(self.root, request, 'dispatched')
        self.assertEqual('accepted', control.status(self.root, request)['state'])
        require(run, 'local', self.root / 'materials')
        with self.assertRaises(ValueError): require(run, 'internet')

    def test_same_submit_and_bootstrap_cannot_duplicate_run(self):
        request, run = self.prepare()
        control.bootstrap(self.root, request)
        with self.assertRaises(ValueError): control.submit(self.root, self.payload)
        self.assertEqual([run], list((self.root / 'runs').iterdir()))

    def test_existing_folder_never_reused(self):
        import datetime
        date = datetime.datetime.now().astimezone().strftime('%Y-%m-%d')
        old = self.root / 'runs' / ('HYP-' + date + '-001')
        old.mkdir(parents=True); (old / 'keep').write_text('unchanged')
        _, run = self.prepare()
        self.assertNotEqual(old, run)
        self.assertEqual('unchanged', (old / 'keep').read_text(encoding='utf-8'))

    def test_changed_request_is_not_acknowledged(self):
        request, _ = self.prepare()
        control.change(self.root, request, 'dispatching')
        path = self.root / '.hst/requests' / request / 'request.json'
        value = control.read(path); value['config']['channels']['internet'] = True
        path.write_text(json.dumps(value))
        with self.assertRaises(ValueError): control.acknowledge(self.root, request)

    def test_question_round_trip_preserves_choice_and_rejects_stale_answers(self):
        request, run = self.accept()
        q = control.question(self.root, request, 'Глубина анализа?', ['Быстро', 'Подробно', 'Пропустить'], 'validation')
        with self.assertRaises(ValueError): control.answer(self.root, request, '0' * 32, 'Быстро')
        with self.assertRaises(ValueError): control.answer(self.root, request, q['id'], 'anything')
        control.answer(self.root, request, q['id'], 'Подробно')
        control.question_sent(self.root, request, q['id'])
        item = control.answer(self.root, request, q['id'], '', consume=True)
        self.assertEqual('Подробно', item['response'])
        self.assertEqual('consumed', item['state'])
        with self.assertRaises(ValueError): control.answer(self.root, request, q['id'], '', consume=True)

    def test_question_without_executor_ack_is_rejected(self):
        request, _ = self.prepare()
        with self.assertRaises(ValueError): control.question(self.root, request, 'Question?', [], 'intake')

    def test_invalid_scope_and_empty_fields_do_not_create_request(self):
        for extra in [{'local_paths': ['../']}, {'statement': ''}, {'channels': {'local': True}}]:
            with self.assertRaises(ValueError): control.submit(self.root, self.payload | extra)
        self.assertEqual([], list((self.root / '.hst/requests').iterdir()))

    def test_service_gaps_are_explicit_and_no_fake_customer_fact(self):
        self.payload.update(profile='service_business', hypothesis_type='service_improvement')
        _, run = self.prepare()
        text = (run / 'input/hypothesis.md').read_text(encoding='utf-8')
        self.assertIn('Не задан', text)
        self.assertIn('требуют уточнения', text)

    def test_vsix_has_real_api_dependency_and_current_version(self):
        target = package(self.root / 'bridge.vsix')
        with zipfile.ZipFile(target) as z:
            info = json.loads(z.read('extension/package.json'))
            self.assertEqual((ROOT / 'VERSION').read_text(encoding='utf-8').strip(), info['version'])
            self.assertEqual(['saoudrizwan.claude-dev'], info['extensionDependencies'])
            self.assertIn('extension/protocol.js', z.namelist())

    @unittest.skipUnless(__import__('shutil').which('node'), 'Node is optional locally; required in TUI CI')
    def test_bridge_real_backend_round_trip(self):
        import subprocess
        request, run = self.prepare()
        output = subprocess.check_output(['node', str(ROOT / 'integrations/vscode-bridge/e2e.test-helper.js'), str(self.root), str(ROOT), sys.executable, request], encoding='utf-8')
        result = json.loads(output)
        self.assertEqual({'started': 1, 'sent': 1, 'response': 'Продолжить', 'state': 'accepted'}, result)
        self.assertEqual(self.payload['channels'], load_config(run)['source_selection']['channels'])
        self.assertFalse(load_config(run)['tui_request_pending'])

    def test_pending_question_blocks_final_audit_and_archive_is_self_contained(self):
        from shutil import copytree
        request, run = self.accept()
        q = control.question(self.root, request, 'Подтвердить?', ['Да'], 'validation')
        self.assertIn('PENDING_TUI_QUESTION', control.validate_run_binding(run))
        control.answer(self.root, request, q['id'], 'Да')
        control.answer(self.root, request, q['id'], '', consume=True)
        self.assertEqual([], control.validate_run_binding(run))
        archive = self.root / 'archive' / run.name
        copytree(run, archive)
        self.assertEqual([], control.validate_run_binding(archive))

    def test_ack_checks_applied_sources_not_just_request_hash(self):
        request, run = self.prepare()
        control.change(self.root, request, 'dispatching')
        config = load_config(run)
        config['source_selection']['channels']['internet'] = True
        (run / 'run_config.json').write_text(json.dumps(config))
        with self.assertRaises(ValueError): control.acknowledge(self.root, request)

    def test_canonical_scope_and_lost_connection_do_not_fake_execution_failure(self):
        self.payload['local_paths'] = ['./materials']
        request, run = self.prepare()
        control.change(self.root, request, 'dispatching')
        control.acknowledge(self.root, request)
        self.assertEqual(['materials'], load_config(run)['source_selection']['local_paths'])
        self.heartbeat(at='2000-01-01T00:00:00+00:00')
        value = control.status(self.root, request)
        self.assertEqual('accepted', value['state'])
        self.assertIn('Нет связи', value['connection'])
