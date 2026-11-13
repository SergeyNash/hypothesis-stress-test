import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from update_workspace import update,unpack
from setup_workspace import install


class Updater(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.framework=self.root/'framework renamed'
        (self.framework/'scripts').mkdir(parents=True)
        (self.framework/'scripts/setup_workspace.py').write_text('old setup')
        (self.framework/'scripts/extract_evidence.py').write_text('extract')
        (self.framework/'VERSION').write_text('old')
        (self.framework/'personal.txt').write_text('custom file')
        (self.framework/'runs').mkdir();(self.framework/'runs/private.txt').write_text('nested run')
        (self.root/'runs').mkdir();(self.root/'runs/private.txt').write_text('workspace run')
        (self.root/'.hst').mkdir()
        (self.root/'.hst/workspace.json').write_text(json.dumps({'schema_version':1,'framework_dir':self.framework.name,'terminal_enabled':True}))
        (self.root/'.clinerules').mkdir();(self.root/'.clinerules/personal.md').write_text('personal rule')
        self.zip=self.root/'release.zip'
        self.archive({'VERSION':'new','scripts/setup_workspace.py':'new setup','scripts/extract_evidence.py':'new extract',
                      '.clinerules/framework.md':'framework rule','.cline/skills/test/SKILL.md':'test skill'})
    def tearDown(self):self.tmp.cleanup()
    def archive(self,files):
        with zipfile.ZipFile(self.zip,'w') as z:
            for name,text in files.items():z.writestr('release-root/'+name,text)
    def fetch(self,path):shutil.copyfile(self.zip,path)
    def call(self,**kwargs):return update(self.root,fetch=self.fetch,**kwargs)

    def test_inspection_only_does_not_change_installation(self):
        before=(self.root/'.hst/workspace.json').read_bytes()
        def forbidden(*args):raise AssertionError('setup must not run')
        result=self.call(setup=forbidden)
        self.assertEqual('inspection_only',result['action'])
        self.assertEqual('old',(self.framework/'VERSION').read_text())
        self.assertEqual(before,(self.root/'.hst/workspace.json').read_bytes())
        self.assertFalse((self.root/'.hst/updates').exists())

    def test_update_discovers_renamed_folder_backs_up_and_preserves_runs(self):
        called=[]
        result=self.call(apply=True,setup=lambda *args:called.append(args))
        self.assertEqual('updated',result['action'])
        self.assertTrue(called[0][2])  # terminal preference retained
        self.assertEqual('new',(self.framework/'VERSION').read_text())
        self.assertEqual('custom file',(self.framework/'personal.txt').read_text())
        self.assertEqual('nested run',(self.framework/'runs/private.txt').read_text())
        self.assertEqual('workspace run',(self.root/'runs/private.txt').read_text())
        self.assertEqual('old',(Path(result['backup'])/'framework/VERSION').read_text())
        self.assertFalse((self.root/'.hst/update.lock').exists())

    def test_failed_setup_rolls_back_framework_configs_and_environment(self):
        env=self.root/'.hst/terminal-venv';env.mkdir();(env/'sentinel').write_text('old environment')
        def fail(workspace,framework,terminal):
            (workspace/'.clinerules/personal.md').write_text('damaged by partial install')
            (workspace/'.clinerules/new.md').write_text('new file')
            (workspace/'.hst/terminal-venv/sentinel').write_text('changed')
            raise ValueError('synthetic setup failure')
        with self.assertRaisesRegex(ValueError,'setup failure'):self.call(apply=True,setup=fail)
        self.assertEqual('old',(self.framework/'VERSION').read_text())
        self.assertEqual('personal rule',(self.root/'.clinerules/personal.md').read_text())
        self.assertFalse((self.root/'.clinerules/new.md').exists())
        self.assertEqual('old environment',(env/'sentinel').read_text())
        self.assertFalse((self.root/'.hst/update.lock').exists())

    def test_network_failure_leaves_existing_files_untouched(self):
        def fail(path):raise OSError('synthetic network failure')
        with self.assertRaises(OSError):update(self.root,apply=True,fetch=fail)
        self.assertEqual('old',(self.framework/'VERSION').read_text())
        self.assertFalse((self.root/'.hst/updates').exists())

    def test_traversal_and_remote_user_runs_are_rejected_before_update(self):
        for bad in ['../escape','scripts/../../escape','runs/HYP-private/input.md','Runs/HYP-private/input.md']:
            self.archive({bad:'bad'})
            with self.assertRaises(ValueError):self.call(apply=True)
            self.assertEqual('old',(self.framework/'VERSION').read_text())

    def test_git_checkout_and_workspace_root_are_not_replaced(self):
        (self.framework/'.git').mkdir()
        with self.assertRaisesRegex(ValueError,'Git checkout'):self.call(apply=True)
        with self.assertRaises(ValueError):update(self.root,self.root,apply=True,fetch=self.fetch)

    def test_installation_adds_stable_updater_and_keeps_other_tasks(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace=Path(tmp)
            install(workspace,ROOT,terminal=True)
            self.assertEqual((ROOT/'scripts/update_workspace.py').read_bytes(),(workspace/'.hst/update.py').read_bytes())

    def test_unpack_replace_and_real_setup_subprocess(self):
        self.archive({'VERSION':'new',
            'scripts/setup_workspace.py':(ROOT/'scripts/setup_workspace.py').read_text(),
            'scripts/extract_evidence.py':'extract',
            '.clinerules/framework.md':'new framework rule',
            '.cline/skills/test/SKILL.md':'new test skill'})
        result=self.call(apply=True,terminal=False)
        self.assertEqual('updated',result['action'])
        self.assertEqual('new framework rule',(self.root/'.clinerules/framework.md').read_text())
        self.assertEqual('personal rule',(self.root/'.clinerules/personal.md').read_text())
        self.assertEqual('workspace run',(self.root/'runs/private.txt').read_text())

if __name__=='__main__':unittest.main()
