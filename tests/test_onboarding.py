from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer
import json
import shutil
import sys
import tempfile
import threading
import unittest
import urllib.request
import urllib.error
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from run_progress import init, record, Viewer
from setup_workspace import install, plan


class Onboarding(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_setup_preserves_personal_skills_and_blocks_conflicts_before_writes(self):
        personal = self.root / '.cline/skills/personal/SKILL.md'
        personal.parent.mkdir(parents=True); personal.write_text('personal')
        conflict = self.root / '.clinerules/00-hypothesis-framework.md'
        conflict.parent.mkdir(); conflict.write_text('custom')
        with self.assertRaisesRegex(ValueError, 'conflicts'):
            install(self.root)
        self.assertFalse((self.root / '.cline/skills/hst-start/SKILL.md').exists())
        self.assertEqual('custom', conflict.read_text())
        install(self.root, replace=True)
        self.assertEqual('personal', personal.read_text())
        self.assertTrue(all(x['status'] == 'same' for x in plan(self.root)['files']))

    def test_setup_detects_actual_download_folder(self):
        framework = self.root / 'hypothesis-stress-test-main'
        (framework / '.cline/skills').mkdir(parents=True)
        (framework / '.clinerules').mkdir()
        (framework / 'scripts').mkdir()
        (framework / 'scripts/extract_evidence.py').write_text('')
        install(self.root, framework)
        self.assertIn('`hypothesis-stress-test-main`', (self.root / '.clinerules/05-hst-workspace.md').read_text())

    def test_progress_wait_error_no_results_and_resume_are_distinct(self):
        output = init(self.root)
        record(self.root, phase='local_evidence', state='waiting_user', message='Проверка полноты')
        record(self.root, phase='market', channel='confluence', state='auth_error', message='HTTP 401')
        record(self.root, phase='business_context', channel='internet', state='no_results', message='No relevant results', query='test')
        init(self.root)  # Resume does not discard history or invent source events.
        data = json.loads((output / 'progress.json').read_text())
        self.assertEqual(3, len(data['events']))
        self.assertEqual(0, data['completed'])
        self.assertEqual('waiting_user', next(p for p in data['phases'] if p['id'] == 'local_evidence')['state'])
        self.assertEqual(['auth_error', 'no_results'], [e['state'] for e in data['events'] if e['kind'] == 'source'])
        with self.assertRaisesRegex(ValueError, 'completion verification failed'):
            record(self.root, phase='market', state='completed', message='False completion')

    def test_completion_requires_inventory_review_when_present(self):
        run = self.root / 'run'
        shutil.copytree(ROOT / 'examples/example-005', run)
        inv = run / 'outputs/evidence_inventory.md'
        inv.write_text(inv.read_text() + '\n## Retrieval Review\n- status: pending\n')
        with self.assertRaisesRegex(ValueError, 'INCOMPLETE_RETRIEVAL_REVIEW'):
            record(run, phase='local_evidence', state='completed', message='not yet')
        inv.write_text(inv.read_text().replace('status: pending', 'status: accepted'))
        record(run, phase='local_evidence', state='completed', message='Reviewed')

    def test_live_server_reads_updates_and_rejects_outside_symlink(self):
        run = self.root / 'run'; run.mkdir()
        output = init(run)
        russian = 'Внешнее исследование → 1 500 ₽'
        artifacts = {
            'external_research.md': '# ' + russian,
            'evidence_inventory.md': russian,
            'notes.txt': russian,
            'sample.jsonl': json.dumps({'message': russian}, ensure_ascii=False) + '\n',
        }
        for name, text in artifacts.items():
            (output / name).write_text(text, encoding='utf-8')
        secret = self.root / 'outside.txt'; secret.write_text('outside')
        (run / 'escape.txt').symlink_to(secret)
        server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Viewer, directory=str(run)))
        thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
        url = f'http://127.0.0.1:{server.server_port}'
        try:
            with urllib.request.urlopen(url + '/') as response:
                self.assertEqual(url + '/outputs/progress.html', response.url)
                snapshot_url = urljoin(response.url, 'progress.json')
                artifact_base = response.url
                self.assertIn('Ход проверки', response.read().decode())
                self.assertEqual('utf-8', response.headers.get_content_charset())
            for name, text in artifacts.items():
                target = urljoin(artifact_base, name)
                with urllib.request.urlopen(target) as response:
                    self.assertEqual('text/plain', response.headers.get_content_type())
                    self.assertEqual('utf-8', response.headers.get_content_charset())
                    payload = response.read()
                    self.assertEqual(text.encode('utf-8'), payload)
                    self.assertEqual(text, payload.decode(response.headers.get_content_charset()))
                with urllib.request.urlopen(urllib.request.Request(target, method='HEAD')) as response:
                    self.assertEqual('utf-8', response.headers.get_content_charset())
            record(run, phase='business_context', state='running', message='Исследование')
            with urllib.request.urlopen(snapshot_url) as response:
                self.assertEqual('utf-8', response.headers.get_content_charset())
                self.assertEqual(1, len(json.load(response)['events']))
            for method in ['GET', 'HEAD']:
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    urllib.request.urlopen(urllib.request.Request(url + '/escape.txt', method=method))
                self.assertEqual(404, caught.exception.code)
        finally:
            server.shutdown(); server.server_close(); thread.join()


if __name__ == '__main__':
    unittest.main()
