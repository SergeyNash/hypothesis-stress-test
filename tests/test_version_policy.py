import sys
from pathlib import Path
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_version import check


class VersionPolicyTests(unittest.TestCase):
    def fixture(self, root, version='2.6.0'):
        (root / 'VERSION').write_text(version + '\n')
        (root / 'README.md').write_text('Версия фреймворка <b>' + version + '</b>')
        (root / '.clinerules').mkdir()
        (root / '.clinerules/00-hypothesis-framework.md').write_text('**Framework version:** ' + version)
        (root / 'CHANGELOG.md').write_text('## [' + version + '] — 2026-11-13\n\nChanges\n')

    def test_next_minor_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            self.assertEqual([], check(root, '2.5.0'))

    def test_unchanged_and_skipped_minor_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            for base in ['2.6.0', '2.4.0']:
                self.assertTrue(check(root, base))

    def test_stale_metadata_and_unreleased_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            (root / 'README.md').write_text('Версия фреймворка <b>2.5.0</b>')
            (root / 'CHANGELOG.md').write_text('## [Unreleased]\nChanges\n')
            self.assertEqual(3, len(check(root, '2.5.0')))

    def test_nonzero_patch_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root, '2.6.1')
            with self.assertRaises(ValueError):
                check(root, '2.5.0')
