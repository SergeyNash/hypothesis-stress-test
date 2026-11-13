#!/usr/bin/env python3
"""Publish intake progress before RUN_DIR exists; preserve actual early timestamps."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import uuid

from run_progress import atomic, lock, init, record, PHASES, NAMES

STAGES = {'routing', 'intake', 'confirmation', 'bootstrap'}
STATES = {'running', 'waiting_user', 'error', 'cancelled'}


def directory(workspace, create=False):
    root = Path(workspace).resolve()
    state = root / '.hst'
    if state.is_symlink():
        raise ValueError('Startup state must not be a symlink')
    if create:
        state.mkdir(exist_ok=True)
    for name in ['startup.json', 'startups', '.progress.lock']:
        if (state / name).is_symlink():
            raise ValueError('Startup paths must not be symlinks')
    return root, state


def read(workspace):
    _, state = directory(workspace)
    path = state / 'startup.json'
    if not path.exists():
        return None
    if path.stat().st_size > 16384:
        raise ValueError('Startup state is too large')
    value = json.loads(path.read_text(encoding='utf-8-sig'))
    if (not isinstance(value, dict) or value.get('schema_version') != 1 or
            not re.fullmatch(r'[a-f0-9]{32}', str(value.get('session_id', ''))) or
            value.get('stage') not in STAGES or value.get('state') not in STATES | {'attached'} or
            not all(isinstance(value.get(k), str) for k in ['at', 'started_at', 'message'])):
        raise ValueError('Invalid startup state')
    return value


def persist(state, value):
    history = state / 'startups'
    history.mkdir(exist_ok=True)
    path = history / (value['session_id'] + '.jsonl')
    if path.is_symlink():
        raise ValueError('Startup history must not be a symlink')
    with path.open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(value, ensure_ascii=False) + '\n')
    atomic(state / 'startup.json', json.dumps(value, ensure_ascii=False, indent=2))
    return value


def update(workspace, *, session=None, stage='intake', status='running', message='Подготовка новой гипотезы'):
    if stage not in STAGES or status not in STATES or not message or len(message) > 2000:
        raise ValueError('Invalid startup event')
    _, state = directory(workspace, create=True)
    with lock(state):
        now = datetime.now(timezone.utc).isoformat(timespec='seconds')
        if session is None:
            value = {'schema_version': 1, 'session_id': uuid.uuid4().hex, 'started_at': now}
        else:
            value = read(workspace)
            if not value or value['session_id'] != session or value['state'] in {'attached', 'cancelled'}:
                raise ValueError('Startup session is no longer active; do not overwrite another session')
        value.update(at=now, stage=stage, state=status, message=message)
        return persist(state, value)


def attach(workspace, session, run):
    root, state = directory(workspace)
    run = Path(run).resolve()
    if (not run.is_relative_to(root) or not re.fullmatch(r'HYP-\d{4}-\d{2}-\d{2}-\d{3}', run.name)
            or not (run / 'input/hypothesis.md').is_file()):
        raise ValueError('Attach requires a bootstrapped hypothesis inside the workspace')
    with lock(state):
        value = read(root)
        if not value or value['session_id'] != session:
            raise ValueError('Startup session mismatch')
        if value['state'] == 'attached':
            if value.get('run_dir') == run.relative_to(root).as_posix():
                return value
            raise ValueError('Startup is already attached to another run')
        if value['state'] == 'cancelled':
            raise ValueError('Startup was cancelled')
        # Attach is only for a fresh bootstrap, never a shortcut into an old run.
        if (run / 'run_config.json').exists() or any((run / 'outputs').glob('*.marker')):
            raise ValueError('Attach requires a fresh run; resume old runs through hst-run')
        init(run)
        from run_progress import events
        rows = events(run / 'outputs')
        if not any(e['phase'] == 'intake' and e['state'] == 'completed' for e in rows):
            record(run, phase='intake', state='completed', message='Карточка и новая папка подтверждены')
        if not any(e['phase'] == 'validation' and e['state'] == 'running' for e in rows):
            record(run, phase='validation', state='running', message='Проверяю входные данные до запуска анализа')
        source = state / 'startups' / (session + '.jsonl')
        if source.is_symlink() or source.stat().st_size > 1024 * 1024:
            raise ValueError('Invalid startup history')
        dest = run / 'outputs/startup_events.jsonl'
        if dest.is_symlink():
            raise ValueError('Startup archive must not be a symlink')
        atomic(dest, source.read_text(encoding='utf-8'))
        from active_run import publish
        publish(run, root)
        value.update(state='attached', stage='bootstrap', run_dir=run.relative_to(root).as_posix(),
                     at=datetime.now(timezone.utc).isoformat(timespec='seconds'), message='Папка создана; проверка входных данных')
        return persist(state, value)


def pending_snapshot(workspace):
    value = read(workspace)
    if not value or value['state'] in {'attached', 'cancelled'}:
        return None
    phases = [dict(id=p, name=NAMES[p], state=value['state'] if p == 'intake' else 'pending',
                   message=value['message'] if p == 'intake' else '') for p in PHASES]
    event = dict(id=1, at=value['at'], kind='phase', phase='intake', state=value['state'], message=value['message'])
    return dict(run='Подготовка новой гипотезы', startup=True, startup_session=value['session_id'],
                phases=phases, events=[event], updated_at=value['at'], completed=0, total=len(phases))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['start', 'update', 'attach'])
    parser.add_argument('--workspace', type=Path, required=True)
    parser.add_argument('--session')
    parser.add_argument('--stage', choices=sorted(STAGES), default='intake')
    parser.add_argument('--state', choices=sorted(STATES), default='running')
    parser.add_argument('--message', default='Подготовка новой гипотезы')
    parser.add_argument('--run-dir', type=Path)
    args = parser.parse_args()
    if args.action != 'start' and not args.session:
        parser.error('--session is required')
    if args.action == 'attach' and not args.run_dir:
        parser.error('--run-dir is required')
    try:
        value = attach(args.workspace, args.session, args.run_dir) if args.action == 'attach' else update(
            args.workspace, session=args.session if args.action == 'update' else None,
            stage=args.stage, status=args.state, message=args.message)
        print(json.dumps(value, ensure_ascii=False))
    except (ValueError, OSError) as exc:
        parser.exit(1, 'Startup failed: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()
