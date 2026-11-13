"""Workspace-local active-run pointer. No latest-directory guessing or run mutations."""
from datetime import datetime, timezone
import json
from pathlib import Path
import uuid


def publish(run, workspace=None, *, preserve_startup=False):
    run=Path(run).resolve()
    if workspace is None:
        if run.parent.name!='runs':
            return None  # Custom layouts require an explicit workspace.
        workspace=run.parent.parent
    workspace=Path(workspace).resolve()
    if not run.is_relative_to(workspace) or not (run/'input/hypothesis.md').is_file():
        raise ValueError('Active run must be an existing hypothesis inside the workspace')
    state=workspace/'.hst'
    if state.is_symlink():raise ValueError('workspace state must not be a symlink')
    state.mkdir(exist_ok=True)
    if not preserve_startup:
        from startup_progress import read, update
        pending = read(workspace)
        if pending and pending['state'] not in {'attached', 'cancelled'}:
            update(workspace, session=pending['session_id'], status='cancelled',
                   message='Подготовка закрыта: явно выбран прогон ' + run.name)
    pointer=state/'active-run.json'
    if pointer.is_symlink():raise ValueError('active-run pointer must not be a symlink')
    value={'schema_version':1,'run_dir':run.relative_to(workspace).as_posix(),
           'run_id':run.name,'activation_id':uuid.uuid4().hex,
           'activated_at':datetime.now(timezone.utc).isoformat()}
    # Unique temporary name allows concurrent writers; the last explicit activation wins.
    tmp=state/('.active-run-'+uuid.uuid4().hex+'.tmp')
    try:
        tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
        tmp.replace(pointer)
    finally:tmp.unlink(missing_ok=True)
    return pointer


def resolve(workspace):
    workspace=Path(workspace).resolve();pointer=workspace/'.hst/active-run.json'
    if not pointer.exists():return None
    if pointer.is_symlink() or not pointer.resolve().is_relative_to(workspace):
        raise ValueError('Указатель прогона выходит за пределы рабочей папки')
    if pointer.stat().st_size>16384:raise ValueError('Слишком большой указатель прогона')
    data=json.loads(pointer.read_text(encoding='utf-8-sig'))
    if (not isinstance(data,dict) or data.get('schema_version')!=1 or
        not isinstance(data.get('run_dir'),str) or not isinstance(data.get('activation_id'),str)):
        raise ValueError('Некорректный указатель активного прогона')
    path=Path(data['run_dir'])
    if path.is_absolute():raise ValueError('Указатель должен содержать относительный путь')
    run=(workspace/path).resolve()
    if not run.is_relative_to(workspace) or data.get('run_id')!=run.name:
        raise ValueError('Активный прогон вне рабочей папки или ID не совпадает')
    return run,data['activation_id']


class Follow:
    """Maintain the last snapshot only within one activation, never across hypotheses."""
    def __init__(self,workspace):
        self.workspace=Path(workspace).resolve();self.key=None;self.last=None;self.run=None

    def poll(self,reader):
        try:
            from startup_progress import pending_snapshot
            pending = pending_snapshot(self.workspace)
            if pending is not None:
                self.last = None; self.key = None; self.run = None
                return pending, None, None
            active=resolve(self.workspace)
        except (OSError,ValueError) as e:
            self.last=None;self.key=None;self.run=None
            return None,'Нельзя определить активный прогон: '+str(e),None
        if active is None:
            self.last=None;self.key=None;self.run=None
            return None,'Ожидаю запуска гипотезы в Cline',None
        run,activation=active;key=(str(run),activation)
        if key!=self.key:self.last=None;self.key=key
        self.run=run
        try:
            snapshot=reader(run/'outputs/progress.json')
            if snapshot.get('run')!=run.name:raise ValueError('Журнал относится к другому прогону')
            self.last=snapshot
            return snapshot,None,run
        except FileNotFoundError:
            return self.last,'Ожидаю журнал нового прогона',run
        except (OSError,ValueError,KeyError,TypeError) as e:
            return self.last,'Журнал временно недоступен: '+str(e),run
