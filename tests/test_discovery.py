from pathlib import Path
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from discover_sources import discover


class Discovery(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def file(self, name, content='data'):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding='utf-8')
        return p

    @unittest.skipUnless(importlib.util.find_spec('docx') and importlib.util.find_spec('openpyxl'), 'optional document readers missing')
    def test_topic_office_documents_survive_small_extraction_cap(self):
        # Real ZIP-based documents in a generic parent folder, beyond many root notes.
        from docx import Document
        from openpyxl import Workbook
        for n in range(205):
            self.file(f'notes/{n:03}.md', 'unrelated')
        folder = self.root / 'Развитие направления/Гипотезы роста/Поддержка ИИ'
        folder.mkdir(parents=True)
        doc = Document(); doc.add_paragraph('Synthetic support observation')
        doc.save(folder / 'Рынок.docx')
        book = Workbook(); book.active['A1'] = 123
        book.save(folder / 'Тендеры.xlsx'); book.close()
        out = json.loads(subprocess.check_output([
            sys.executable, str(ROOT / 'scripts/extract_evidence.py'),
            '--root', str(self.root), '--query', 'ИИ', '--max-files', '2']))
        self.assertEqual({'.docx', '.xlsx'}, {Path(x['source_path']).suffix for x in out['files']})
        self.assertTrue(all(x['status'] == 'extracted' for x in out['files']))
        self.assertTrue(out['limit_reached'])
        self.assertFalse(out['discovery']['limit_reached'])

    def test_renamed_framework_and_symlinks_are_excluded(self):
        self.file('framework-renamed/.cline/skills/local-knowledge-retrieval/SKILL.md')
        self.file('framework-renamed/scripts/extract_evidence.py')
        self.file('framework-renamed/false.md')
        self.file('runs/old/outputs/false.md')
        self.file('real.md')
        (self.root / 'link').symlink_to(self.root, target_is_directory=True)
        result = discover(self.root)
        self.assertEqual(['real.md'], [x['path'] for x in result['files']])
        reasons = {x['reason'] for x in result['excluded']}
        self.assertIn('framework_directory', reasons)
        self.assertIn('symlink', reasons)

    def test_metadata_limit_and_unsupported_formats_are_visible(self):
        self.file('a.pptx'); self.file('b.md'); self.file('c.md')
        result = discover(self.root, max_entries=2)
        self.assertTrue(result['limit_reached'])
        self.assertEqual(2, result['entries_seen'])
        self.assertEqual('unsupported', result['files'][0]['reader'])

    def test_depth_limit_is_not_reported_as_empty_coverage(self):
        self.file('one/two/three.md')
        result = discover(self.root, max_depth=1)
        self.assertTrue(result['limit_reached'])
        self.assertEqual('depth_limit', result['excluded'][0]['reason'])

    def test_generic_growth_directory_is_prioritized_without_query(self):
        self.file('aaa.md'); self.file('Проекты/Идеи развития/test.md')
        result = discover(self.root)
        self.assertEqual('Проекты/Идеи развития/test.md', result['files'][0]['path'])

    def test_short_ai_term_does_not_match_inside_unrelated_words(self):
        self.file('стратегии.md'); self.file('AI_контур/ИИ.md')
        result = discover(self.root, 'ИИ AI')
        self.assertEqual(['ai', 'ии'], result['files'][0]['topic_matches'])
        self.assertEqual([], result['files'][1]['topic_matches'])


if __name__ == '__main__':
    unittest.main()
