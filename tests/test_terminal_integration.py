import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from active_run import Follow, publish, resolve
from setup_workspace import install, plan
from vscode_tasks import merge, parse, task, LABEL
import run_control


class TerminalIntegration(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def run_dir(self,name):
        run=self.root/'runs'/name
        shutil.copytree(ROOT/'examples/example-005',run)
        data={'run':name,'events':[],'phases':[{'id':'intake','name':'Подготовка','state':'running'}]}
        (run/'outputs/progress.json').write_text(json.dumps(data),encoding='utf-8')
        return run
    def reader(self,path):return json.loads(path.read_text())

    def test_waits_before_new_run_without_creating_files(self):
        state,note,run=Follow(self.root).poll(self.reader)
        self.assertIsNone(state);self.assertIsNone(run)
        self.assertIn('Ожидаю',note);self.assertEqual([],list(self.root.iterdir()))

    def test_follows_two_explicit_new_runs_and_retains_completed_one_until_next(self):
        first=self.run_dir('HYP-2026-11-09-001');second=self.run_dir('HYP-2026-11-09-002')
        watcher=Follow(self.root)
        # A newer folder alone must not switch or choose a run.
        self.assertIsNone(watcher.poll(self.reader)[0])
        publish(first);self.assertEqual(first.name,watcher.poll(self.reader)[0]['run'])
        self.assertEqual(first.name,watcher.poll(self.reader)[0]['run'])
        publish(second);self.assertEqual(second.name,watcher.poll(self.reader)[0]['run'])

    def test_new_activation_clears_old_view_before_missing_journal(self):
        first=self.run_dir('HYP-2026-11-09-001');second=self.run_dir('HYP-2026-11-09-002')
        watcher=Follow(self.root);publish(first);watcher.poll(self.reader)
        (second/'outputs/progress.json').unlink();publish(second)
        state,note,run=watcher.poll(self.reader)
        self.assertIsNone(state);self.assertEqual(second,run);self.assertIn('нового',note)
        (second/'outputs/progress.json').write_text(json.dumps({'run':second.name}))
        self.assertEqual(second.name,watcher.poll(self.reader)[0]['run'])

    def test_partial_json_keeps_last_data_only_for_same_run(self):
        run=self.run_dir('HYP-2026-11-09-001');publish(run);watcher=Follow(self.root)
        before=watcher.poll(self.reader)[0];(run/'outputs/progress.json').write_text('{')
        state,note,_=watcher.poll(self.reader)
        self.assertEqual(before,state);self.assertIn('недоступен',note)

    def test_mismatched_run_id_is_not_displayed(self):
        run=self.run_dir('HYP-2026-11-09-001');publish(run)
        (run/'outputs/progress.json').write_text(json.dumps({'run':'wrong'}))
        self.assertIsNone(Follow(self.root).poll(self.reader)[0])

    def test_deleted_pointer_clears_old_state(self):
        run=self.run_dir('HYP-2026-11-09-001');publish(run);watcher=Follow(self.root);watcher.poll(self.reader)
        (self.root/'.hst/active-run.json').unlink()
        self.assertIsNone(watcher.poll(self.reader)[0])

    def test_external_and_symlink_pointer_is_rejected(self):
        run=self.run_dir('HYP-2026-11-09-001');publish(run)
        pointer=self.root/'.hst/active-run.json';d=json.loads(pointer.read_text());d['run_dir']='../../outside';pointer.write_text(json.dumps(d))
        with self.assertRaises(ValueError):resolve(self.root)
        pointer.unlink();outside=self.root/'outside.json';outside.write_text('{}');pointer.symlink_to(outside)
        with self.assertRaises(ValueError):resolve(self.root)

    def test_custom_layout_requires_explicit_workspace(self):
        run=self.root/'custom'/'HYP-2026-11-09-001';(run/'input').mkdir(parents=True);(run/'input/hypothesis.md').write_text('input')
        self.assertIsNone(publish(run))
        publish(run,self.root);self.assertEqual(run,resolve(self.root)[0])

    def test_prepare_publishes_even_when_http_server_fails(self):
        run=self.root/'runs'/'HYP-2026-11-09-001';(run/'input').mkdir(parents=True)
        shutil.copyfile(ROOT/'examples/example-005/input/hypothesis.md',run/'input/hypothesis.md')
        with patch.object(run_control,'viewer',side_effect=ValueError('host server failure')):
            with self.assertRaises(ValueError):run_control.prepare(run,'full')
        self.assertEqual(run,resolve(self.root)[0])
        self.assertTrue((run/'outputs/progress.json').exists())

    def test_jsonc_user_tasks_comments_inputs_and_shell_arguments_preserved(self):
        source='''{ // user header
  "version": "2.0.0",
  "tasks": [
    // keep this task and its exact bytes
    {"label": "build", "command": "echo /* not a comment */ // literal",},
  ],
  "inputs": [{"id":"custom","type":"promptString","description":"pick"}],
}'''
        desired=task(self.root,ROOT)
        output,owned_changed=merge(source,desired)
        self.assertFalse(owned_changed);self.assertIn('// keep this task and its exact bytes',output)
        self.assertIn('{"label": "build", "command": "echo /* not a comment */ // literal",}',output)
        parsed,_=parse(output)
        self.assertEqual(2,len(parsed['tasks']));self.assertEqual('custom',parsed['inputs'][0]['id'])
        again,_=merge(output,desired);self.assertEqual(output,again)

    def test_jsonc_existing_managed_task_needs_replace_and_preserves_other_bytes(self):
        desired=task(self.root,ROOT);old=dict(desired,presentation={'reveal':'never'})
        source=json.dumps({'version':'2.0.0','tasks':[{'label':'personal','command':'echo test'},old]})
        self.assertEqual((source,True),merge(source,desired))
        out,changed=merge(source,desired,replace=True)
        self.assertTrue(changed);self.assertIn('"label": "personal", "command": "echo test"',out)
        parsed,_=parse(out);self.assertEqual(desired,parsed['tasks'][1])

    def test_missing_tasks_array_is_added_without_rewriting_other_configuration(self):
        source='{ /* my settings */ "version":"2.0.0", "inputs": [], }'
        out,_=merge(source,task(self.root,ROOT))
        self.assertTrue(out.startswith('{ /* my settings */ "version":"2.0.0", "inputs": [], '))
        self.assertEqual(LABEL,parse(out)[0]['tasks'][0]['label'])

    def test_invalid_jsonc_and_duplicate_owned_tasks_fail_before_install_writes(self):
        vscode=self.root/'.vscode';vscode.mkdir();p=vscode/'tasks.json';p.write_text('{ broken')
        with self.assertRaises(ValueError):install(self.root,terminal=True,replace=True)
        self.assertFalse((self.root/'.cline').exists());self.assertEqual('{ broken',p.read_text())
        with self.assertRaises(ValueError):merge(json.dumps({'tasks':[{'label':LABEL},{'label':LABEL}]}),task(self.root,ROOT))

    def test_duplicate_jsonc_keys_are_not_silently_reinterpreted(self):
        with self.assertRaises(ValueError):merge('{"tasks": [], "tasks": []}',task(self.root,ROOT))

    def test_terminal_install_handles_nested_zip_path_and_preserves_personal_tasks(self):
        framework=self.root/'Framework renamed folder'
        for name in ['scripts',' .cline'.strip(),'.clinerules']: (framework/name).mkdir(parents=True,exist_ok=True)
        (framework/'scripts/extract_evidence.py').write_text('')
        (framework/'scripts/terminal_progress.py').write_text('')
        (self.root/'.vscode').mkdir();p=self.root/'.vscode/tasks.json';p.write_text('{"tasks":[{"label":"personal","command":"echo untouched"}]}')
        install(self.root,framework,terminal=True)
        data=parse(p.read_text())[0];managed=data['tasks'][1]
        self.assertEqual(str(framework/'scripts/terminal_progress.py'),managed['args'][0])
        self.assertEqual('process',managed['type']);self.assertEqual('dedicated',managed['presentation']['panel'])
        self.assertEqual('folderOpen',managed['runOptions']['runOn']);self.assertEqual(1,managed['runOptions']['instanceLimit'])
        self.assertTrue(all(x['status']=='same' for x in plan(self.root,framework,terminal=True)['files']))
        self.assertEqual('personal',data['tasks'][0]['label'])

    def test_basic_install_does_not_create_optional_terminal_configuration(self):
        install(self.root)
        self.assertFalse((self.root/'.vscode/tasks.json').exists())
        self.assertFalse((self.root/'.hst').exists())


@unittest.skipUnless(importlib.util.find_spec('rich') and importlib.util.find_spec('click'),'optional terminal dependencies missing')
class TerminalRendering(unittest.TestCase):
    def test_finished_view_has_actual_result_and_report_link_without_waiting_copy(self):
        import io
        from rich.console import Console
        from terminal_progress import event_state,render,PHASES
        events=[dict(kind='phase',phase=p,state='completed',at='2026-11-13T07:43:18Z',message='Done') for p,_ in PHASES]
        state=dict(event_state(events),validation={'status':'PASS'},human_report_available=True,
                   html_url='http://127.0.0.1:53169/outputs/progress.html')
        for height in [18,44]:
            console=Console(width=120,file=io.StringIO(),record=True)
            console.print(render(state,width=120,height=height))
            output=console.export_text()
            self.assertIn('проверка PASS',output)
            self.assertIn('http://127.0.0.1:53169/outputs/human_report.html',output)
            self.assertNotIn('Ожидаю данные журнала',output)
            self.assertNotIn('Пайплайн продолжит работу',output)

    def test_source_links_target_channel_history_and_stages_follow_pipeline_order(self):
        import io
        from rich.console import Console
        from terminal_progress import event_state,render
        state=event_state([])
        state['html_url']='http://127.0.0.1:61049/outputs/progress.html'
        console=Console(width=120,file=io.StringIO(),record=True)
        content=render(state,width=120,height=44)
        segments=list(console.render(content))
        links={s.style.link for s in segments if s.style and s.style.link}
        self.assertTrue(all(state['html_url']+'#source-'+key in links for key in ['local','confluence','internet']))
        console.print(content)
        output=console.export_text()
        self.assertIn('01  Подготовка гипотезы',output)
        self.assertIn('10  Итоговый отчёт',output)
        self.assertIn('Этапы · по порядку',output)

    def test_full_width_journal_wraps_message_and_fits_window(self):
        import io
        from rich.console import Console
        from terminal_progress import event_state,render
        message='Разобраны документы по гипотезе; '+('подробности анализа ' * 7)+'КОНЕЦ СООБЩЕНИЯ'
        event={'id':1,'kind':'phase','phase':'business_context','state':'running','at':'2026-11-12T10:00:00Z','message':message}
        state=event_state([event])
        state['updated_at']=None
        console=Console(width=110,file=io.StringIO(),record=True)
        console.print(render(state,width=110,height=38))
        output=console.export_text()
        journal=output.split('Журнал · новые сверху',1)[1]
        self.assertIn('КОНЕЦ СООБЩЕНИЯ',journal)
        self.assertIn('Этапы · по порядку',journal)
        self.assertLessEqual(len(output.splitlines()),38)

    def test_html_address_uses_only_current_run_published_loopback_port(self):
        from terminal_progress import html_address
        with tempfile.TemporaryDirectory() as tmp:
            run=Path(tmp);(run/'outputs').mkdir()
            state=run/'outputs/.viewer-state.json'
            self.assertIsNone(html_address(run))
            for value in ['https://example.com/','http://127.0.0.1:0/','http://127.0.0.1:65536/','http://127.0.0.1:80/\x1b[31m',None]:
                state.write_text(json.dumps({'viewer_url':value}))
                self.assertIsNone(html_address(run))
            state.write_text('{')
            self.assertIsNone(html_address(run))
            state.write_text(json.dumps({'viewer_url':'http://127.0.0.1:61049/'}))
            self.assertEqual('http://127.0.0.1:61049/outputs/progress.html',html_address(run))

    def test_link_and_poll_time_visible_in_full_and_compact_layout(self):
        from rich.console import Console
        from terminal_progress import event_state,render
        state=dict(event_state([]),html_url='http://127.0.0.1:61049/outputs/progress.html',checked_at='2026-11-12T10:00:00Z')
        for height in [18,38]:
            console=Console(width=110,record=True)
            console.print(render(state,width=110,height=height))
            output=console.export_text()
            self.assertIn(state['html_url'],output)
            self.assertIn('13:00:00 МСК',output)

    def test_empty_workspace_and_small_terminal(self):
        from click.testing import CliRunner
        import terminal_progress as ui
        with tempfile.TemporaryDirectory() as tmp:
            result=CliRunner().invoke(ui.main,['--workspace',tmp,'--once','--width','80'])
            self.assertEqual(0,result.exit_code,result.output)
            self.assertIn('Ожидаю запуска гипотезы',result.output)
            self.assertNotIn('DEMO',result.output)

    def test_workspace_and_demo_are_mutually_exclusive(self):
        from click.testing import CliRunner
        import terminal_progress as ui
        with tempfile.TemporaryDirectory() as tmp:
            result=CliRunner().invoke(ui.main,['--workspace',tmp,'--demo','--once'])
            self.assertNotEqual(0,result.exit_code)

    def test_controls_are_data_and_not_terminal_instructions(self):
        from terminal_progress import safe
        self.assertNotIn('\x1b',safe('\x1b[31mtext\x1b[0m'))


if __name__=='__main__':unittest.main()

@unittest.skipUnless(importlib.util.find_spec('rich') and importlib.util.find_spec('click') and sys.platform!='win32','live PTY smoke requires Unix and optional terminal dependencies')
class TerminalLiveProcess(unittest.TestCase):
    def test_wait_then_follow_two_runs_in_one_terminal_and_restore_screen(self):
        import fcntl,os,pty,select,signal,struct,subprocess,termios,time
        from run_progress import init, record
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);master,slave=pty.openpty()
            fcntl.ioctl(slave,termios.TIOCSWINSZ,struct.pack('HHHH',36,120,0,0))
            child=subprocess.Popen([sys.executable,str(ROOT/'scripts/terminal_progress.py'),'--workspace',str(root)],
                stdin=slave,stdout=slave,stderr=slave,env=dict(os.environ,TERM='xterm-256color'))
            os.close(slave);output=b''
            def wait_for(text):
                nonlocal output
                deadline=time.monotonic()+6
                needle=text.encode('utf-8')
                while time.monotonic()<deadline:
                    if select.select([master],[],[],.1)[0]:
                        output+=os.read(master,65536)
                    if needle in output:return
                    if child.poll() is not None:break
                self.fail('Terminal did not show '+text)
            try:
                wait_for('Ожидаю запуска гипотезы')
                for serial in ['001','002']:
                    name='HYP-2026-11-09-'+serial;run=root/'runs'/name
                    (run/'input').mkdir(parents=True)
                    (run/'input/hypothesis.md').write_text('synthetic input')
                    init(run);record(run,phase='local_evidence',state='waiting_user',message='Выберите глубину анализа '+serial)
                    publish(run)
                    wait_for(name);wait_for('Выберите глубину анализа '+serial)
                    # URL publication/port changes must appear without a new progress event.
                    port='61049' if serial=='001' else '61050'
                    (run/'outputs/.viewer-state.json').write_text(json.dumps({'viewer_url':'http://127.0.0.1:'+port+'/'}))
                    wait_for('http://127.0.0.1:'+port+'/outputs/progress.html')
                child.send_signal(signal.SIGINT);child.wait(timeout=5)
                while select.select([master],[],[],.1)[0]:
                    try:output+=os.read(master,65536)
                    except OSError:break
                self.assertEqual(0,child.returncode)
                self.assertIn(b'\x1b[?1049h',output);self.assertIn(b'\x1b[?1049l',output)
            finally:
                if child.poll() is None:child.terminate();child.wait(timeout=5)
                os.close(master)
