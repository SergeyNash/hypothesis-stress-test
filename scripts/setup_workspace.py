#!/usr/bin/env python3
"""Inspect/install HST's Cline adapter without moving a user's knowledge base."""
import argparse
import hashlib
import subprocess
import importlib.util
import json
from pathlib import Path
import shutil
import sys

FRAMEWORK = Path(__file__).resolve().parents[1]


def plan(workspace, framework=FRAMEWORK, terminal=False):
    workspace, framework = Path(workspace).resolve(), Path(framework).resolve()
    if not workspace.is_dir():
        raise ValueError('workspace_not_directory')
    if not (framework / 'scripts/extract_evidence.py').is_file():
        raise ValueError('framework_not_found')
    entries = []
    for directory in ['.cline', '.clinerules']:
        for source in sorted((framework / directory).rglob('*')):
            if not source.is_file() or source.is_symlink():
                continue
            relative = source.relative_to(framework)
            target = workspace / relative
            if not target.resolve().is_relative_to(workspace):
                raise ValueError('destination_outside_workspace')
            if target.exists() and not target.is_file():
                raise ValueError('destination_not_file:' + relative.as_posix())
            status = ('same' if target.read_bytes() == source.read_bytes() else 'conflict') if target.exists() else 'missing'
            entries.append({'path': relative.as_posix(), 'status': status, 'source': str(source)})
    if workspace != framework:
        # Resolve actual ZIP names without assuming a conventional directory name.
        import os
        location = Path(os.path.relpath(framework, workspace)).as_posix()
        content = f'''# HST workspace locations\n\nKB_ROOT is the current workspace. FRAMEWORK_DIR is `{location}` relative to KB_ROOT. Resolve all HST scripts, templates, profiles, layers and docs against FRAMEWORK_DIR, including relative links in copied skills. Runs go in KB_ROOT/runs. Existing KB materials stay where they are.\n'''
        target = workspace / '.clinerules/05-hst-workspace.md'
        if not target.resolve().is_relative_to(workspace):
            raise ValueError('destination_outside_workspace')
        status = ('same' if target.read_text(encoding='utf-8') == content else 'conflict') if target.exists() else 'missing'
        entries.append({'path': '.clinerules/05-hst-workspace.md', 'status': status, 'content': content})
    if terminal:
        from vscode_tasks import task, merge
        if not (framework / 'scripts/terminal_progress.py').is_file():
            raise ValueError('terminal_viewer_not_found')
        for name in ['.vscode/tasks.json', '.hst/workspace.json']:
            target=workspace/name
            if not target.resolve().is_relative_to(workspace) or target.is_symlink():
                raise ValueError('terminal_destination_outside_workspace')
            if target.exists() and not target.is_file():
                raise ValueError('terminal_destination_not_file')
            old=target.read_text(encoding='utf-8') if target.exists() else ''
            if name.endswith('tasks.json'):
                content,owned_changed=merge(old,task(workspace,framework),replace=True)
                status='same' if content==old else ('conflict' if owned_changed else ('update' if old else 'missing'))
            else:
                import os
                value={'schema_version':1,'framework_dir':Path(os.path.relpath(framework,workspace)).as_posix(),'terminal_enabled':True}
                content=json.dumps(value,ensure_ascii=False,indent=2)+'\n'
                status='same' if content==old else ('conflict' if old else 'missing')
            entries.append({'path':name,'status':status,'content':content})
        updater=framework/'scripts/update_workspace.py'
        if updater.is_file():
            target=workspace/'.hst/update.py'
            if target.is_symlink() or not target.resolve().is_relative_to(workspace):
                raise ValueError('updater_destination_outside_workspace')
            status=('same' if target.read_bytes()==updater.read_bytes() else 'conflict') if target.exists() else 'missing'
            entries.append({'path':'.hst/update.py','status':status,'source':str(updater)})
    return {'workspace': str(workspace), 'framework': str(framework), 'files': entries,
            'readers': {name: bool(importlib.util.find_spec(name)) for name in ['docx', 'openpyxl', 'pypdf']},
            'python': sys.executable}


def install(workspace, framework=FRAMEWORK, replace=False, terminal=False):
    result = plan(workspace, framework, terminal)
    conflicts = [x['path'] for x in result['files'] if x['status'] == 'conflict']
    if conflicts and not replace:
        raise ValueError('conflicts; no files changed: ' + ', '.join(conflicts))
    for item in result['files']:
        if item['status'] == 'same':
            continue
        target = Path(workspace).resolve() / item['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        if 'content' in item:
            target.write_text(item['content'], encoding='utf-8')
        else:
            shutil.copyfile(item['source'], target)
    return result


def ensure_terminal(workspace, framework=FRAMEWORK):
    """Optional installation is explicit; never downloads dependencies on workspace open."""
    workspace,framework=Path(workspace).resolve(),Path(framework).resolve()
    state=workspace/'.hst';env=state/'terminal-venv'
    if state.is_symlink() or env.is_symlink():raise ValueError('terminal_environment_must_not_be_symlink')
    python=env/('Scripts/python.exe' if sys.platform=='win32' else 'bin/python')
    requirements=framework/'requirements-terminal.txt'
    digest=hashlib.sha256(requirements.read_bytes()).hexdigest()
    stamp=env/'.hst-requirements.sha256'
    if python.is_file() and stamp.is_file() and stamp.read_text()==digest:
        check=subprocess.run([str(python),'-c','import rich, click'],capture_output=True)
        if check.returncode==0:return str(python)
    if not python.exists():
        subprocess.run([sys.executable,'-m','venv',str(env)],check=True)
    subprocess.run([str(python),'-m','pip','install','--disable-pip-version-check','-r',str(requirements)],check=True,stdout=sys.stderr,stderr=sys.stderr)
    subprocess.run([str(python),'-c','import rich, click'],check=True)
    stamp.write_text(digest)
    return str(python)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workspace', type=Path, required=True)
    p.add_argument('--framework', type=Path, default=FRAMEWORK)
    p.add_argument('--apply', action='store_true')
    p.add_argument('--replace-framework-files', action='store_true')
    p.add_argument('--terminal',action='store_true',help='Install optional Rich/Click viewer and a dedicated VS Code folder-open task')
    args = p.parse_args()
    try:
        report=plan(args.workspace,args.framework,args.terminal)
        if args.apply:
            conflicts=[x['path'] for x in report['files'] if x['status']=='conflict']
            if conflicts and not args.replace_framework_files:
                raise ValueError('conflicts; no files changed: '+', '.join(conflicts))
            if args.terminal:
                terminal_python=ensure_terminal(args.workspace,args.framework)
            report=install(args.workspace,args.framework,args.replace_framework_files,args.terminal)
            if args.terminal:report['terminal_python']=terminal_python
        if args.terminal:
            report['terminal_task']='HST · Прогресс'
            report['terminal_note']='Allow automatic tasks for this trusted workspace in VS Code, or run Terminal > Run Task > HST · Прогресс. Existing windows need a task launch or folder reopen.'
        report['action'] = 'applied' if args.apply else 'inspection_only'
        print(json.dumps(report, ensure_ascii=False, indent=2))
    except (ValueError, OSError, subprocess.CalledProcessError) as e:
        p.error(str(e))


if __name__ == '__main__':
    main()
