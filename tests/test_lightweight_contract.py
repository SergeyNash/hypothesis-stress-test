from pathlib import Path
import re
import subprocess
import unittest

ROOT=Path(__file__).resolve().parents[1]


class LightweightContract(unittest.TestCase):
    def test_runtime_and_static_payload_machinery_are_absent(self):
        # Architecture regression: do not quietly reintroduce a mandatory runtime.
        self.assertEqual({'terminal_progress.py','setup_workspace.py','update_workspace.py','vscode_tasks.py','check_version.py'},{p.name for p in (ROOT/'scripts').glob('*.py')})
        self.assertFalse((ROOT/'prototypes').exists());self.assertFalse((ROOT/'integrations').exists())
        self.assertEqual([],list((ROOT/'templates').rglob('*.json')))
        self.assertEqual([],list((ROOT/'examples').rglob('*.marker')))

    def test_active_instructions_never_call_removed_tools_or_link_deleted_files(self):
        paths=[]
        for area in ['.cline','.clinerules','templates','profiles','layers','playbooks','implementations','architecture']:
            paths.extend((ROOT/area).rglob('*.md'))
        for p in paths:
            text=p.read_text(encoding='utf-8')
            self.assertNotIn('as valid JSON',text,p)
            self.assertNotRegex(text,r'(?mi)^#{1,6} (?:Completion marker|.*— Completion marker)',p)
            calls=re.findall(r'scripts/([a-z_]+\.py)',text)
            for name in calls:self.assertTrue((ROOT/'scripts'/name).is_file(),(p,name))
            for target in re.findall(r'\]\(([^)]+)\)',text):
                if '://' in target or target.startswith('#') or target in {'url','path'} or any(c in target for c in ['<','[']):continue
                self.assertTrue((p.parent/target.split('#')[0]).exists(),(p,target))

    def test_retirement_manifest_does_not_delete_replacements_or_user_runs(self):
        for line in (ROOT/'maintenance/retired-paths.txt').read_text().splitlines():
            self.assertNotIn('..',Path(line).parts)
            self.assertNotIn(Path(line).parts[0],{'runs','.hst','.git'})
            self.assertFalse((ROOT/line).exists(),line)
