#!/usr/bin/env python3
"""Workspace-local, acknowledged TUI/Cline launch and question protocol."""
import time as _hst_clock
_HST_STARTED = _hst_clock.perf_counter()
_HST_CPU_STARTED = _hst_clock.process_time()
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import uuid

from run_progress import atomic, lock

ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r'^[a-f0-9]{32}$')
TERMINAL = {'finished', 'failed', 'cancelled'}


def now():
    return datetime.now(timezone.utc).isoformat()


def state_root(workspace):
    root = Path(workspace).resolve()
    state = root / '.hst'
    for path in [state, state / 'requests', state / 'tui-bridge.json']:
        if path.is_symlink():
            raise ValueError('Control state must not be a symlink')
    state.mkdir(exist_ok=True)
    (state / 'requests').mkdir(exist_ok=True)
    return root, state


def location(workspace, request_id):
    if not ID.fullmatch(request_id):
        raise ValueError('Invalid request ID')
    root, state = state_root(workspace)
    directory = state / 'requests' / request_id
    if directory.is_symlink():
        raise ValueError('Request directory must not be a symlink')
    return root, directory


def read(path):
    if path.is_symlink() or not path.resolve().is_relative_to(path.parent.resolve()) or path.stat().st_size > 1024 * 1024:
        raise ValueError('Invalid control file')
    return json.loads(path.read_text(encoding='utf-8-sig'))


def save(path, value):
    if path.is_symlink():
        raise ValueError('Control file must not be a symlink')
    atomic(path, json.dumps(value, ensure_ascii=False, indent=2))


def bound_run(root, value):
    relative = Path(value['run_dir'])
    run = (root / relative).resolve()
    if relative.is_absolute() or not run.is_relative_to(root) or not re.fullmatch(r'HYP-\d{4}-\d{2}-\d{2}-\d{3}', run.name):
        raise ValueError('Invalid request/run binding')
    return run


def sync_run(root, directory, value):
    if not value.get('run_dir'):
        return
    run = bound_run(root, value)
    snapshot = dict(value)
    question_path = directory / 'question.json'
    if question_path.exists():
        snapshot['question'] = read(question_path)
    save(run / 'outputs/tui_control.json', snapshot)
    journal = run / 'outputs/tui_events.jsonl'
    if journal.is_symlink():
        raise ValueError('TUI journal must not be a symlink')
    with journal.open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(dict(snapshot, recorded_at=now()), ensure_ascii=False) + '\n')


def save_status(root, directory, value):
    save(directory / 'status.json', value)
    sync_run(root, directory, value)


def status(workspace, request_id):
    root, directory = location(workspace, request_id)
    result = read(directory / 'status.json')
    if result.get('run_dir'):
        run = (root / result['run_dir']).resolve()
        if not run.is_relative_to(root):
            raise ValueError('Run outside workspace')
        validation = run / 'outputs/run_validation.json'
        if validation.is_file():
            checked = read(validation)
            if result['state'] != 'finished' and checked.get('status') == 'PASS' and checked.get('scope') == 'run' and checked.get('target') == str(run):
                with lock(directory):
                    result = read(directory / 'status.json')
                    result.update(state='finished', at=now(), message='Прогон завершён; итоговая проверка PASS')
                    save_status(root, directory, result)
    if result['state'] not in TERMINAL:
        heartbeat = root / '.hst/tui-bridge.json'
        try:
            bridge = read(heartbeat)
            age = (datetime.now(timezone.utc) - datetime.fromisoformat(bridge['at'])).total_seconds()
            if age > 12 or bridge.get('ready') is not True:
                result['connection'] = 'Нет связи с VS Code/Cline; запрос сохранён. Открой ту же базу в VS Code.'
        except (OSError, ValueError, KeyError):
            result['connection'] = 'Связь с VS Code недоступна; запрос сохранён.'
    question = directory / 'question.json'
    if question.exists():
        result['question'] = read(question)
    return result


def change(workspace, request_id, event, message=''):
    root, directory = location(workspace, request_id)
    allowed = {'queued': {'failed'}, 'allocated': {'failed'}, 'prepared': {'dispatching'}, 'dispatching': {'dispatched', 'accepted', 'failed'},
               'dispatched': {'accepted', 'failed'}, 'accepted': {'accepted', 'failed'}}
    with lock(directory):
        value = read(directory / 'status.json')
        # Acknowledge may arrive before the extension's promise resolves.
        if event == 'dispatched' and value['state'] == 'accepted':
            return value
        if event not in allowed.get(value['state'], set()):
            raise ValueError('Invalid launch transition: ' + value['state'] + ' -> ' + event)
        value.update(state=event, at=now(), message=message)
        save_status(root, directory, value)
        return value


def normalize(root, data):
    if not isinstance(data, dict):
        raise ValueError('Expected launch object')
    for key in ['statement', 'domain', 'audience', 'scenario', 'roles']:
        value = data.get(key)
        if not isinstance(value, str) or not value.strip() or len(value) > 20000:
            raise ValueError('Заполни поле: ' + key)
    if data.get('profile') not in {'digital_product', 'service_business'}:
        raise ValueError('Invalid profile')
    from service_profile import TYPES
    if data['profile'] == 'service_business' and data.get('hypothesis_type') not in TYPES:
        raise ValueError('Invalid service hypothesis type')
    channels = data.get('channels')
    if not isinstance(channels, dict) or set(channels) != {'local', 'confluence', 'internet'} or any(type(v) is not bool for v in channels.values()):
        raise ValueError('Choose all three source channels')
    paths = data.get('local_paths', [])
    if not isinstance(paths, list) or any(not isinstance(p, str) for p in paths):
        raise ValueError('Invalid local folders')
    cleaned_paths = []
    if paths and not channels['local']:
        raise ValueError('Папки доступны только при включённой локальной базе')
    for path in paths:
        relative = Path(path)
        target = (root / relative).resolve()
        if relative.is_absolute() or not target.is_relative_to(root) or not target.is_dir():
            raise ValueError('Папка должна существовать внутри базы: ' + path)
        if target == root / '.hst' or target.is_relative_to(root / '.hst'):
            raise ValueError('Runtime state is not an evidence source')
        cleaned_paths.append(target.relative_to(root).as_posix())
    return {k: data[k].strip() for k in ['statement', 'domain', 'audience', 'scenario', 'roles']} | {
        'profile': data['profile'], 'hypothesis_type': data.get('hypothesis_type', ''),
        'channels': channels, 'local_paths': cleaned_paths}


def submit(workspace, data):
    root, state = state_root(workspace)
    heartbeat = state / 'tui-bridge.json'
    if not heartbeat.exists():
        raise ValueError('Нет связи с VS Code. Установи HST Bridge и открой эту базу в VS Code.')
    bridge = read(heartbeat)
    age = (datetime.now(timezone.utc) - datetime.fromisoformat(bridge['at'])).total_seconds()
    if age > 12 or age < -5 or bridge.get('workspace') != str(root) or bridge.get('ready') is not True:
        raise ValueError('Модуль связи не готов: ' + str(bridge.get('message', 'открой VS Code с HST Bridge и Cline')))
    payload = normalize(root, data)
    with lock(state):
        for previous in (state / 'requests').iterdir():
            if previous.is_symlink() or not ID.fullmatch(previous.name):
                continue
            value = status(root, previous.name)
            if value['state'] not in TERMINAL:
                raise ValueError('Уже есть незавершённый запуск: ' + previous.name)
        request_id = uuid.uuid4().hex
        _, directory = location(root, request_id)
        directory.mkdir()
        request = {'schema_version': 1, 'request_id': request_id, 'at': now(), 'config': payload}
        save(directory / 'request.json', request)
        value = {'schema_version': 1, 'request_id': request_id, 'state': 'queued', 'at': now(),
                 'message': 'Настройки сохранены; ожидаю передачи в Cline'}
        save(directory / 'status.json', value)
    return value


def markdown(config, name):
    date = name[4:14]
    single = lambda key: re.sub(r'\s+', ' ', config[key]).strip()
    roles = [r.strip() for r in config['roles'].split(';') if r.strip()]
    text = f'''# Гипотеза

## Метаданные

- ID гипотезы: {name}
- Дата создания: {date}
- ID прогона: RUN-{name[4:]}
- Статус: draft
- Профиль применения: {config['profile']}

## Формулировка

{config['statement']}

## Релевантные роли

''' + '\n'.join('- ' + re.sub(r'\s+', ' ', r) for r in roles) + f'''

## Контекст исследования

- Домен: {single('domain')}
- Целевая аудитория: {single('audience')}
- Сценарий: {single('scenario')}
'''
    if config['profile'] == 'service_business':
        text += f'''
## Сервисный контекст

- Тип гипотезы: {config['hypothesis_type']}
- Владелец решения: Не задан; уточнить через TUI
- Текущий способ: Не задан; уточнить через TUI
- Результат заказчика: Не задан отдельно; уточнить из формулировки
- Обещание услуги: Не задано отдельно; уточнить границы через TUI
- Изменение у поставщика: Не задано отдельно; уточнить через TUI
- Привязка ролей: {single('roles')}; стороны неуказанных ролей требуют уточнения
'''
    return text


def bootstrap(workspace, request_id):
    root, directory = location(workspace, request_id)
    with lock(directory):
        value = read(directory / 'status.json')
        if value['state'] != 'queued':
            return value
        request = read(directory / 'request.json')
        config = normalize(root, request['config'])
        # Allocation is serialized per workspace; existing run folders are never reused.
        _, state = state_root(root)
        with lock(state):
            runs = root / 'runs'
            if runs.is_symlink():
                raise ValueError('runs must not be a symlink')
            runs.mkdir(exist_ok=True)
            date = datetime.now().astimezone().strftime('%Y-%m-%d')
            for suffix in range(1, 1000):
                run = runs / f'HYP-{date}-{suffix:03d}'
                try:
                    run.mkdir()
                    break
                except FileExistsError:
                    continue
            else:
                raise ValueError('No free run ID')
        (run / 'input/attachments').mkdir(parents=True)
        (run / 'outputs').mkdir()
        (run / 'input/hypothesis.md').write_text(markdown(config, run.name), encoding='utf-8')
        (run / 'run.md').write_text('# Run\n\nCreated by explicit TUI launch ' + request_id + '\n', encoding='utf-8')
        # Persist allocation before a viewer/setup failure so retries never allocate a second folder.
        value.update(state='allocated', run_dir=run.relative_to(root).as_posix(), at=now())
        save_status(root, directory, value)
        (run / 'outputs/tui_launch.json').write_bytes((directory / 'request.json').read_bytes())
        try:
            from run_control import prepare, load_config, save_config
            try:
                prepare(run, 'full', root)
            except Exception:
                # Keep a real viewer failure. Do not pretend it started or permit roles yet.
                raise
            run_config = load_config(run)
            run_config['tui_request_pending'] = True
            save_config(run, run_config)
            from source_selection import select
            select(run, config['channels'], config['local_paths'], root, reason='Пользователь нажал Запустить в TUI; request ' + request_id)
            run_config = load_config(run)
            run_config['tui_request_id'] = request_id
            run_config['framework_version'] = (ROOT / 'VERSION').read_text().strip()
            run_config['tui_request_sha256'] = hashlib.sha256((directory / 'request.json').read_bytes()).hexdigest()
            save_config(run, run_config)
            value.update(state='prepared', message='Папка создана, настройки источников применены; передаю в Cline', at=now())
        except Exception as exc:
            value.update(state='failed', message=str(exc), at=now())
            save_status(root, directory, value)
            raise
        save_status(root, directory, value)
        return value


def acknowledge(workspace, request_id):
    root, directory = location(workspace, request_id)
    value = read(directory / 'status.json')
    run = bound_run(root, value)
    from run_control import load_config
    config = load_config(run)
    digest = hashlib.sha256((directory / 'request.json').read_bytes()).hexdigest()
    if config.get('tui_request_id') != request_id or config.get('tui_request_sha256') != digest:
        raise ValueError('Launch request binding mismatch')
    expected = read(directory / 'request.json')['config']
    selected = config.get('source_selection', {})
    if selected.get('channels') != expected['channels'] or selected.get('local_paths') != expected['local_paths']:
        raise ValueError('Saved sources differ from the submitted TUI choice')
    accepted = change(root, request_id, 'accepted', 'Cline принял запрос и сохранённую конфигурацию')
    from run_control import save_config, auto_enter
    config['tui_request_pending'] = False
    save_config(run, config)
    auto_enter(run)
    return accepted


def question(workspace, request_id, text, options, phase):
    root, directory = location(workspace, request_id)
    value = read(directory / 'status.json')
    if value['state'] != 'accepted':
        raise ValueError('Only an acknowledged Cline task may ask a question')
    if not text.strip() or len(text) > 8000 or len(options) > 8:
        raise ValueError('Invalid question')
    from run_progress import PHASES, record
    if phase not in PHASES:
        raise ValueError('Invalid question phase')
    path = directory / 'question.json'
    with lock(directory):
        if path.exists() and read(path)['state'] != 'consumed':
            raise ValueError('Resolve the existing question first')
        item = {'id': uuid.uuid4().hex, 'state': 'pending', 'question': text,
                'options': options, 'phase': phase, 'at': now()}
        save(path, item)
        sync_run(root, directory, value)
    record(bound_run(Path(workspace).resolve(), value), phase=phase, state='waiting_user', message=text[:4000])
    return item


def answer(workspace, request_id, question_id, response, consume=False):
    root, directory = location(workspace, request_id)
    with lock(directory):
        path = directory / 'question.json'
        item = read(path)
        if item['id'] != question_id:
            raise ValueError('Stale question response')
        if consume:
            if item['state'] not in {'answered', 'sent'}:
                raise ValueError('Question is not answered')
            value = read(directory / 'status.json')
            from run_progress import record
            record(bound_run(Path(workspace).resolve(), value), phase=item['phase'], state='running', message='Ответ из TUI получен: ' + item['response'][:3000])
            item['state'] = 'consumed'
        else:
            if item['state'] != 'pending' or not response.strip() or len(response) > 8000:
                raise ValueError('Question is already answered or response is empty')
            if item['options'] and response not in item['options']:
                raise ValueError('Choose a displayed option')
            item.update(state='answered', response=response, answered_at=now())
        save(path, item)
        sync_run(root, directory, read(directory / 'status.json'))
    return item


def question_sent(workspace, request_id, question_id):
    root, directory = location(workspace, request_id)
    value = read(directory / 'status.json')
    from active_run import resolve
    active = resolve(root)
    if not active or active[0] != (root / value['run_dir']).resolve():
        raise ValueError('Another run is active; do not send this answer into Cline')
    with lock(directory):
        item = read(directory / 'question.json')
        if item['id'] != question_id or item['state'] != 'answered':
            raise ValueError('Stale/already delivered response')
        item.update(state='sent', sent_at=now())
        save(directory / 'question.json', item)
        sync_run(root, directory, value)
    return item


def validate_run_binding(run):
    run = Path(run)
    config_path = run / 'run_config.json'
    if not config_path.exists():
        return []
    config = read(config_path)
    request_id = config.get('tui_request_id')
    if request_id is None:
        return []
    if not isinstance(request_id, str) or not ID.fullmatch(request_id):
        return ['INVALID_TUI_REQUEST_ID']
    launch = run / 'outputs/tui_launch.json'
    snapshot = run / 'outputs/tui_control.json'
    if not launch.is_file() or not snapshot.is_file():
        return ['MISSING_TUI_LAUNCH_RECORDS']
    request = read(launch); value = read(snapshot)
    errors = []
    if (request.get('request_id') != request_id or value.get('request_id') != request_id or
            hashlib.sha256(launch.read_bytes()).hexdigest() != config.get('tui_request_sha256')):
        errors.append('TUI_LAUNCH_BINDING_MISMATCH')
    if config.get('tui_request_pending') or value.get('state') not in {'accepted', 'finished'}:
        errors.append('TUI_EXECUTOR_NOT_ACKNOWLEDGED')
    if value.get('question', {}).get('state', 'consumed') != 'consumed':
        errors.append('PENDING_TUI_QUESTION')
    history = config.get('source_selection_history', [])
    if not history or history[0].get('channels') != request.get('config', {}).get('channels'):
        errors.append('TUI_SOURCE_CHOICE_MISMATCH')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['submit', 'bootstrap', 'status', 'transition', 'acknowledge', 'ask', 'answer', 'consume', 'question-sent', 'current'])
    parser.add_argument('--workspace', type=Path, required=True)
    parser.add_argument('--request')
    parser.add_argument('--event')
    parser.add_argument('--message', default='')
    parser.add_argument('--question')
    parser.add_argument('--question-id')
    parser.add_argument('--option', action='append', default=[])
    parser.add_argument('--phase', default='local_evidence')
    parser.add_argument('--response', default='')
    args = parser.parse_args()
    try:
        if args.action == 'current':
            state = Path(args.workspace).resolve() / '.hst/requests'
            candidates = [status(args.workspace, p.name) for p in state.iterdir() if ID.fullmatch(p.name)] if state.is_dir() else []
            active = [c for c in candidates if c['state'] not in TERMINAL]
            result = max(active or candidates, key=lambda c: c['at']) if candidates else {}
        elif args.action == 'submit':
            result = submit(args.workspace, json.load(sys.stdin))
        else:
            if not args.request:
                raise ValueError('--request is required')
            if args.action == 'bootstrap': result = bootstrap(args.workspace, args.request)
            elif args.action == 'status': result = status(args.workspace, args.request)
            elif args.action == 'transition': result = change(args.workspace, args.request, args.event, args.message)
            elif args.action == 'acknowledge': result = acknowledge(args.workspace, args.request)
            elif args.action == 'question-sent': result = question_sent(args.workspace, args.request, args.question_id)
            elif args.action == 'ask': result = question(args.workspace, args.request, args.question or '', args.option, args.phase)
            else: result = answer(args.workspace, args.request, args.question_id, args.response, consume=args.action == 'consume')
        print(json.dumps(result, ensure_ascii=False))
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, 'TUI: ' + str(exc) + '\n')


if __name__ == '__main__':
    from runtime_metrics import execute
    raise SystemExit(execute(main, 'tui_control', _HST_STARTED, _HST_CPU_STARTED))
