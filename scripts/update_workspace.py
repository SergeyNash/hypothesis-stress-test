#!/usr/bin/env python3
"""Download HST main and update a nested ZIP installation with backups (stdlib only)."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile
from urllib.request import Request, urlopen
import uuid
import zipfile

ARCHIVE_URL='https://api.github.com/repos/SergeyNash/hypothesis-stress-test/zipball/main'
LIMIT=50*1024*1024
CONFIGS=['.cline','.clinerules','.vscode/tasks.json','.hst/workspace.json','.hst/update.py']
PROTECTED={'runs','.hst','.obsidian','.git'}


def download(destination):
    request=Request(ARCHIVE_URL,headers={'User-Agent':'hypothesis-stress-test-updater','Accept':'application/vnd.github+json'})
    with urlopen(request,timeout=60) as response, destination.open('wb') as stream:
        count=0
        while True:
            block=response.read(128*1024)
            if not block:break
            count+=len(block)
            if count>LIMIT:raise ValueError('Archive exceeds 50 MiB')
            stream.write(block)


def unpack(archive,destination):
    with zipfile.ZipFile(archive) as z:
        entries=z.infolist()
        if len(entries)>20000 or sum(e.file_size for e in entries)>250*1024*1024:
            raise ValueError('Archive expansion limit exceeded')
        seen=set();roots=set()
        for item in entries:
            path=PurePosixPath(item.filename)
            if (path.is_absolute() or '..' in path.parts or '\\' in item.filename or ':' in item.filename
                or stat.S_ISLNK(item.external_attr>>16) or not path.parts):
                raise ValueError('Unsafe archive entry')
            key=path.as_posix().casefold().rstrip('/')
            if key in seen:raise ValueError('Duplicate/case-colliding archive entry')
            seen.add(key);roots.add(path.parts[0])
            if len(path.parts)>1 and path.parts[1].casefold() in PROTECTED:
                # Upstream must not ship user state/runs into an updater payload.
                if path.parts[1].casefold()!='runs' or not (item.is_dir() or path.name in {'.gitkeep','.gitignore'}):
                    raise ValueError('Archive contains protected user state')
        if len(roots)!=1:raise ValueError('Expected one repository archive root')
        z.extractall(destination)
    package=destination/next(iter(roots))
    for name in ['VERSION','scripts/setup_workspace.py','scripts/extract_evidence.py','.clinerules','.cline']:
        if not (package/name).exists():raise ValueError('Incomplete framework archive: '+name)
    return package


def locations(workspace,framework=None):
    workspace=Path(workspace).resolve()
    if not workspace.is_dir():raise ValueError('Workspace must be an existing directory')
    state=workspace/'.hst'
    if state.is_symlink():raise ValueError('Workspace state must not be a symlink')
    if (state/'workspace.json').is_symlink():raise ValueError('Workspace settings must not be a symlink')
    if (state/'terminal-venv').is_symlink():raise ValueError('Terminal environment must not be a symlink')
    if framework is None and (state/'workspace.json').is_file():
        framework=workspace/json.loads((state/'workspace.json').read_text(encoding='utf-8-sig'))['framework_dir']
    if framework is None:framework=Path(__file__).resolve().parents[1]
    framework=Path(framework)
    if framework.is_symlink():raise ValueError('Framework must not be a symlink')
    framework=framework.resolve()
    if framework==workspace or not framework.is_relative_to(workspace):
        raise ValueError('Updater supports a framework folder inside the KB. Open DataB and pass --workspace there.')
    if framework.is_relative_to(state) or state.is_relative_to(framework):
        raise ValueError('Framework and updater state must be separate directories')
    if (framework/'.git').exists():raise ValueError('Git checkout detected; use git pull for this installation')
    if not (framework/'scripts/setup_workspace.py').is_file():raise ValueError('Existing framework installation not found')
    if Path.cwd().resolve().is_relative_to(framework):
        raise ValueError('Run the update from the KB root (DataB), outside the framework folder')
    for path in [framework,*[workspace/n for n in CONFIGS]]:
        if path.is_symlink() or (path.exists() and path.is_dir() and any(p.is_symlink() for p in path.rglob('*'))):
            raise ValueError('Symlink in update target: '+str(path))
        if not path.resolve().is_relative_to(workspace):raise ValueError('Update target outside workspace')
    return workspace,framework


@contextmanager
def update_lock(state):
    state.mkdir(exist_ok=True)
    lock=state/'update.lock'
    fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    try:
        os.close(fd)
        yield
    finally:lock.unlink(missing_ok=True)


def copy_item(source,target):
    target.parent.mkdir(parents=True,exist_ok=True)
    if source.is_dir():shutil.copytree(source,target)
    else:shutil.copy2(source,target)


def apply_setup(workspace,framework,terminal):
    command=[sys.executable,str(framework/'scripts/setup_workspace.py'),'--workspace',str(workspace),
             '--framework',str(framework),'--apply','--replace-framework-files']
    if terminal:command.append('--terminal')
    subprocess.run(command,cwd=workspace,check=True,env=dict(os.environ,PYTHONUTF8='1'))


def update(workspace,framework=None,*,apply=False,terminal=None,fetch=download,setup=apply_setup):
    workspace,framework=locations(workspace,framework)
    state=workspace/'.hst'
    if terminal is None:
        settings=state/'workspace.json'
        terminal=bool(json.loads(settings.read_text(encoding='utf-8-sig')).get('terminal_enabled')) if settings.is_file() else False
    with tempfile.TemporaryDirectory(prefix='hst-download-') as temporary:
        temp=Path(temporary);archive=temp/'framework.zip'
        fetch(archive);package=unpack(archive,temp/'unpacked')
        old=(framework/'VERSION').read_text(encoding='utf-8').strip() if (framework/'VERSION').is_file() else 'unknown'
        new=(package/'VERSION').read_text(encoding='utf-8').strip()
        report={'action':'inspection_only','source':ARCHIVE_URL,'workspace':str(workspace),
                'framework':str(framework),'old_version':old,'new_version':new,'terminal':terminal,
                'archive_root':package.name,
                'note':'main may change without a VERSION bump; the complete archive is applied'}
        if not apply:return report
        with update_lock(state):
            updates=state/'updates'
            if updates.is_symlink():raise ValueError('Updates directory must not be a symlink')
            backup=updates/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8])
            backup.mkdir(parents=True)
            saved=[];swapped=False
            prepared=framework.with_name('.'+framework.name+'-update-'+uuid.uuid4().hex)
            try:
                # Retain custom files, including nested runs; released files overlay the copy.
                shutil.copytree(framework,prepared,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
                for item in package.iterdir():
                    if item.name.casefold() in PROTECTED:continue
                    target=prepared/item.name
                    if item.is_dir():shutil.copytree(item,target,dirs_exist_ok=True)
                    else:shutil.copy2(item,target)
                for name in CONFIGS:
                    source=workspace/name
                    exists=source.exists();saved.append((name,exists))
                    if exists:copy_item(source,backup/'config'/name)
                # Dependency installation may repair/change an existing environment even
                # when the requirements text is unchanged. Preserve it for rollback too.
                env=state/'terminal-venv'
                env_existed=env.exists()
                if terminal and env_existed:
                    copy_item(env,backup/'terminal-venv')
                framework.rename(backup/'framework')
                swapped=True
                prepared.rename(framework)
                setup(workspace,framework,terminal)
                report.update(action='updated',backup=str(backup))
                (backup/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
                return report
            except Exception:
                if swapped:
                    if framework.exists():shutil.rmtree(framework)
                    (backup/'framework').rename(framework)
                    for name,existed in saved:
                        target=workspace/name
                        if target.is_dir():shutil.rmtree(target)
                        elif target.exists():target.unlink()
                        if existed:copy_item(backup/'config'/name,target)
                    if (backup/'terminal-venv').exists():
                        if (state/'terminal-venv').exists():shutil.rmtree(state/'terminal-venv')
                        shutil.copytree(backup/'terminal-venv',state/'terminal-venv')
                    elif terminal and not env_existed and (state/'terminal-venv').exists():
                        shutil.rmtree(state/'terminal-venv')
                raise
            finally:
                if prepared.exists():shutil.rmtree(prepared)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace',type=Path,required=True)
    parser.add_argument('--framework',type=Path)
    parser.add_argument('--apply',action='store_true',help='Download main, back up, update and apply Cline/terminal settings')
    group=parser.add_mutually_exclusive_group()
    group.add_argument('--terminal',dest='terminal',action='store_true')
    group.add_argument('--no-terminal',dest='terminal',action='store_false')
    parser.set_defaults(terminal=None)
    args=parser.parse_args()
    try:
        result=update(args.workspace,args.framework,apply=args.apply,terminal=args.terminal)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        if args.apply:print('Обновление применено. Перезапустите HST · Прогресс и начните новый чат Cline.')
        else:print('Проверка выполнена. Для обновления повторите команду с --apply.')
    except (OSError,ValueError,KeyError,zipfile.BadZipFile,subprocess.CalledProcessError) as exc:
        parser.exit(1,'Update failed: '+str(exc)+'\n')

if __name__=='__main__':main()
