#!/usr/bin/env python3
"""Inspect/install HST's Cline adapter without moving a user's knowledge base."""
import argparse
import hashlib
import subprocess
from datetime import datetime, timezone
import uuid
import json
from pathlib import Path
import shutil
import sys

FRAMEWORK = Path(__file__).resolve().parents[1]


def plan(workspace, framework=FRAMEWORK, terminal=False):
    workspace, framework = Path(workspace).resolve(), Path(framework).resolve()
    if not workspace.is_dir():
        raise ValueError('workspace_not_directory')
    if not (framework / 'VERSION').is_file() or not (framework / '.cline/skills/hst-start/SKILL.md').is_file():
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
        for name in ['.vscode/tasks.json']:
            target=workspace/name
            if not target.resolve().is_relative_to(workspace) or target.is_symlink():
                raise ValueError('terminal_destination_outside_workspace')
            if target.exists() and not target.is_file():
                raise ValueError('terminal_destination_not_file')
            old=target.read_text(encoding='utf-8') if target.exists() else ''
            content,owned_changed=merge(old,task(workspace,framework),replace=True)
            status='same' if content==old else ('conflict' if owned_changed else ('update' if old else 'missing'))
            entries.append({'path':name,'status':status,'content':content})
    import os
    previous=settings(workspace)
    content='# HST workspace\n\nFramework: '+Path(os.path.relpath(framework,workspace)).as_posix()+'\nTerminal: '+('enabled' if terminal or previous.get('terminal_enabled') else 'disabled')+'\n'
    for name,body,source in [('.hst/workspace.md',content,None),('.hst/update.py',None,framework/'scripts/update_workspace.py')]:
        target=workspace/name
        if target.is_symlink():raise ValueError('symlink_in_installation')
        entry={'path':name,'status':'same' if target.is_file() and (target.read_text(encoding='utf-8')==body if body is not None else target.read_bytes()==source.read_bytes()) else ('conflict' if target.exists() else 'missing')}
        entry.update({'content':body} if body is not None else {'source':str(source)})
        entries.append(entry)
    return {'workspace':str(workspace),'framework':str(framework),'files':entries,'retire':retired(workspace,framework),'python':sys.executable}


def settings(workspace):
    state=Path(workspace)/'.hst'
    if state.is_symlink():raise ValueError('symlink_in_settings')
    path=state/'workspace.md'
    if path.is_symlink():raise ValueError('symlink_in_settings')
    if path.is_file():
        import re
        values=dict(re.findall(r'^(Framework|Terminal):[ \t]*(.*)$',path.read_text(encoding='utf-8-sig'),re.M))
        return {'framework_dir':values.get('Framework'),'terminal_enabled':values.get('Terminal')=='enabled'}
    old=state/'workspace.json'
    if old.is_symlink():raise ValueError('symlink_in_settings')
    return json.loads(old.read_text(encoding='utf-8-sig')) if old.exists() else {}


def retired(workspace,framework):
    workspace,framework=Path(workspace),Path(framework)
    names=['.hst/workspace.json','.hst/active-run.json','.hst/source-preferences.json','.hst/startup.json','.hst/startups','.hst/tui.json','.hst/tui-bridge.json','.hst/requests']
    manifest=framework/'maintenance/retired-paths.txt'
    if manifest.is_file():
        names += [n for n in manifest.read_text().splitlines() if n.startswith(('.cline/','.clinerules/'))]
    names += [p.relative_to(workspace).as_posix() for p in (workspace/'.hst').glob('hst-bridge-*.vsix')]
    names += [p.relative_to(workspace).as_posix() for p in (workspace/'.hst/bin').glob('hst-tui*')]
    result=[]
    for name in dict.fromkeys(names):
        p=workspace/name
        if p.exists() or p.is_symlink():
            if p.is_symlink() or not p.resolve().is_relative_to(workspace.resolve()) or (p.is_dir() and any(x.is_symlink() for x in p.rglob('*'))):raise ValueError('unsafe_retired_path')
            result.append(name)
    return result



def install(workspace, framework=FRAMEWORK, replace=False, terminal=False):
    result = plan(workspace, framework, terminal)
    conflicts = [x['path'] for x in result['files'] if x['status'] == 'conflict']
    if conflicts and not replace:
        raise ValueError('conflicts; no files changed: ' + ', '.join(conflicts))
    changed=[x for x in result['files'] if x['status']!='same']
    names=list(dict.fromkeys([x['path'] for x in changed]+result['retire']))
    saved={};backup=None
    if names:
        backup=Path(workspace)/'.hst/updates'/('setup-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8])
        if backup.parent.is_symlink():raise ValueError('updates_directory_must_not_be_symlink')
        backup.mkdir(parents=True)
        for name in names:
            target=Path(workspace)/name
            saved[name]=target.exists()
            if target.is_symlink() or (target.is_dir() and any(p.is_symlink() for p in target.rglob('*'))):raise ValueError('symlink_in_installation')
            if target.exists():
                copy=backup/name;copy.parent.mkdir(parents=True,exist_ok=True)
                if target.is_dir():shutil.copytree(target,copy)
                else:shutil.copy2(target,copy)
    try:
        for item in changed:
            target=Path(workspace)/item['path'];target.parent.mkdir(parents=True,exist_ok=True)
            if 'content' in item:target.write_text(item['content'],encoding='utf-8')
            else:shutil.copyfile(item['source'],target)
        for name in result['retire']:
            target=Path(workspace)/name
            if target.is_dir():shutil.rmtree(target)
            else:target.unlink(missing_ok=True)
    except Exception:
        for name,existed in saved.items():
            target=Path(workspace)/name
            if target.is_dir():shutil.rmtree(target)
            else:target.unlink(missing_ok=True)
            if existed:
                target.parent.mkdir(parents=True,exist_ok=True)
                if (backup/name).is_dir():shutil.copytree(backup/name,target)
                else:shutil.copy2(backup/name,target)
        raise
    result['backup']=str(backup) if backup else None
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
        check=subprocess.run([str(python),'-c','import rich'],capture_output=True)
        if check.returncode==0:return str(python)
    if not python.exists():
        subprocess.run([sys.executable,'-m','venv',str(env)],check=True)
    subprocess.run([str(python),'-m','pip','install','--disable-pip-version-check','-r',str(requirements)],check=True,stdout=sys.stderr,stderr=sys.stderr)
    subprocess.run([str(python),'-c','import rich'],check=True)
    stamp.write_text(digest)
    return str(python)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workspace', type=Path, required=True)
    p.add_argument('--framework', type=Path, default=FRAMEWORK)
    p.add_argument('--apply', action='store_true')
    p.add_argument('--replace-framework-files', action='store_true')
    p.add_argument('--terminal',action='store_true',help='Install optional Rich viewer and a dedicated VS Code folder-open task')
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
        print('HST workspace: '+report['action']+'\n'+str(report['workspace']))
        for item in report['files']:print('- '+item['status']+': '+item['path'])
        for item in report['retire']:print('- retire (backup): '+item)
        if report.get('backup'):print('Backup: '+report['backup'])
    except (ValueError, OSError, subprocess.CalledProcessError) as e:
        p.error(str(e))


if __name__ == '__main__':
    main()
