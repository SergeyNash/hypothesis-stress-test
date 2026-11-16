"""Verify upgrade data preservation and rollback, without network/dependency installs."""
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import setup_workspace as setup
import update_workspace as updater
import vscode_tasks


class Maintenance(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.workspace=Path(self.tmp.name)/'DataB';self.workspace.mkdir()

    def write(self,name,text):
        target=self.workspace/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding='utf-8');return target

    def local_framework(self):
        # Match the supported installation: framework nested inside DataB. The
        # Windows runner puts the checkout on D: and temp files on C:.
        framework=self.workspace/'framework';framework.mkdir()
        for name in ['.cline','.clinerules','scripts','maintenance']:
            shutil.copytree(ROOT/name,framework/name,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        shutil.copy2(ROOT/'VERSION',framework/'VERSION')
        return framework

    def test_install_migrates_old_state_with_backup_and_preserves_user_files(self):
        framework=self.local_framework()
        self.write('.hst/workspace.json',json.dumps({'framework_dir':'framework','terminal_enabled':True}))
        self.write('.hst/tui.json','old TUI')
        self.write('.clinerules/55-tui-control.md','old rule')
        custom=self.write('.clinerules/personal.md','my rule')
        run=self.write('runs/HYP-2026-11-14-001/outputs/quality_review.json','historic run')
        tasks=self.write('.vscode/tasks.json','{// user comment\n"version":"2.0.0","tasks":[{"label":"Custom","command":"echo hi"}]}')
        setup.plan(self.workspace,framework,terminal=True)
        self.assertTrue((self.workspace/'.hst/tui.json').exists())
        result=setup.install(self.workspace,framework,replace=True,terminal=True)
        self.assertFalse((self.workspace/'.hst/workspace.json').exists())
        self.assertFalse((self.workspace/'.hst/tui.json').exists())
        self.assertFalse((self.workspace/'.clinerules/55-tui-control.md').exists())
        self.assertEqual('my rule',custom.read_text());self.assertEqual('historic run',run.read_text())
        self.assertEqual('old TUI',(Path(result['backup'])/'.hst/tui.json').read_text())
        self.assertTrue(setup.settings(self.workspace)['terminal_enabled'])
        self.assertIn('// user comment',tasks.read_text())
        parsed,_=vscode_tasks.parse(tasks.read_text());self.assertEqual('Custom',parsed['tasks'][0]['label'])
        self.assertEqual('folderOpen',parsed['tasks'][1]['runOptions']['runOn'])

    def test_install_failure_restores_original_files(self):
        framework=self.local_framework()
        self.write('.clinerules/00-hypothesis-framework.md','my old rules')
        state=self.write('.hst/tui.json','old state')
        original=shutil.copyfile
        def fail(source,target,*args,**kwargs):
            if Path(target)==self.workspace/'.hst/update.py':raise OSError('injected write failure')
            return original(source,target,*args,**kwargs)
        with patch.object(setup.shutil,'copyfile',side_effect=fail):
            with self.assertRaises(OSError):setup.install(self.workspace,framework,replace=True)
        self.assertEqual('my old rules',(self.workspace/'.clinerules/00-hypothesis-framework.md').read_text())
        self.assertEqual('old state',state.read_text())
        self.assertFalse((self.workspace/'.hst/workspace.md').exists())

    def fixture(self):
        framework=self.workspace/'framework'
        self.write('framework/VERSION','2.10.0')
        self.write('framework/scripts/setup_workspace.py','# old setup')
        self.write('framework/scripts/source_snapshot.py','# obsolete')
        self.write('framework/custom.md','custom')
        self.write('framework/runs/local/result.md','nested result')
        self.write('runs/HYP-2026-11-14-001/result.md','user result')
        self.write('.hst/workspace.json',json.dumps({'framework_dir':'framework'}))
        def fetch(target):
            with zipfile.ZipFile(target,'w') as archive:
                for name,text in {'VERSION':'2.11.0','scripts/setup_workspace.py':'# new setup','.cline/skills/hst-start/SKILL.md':'new skill','.clinerules/core.md':'new rules','maintenance/retired-paths.txt':'scripts/source_snapshot.py\n'}.items():archive.writestr('package/'+name,text)
        return framework,fetch

    def test_update_removes_only_retired_paths_and_backs_up_previous_framework(self):
        framework,fetch=self.fixture()
        report=updater.update(self.workspace,framework,apply=True,fetch=fetch,setup=lambda *args:None)
        self.assertFalse((framework/'scripts/source_snapshot.py').exists())
        self.assertEqual('custom',(framework/'custom.md').read_text())
        self.assertEqual('nested result',(framework/'runs/local/result.md').read_text())
        self.assertEqual('user result',(self.workspace/'runs/HYP-2026-11-14-001/result.md').read_text())
        self.assertEqual('2.10.0',(Path(report['backup'])/'framework/VERSION').read_text())

    def test_failed_update_rolls_back_framework_and_adapter(self):
        framework,fetch=self.fixture()
        self.write('.clinerules/personal.md','original')
        def fail(*args):
            self.write('.clinerules/personal.md','changed')
            self.write('.hst/workspace.md','changed')
            raise OSError('injected setup failure')
        with self.assertRaises(OSError):updater.update(self.workspace,framework,apply=True,fetch=fetch,setup=fail)
        self.assertEqual('2.10.0',(framework/'VERSION').read_text())
        self.assertTrue((framework/'scripts/source_snapshot.py').exists())
        self.assertEqual('original',(self.workspace/'.clinerules/personal.md').read_text())
        self.assertFalse((self.workspace/'.hst/workspace.md').exists())
        self.assertFalse((self.workspace/'.hst/update.lock').exists())

    def test_update_inspection_does_not_modify_installation(self):
        framework,fetch=self.fixture()
        report=updater.update(self.workspace,framework,fetch=fetch)
        self.assertEqual('inspection_only',report['action'])
        self.assertEqual('2.10.0',(framework/'VERSION').read_text())
        self.assertFalse((self.workspace/'.hst/updates').exists())

    def test_release_archive_installs_real_adapter_without_extractors_or_json_state(self):
        framework,_=self.fixture()
        self.write('.hst/tui.json','obsolete')
        self.write('.clinerules/55-tui-control.md','obsolete copied rule')
        def fetch(target):
            with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as archive:
                for root in ['.cline','.clinerules','scripts','maintenance']:
                    for source in (ROOT/root).rglob('*'):
                        if source.is_file() and '__pycache__' not in source.parts:
                            archive.write(source,'package/'+source.relative_to(ROOT).as_posix())
                archive.write(ROOT/'VERSION','package/VERSION')
        updater.update(self.workspace,framework,apply=True,terminal=False,fetch=fetch)
        self.assertEqual((ROOT/'VERSION').read_text().strip(),(framework/'VERSION').read_text().strip())
        self.assertFalse((framework/'scripts/source_snapshot.py').exists())
        self.assertFalse((self.workspace/'.hst/tui.json').exists())
        self.assertFalse((self.workspace/'.clinerules/55-tui-control.md').exists())
        self.assertFalse((self.workspace/'.hst/workspace.json').exists())
        self.assertEqual('framework',setup.settings(self.workspace)['framework_dir'])
        self.assertEqual('user result',(self.workspace/'runs/HYP-2026-11-14-001/result.md').read_text())

    def test_untrusted_archive_cannot_escape_destination(self):
        archive=Path(self.tmp.name)/'unsafe.zip'
        with zipfile.ZipFile(archive,'w') as z:z.writestr('package/../../escape','bad')
        with self.assertRaises(ValueError):updater.unpack(archive,Path(self.tmp.name)/'unpacked')
