#!/usr/bin/env python3
"""Prepare a run, verify its live viewer and finish against the explicit run target."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys
import time
from urllib.request import urlopen

from run_progress import atomic, init, record
from validate_runs import check_run, validate_input


def load_config(run):
    p = run / 'run_config.json'
    value = json.loads(p.read_text(encoding='utf-8-sig')) if p.exists() else {}
    if not isinstance(value, dict):
        raise ValueError('invalid run config')
    return value


def save_config(run, config):
    atomic(run / 'run_config.json', json.dumps(config, ensure_ascii=False, indent=2))


def verify_viewer(url, run):
    # Never follow an arbitrary URL saved in an artifact.
    if not re.fullmatch(r'http://127\.0\.0\.1:\d+/', url):
        raise ValueError('viewer URL must be loopback')
    with urlopen(url + 'outputs/progress.html', timeout=2) as response:
        if response.status != 200 or b'progress.json' not in response.read():
            raise ValueError('viewer HTML unavailable')
    with urlopen(url + 'outputs/progress.json', timeout=2) as response:
        state = json.load(response)
        if state.get('run') != run.name:
            raise ValueError('viewer belongs to a different run')
    # Same run names can occur in different workspaces; verify a fresh identity file.
    token = json.loads((run / 'outputs/.viewer-identity.json').read_text(encoding='utf-8'))
    with urlopen(url + 'outputs/.viewer-identity.json', timeout=2) as response:
        if json.load(response) != token:
            raise ValueError('viewer workspace mismatch')
    return url + 'outputs/progress.html'


def viewer(run):
    import uuid
    state_path = run / 'outputs/.viewer-state.json'
    config = json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {}
    identity = run / 'outputs/.viewer-identity.json'
    if not identity.exists():
        atomic(identity, json.dumps({'token': uuid.uuid4().hex}))
    if config.get('viewer_url'):
        try:
            return verify_viewer(config['viewer_url'], run)
        except (OSError, ValueError):
            pass
    log = run / 'outputs/.viewer-server.log'
    with log.open('w', encoding='utf-8') as stream:
        kwargs = {'start_new_session': True} if sys.platform != 'win32' else {
            'creationflags': subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS}
        process = subprocess.Popen([sys.executable, str(Path(__file__).with_name('run_progress.py')),
                                    'serve', '--run-dir', str(run)], stdin=subprocess.DEVNULL,
                                   stdout=stream, stderr=stream, **kwargs)
    try:
        for _ in range(40):
            line = log.read_text(encoding='utf-8').splitlines()
            if line and line[0].startswith('http://127.0.0.1:'):
                url = line[0].strip()
                actual = verify_viewer(url, run)
                config['viewer_url'] = url
                atomic(state_path, json.dumps(config))
                return actual
            if process.poll() is not None:
                break
            time.sleep(.1)
        raise ValueError('viewer did not become ready; use run_progress.py serve in a separate terminal')
    except Exception:
        process.terminate()
        raise


def prepare(run, mode):
    errors = validate_input(run, check_folder_id=True)
    if errors:
        raise ValueError(', '.join(errors))
    config = load_config(run)
    if not config and any((run / 'outputs').glob('*.marker')):
        raise ValueError('Legacy run: use viewer/read-only validation; an explicit protocol upgrade is required.')
    if not config:
        config = {'protocol_version': 2, 'execution_mode': mode, 'language': 'ru',
                  'heavy_analysis': 'ask', 'analysis_choices': []}
        save_config(run, config)
    init(run)
    for phase in ['intake', 'validation']:
        record(run, phase=phase, state='completed', message='Входные данные проверены')
    return viewer(run)


def analysis_choice(run, choice, files, purpose):
    config = load_config(run)
    if not config:
        raise ValueError('prepare run first')
    config.setdefault('analysis_choices', []).append({
        'choice': choice, 'files': files, 'purpose': purpose,
        'at': datetime.now(timezone.utc).isoformat()})
    save_config(run, config)


def require_deep(run, files):
    choices = load_config(run).get('analysis_choices', [])
    if not choices or choices[-1]['choice'] != 'deep' or not set(files).issubset(choices[-1]['files']):
        raise ValueError('Deep analysis requires the user choice for these files; offer quick/deep/skip.')


def finish(run):
    errors = check_run(run)
    report = {'scope': 'run', 'target': str(run), 'status': 'FAIL' if errors else 'PASS',
              'errors': errors, 'limitations': 'Contracts and declared audit consistency only; not source truth or market demand.'}
    atomic(run / 'outputs/run_validation.json', json.dumps(report, ensure_ascii=False, indent=2))
    if errors:
        record(run, phase='human_report', state='error', message='Проверка текущего прогона: FAIL; см. run_validation.json')
        return report
    record(run, phase='human_report', state='completed', message='Проверен текущий RUN_DIR: PASS; решение принимает человек')
    p = run / 'input/hypothesis.md'
    text = p.read_text(encoding='utf-8-sig')
    text = re.sub(r'(?im)^(\s*[-*]\s+(?:\*\*)?(?:Статус|Status):(?:\*\*)?\s*)(?:\*\*|`)?(?:running|draft|выполняется|в работе)(?:\*\*|`)?\s*$', r'\g<1>completed', text)
    atomic(p, text)
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['prepare', 'viewer', 'finish', 'analysis-choice', 'require-deep'])
    p.add_argument('--run-dir', type=Path, required=True)
    p.add_argument('--mode', choices=['full', 'phase'], default='full')
    p.add_argument('--choice', choices=['quick', 'deep', 'skip'])
    p.add_argument('--file', action='append', default=[])
    p.add_argument('--purpose', default='')
    a = p.parse_args()
    run = a.run_dir.resolve()
    try:
        if a.action == 'prepare':
            print(prepare(run, a.mode))
        elif a.action == 'viewer':
            init(run); print(viewer(run))
        elif a.action == 'analysis-choice':
            if not a.choice or not a.file or not a.purpose:
                p.error('analysis-choice requires --choice, --file and --purpose (actual user response)')
            analysis_choice(run, a.choice, a.file, a.purpose)
        elif a.action == 'require-deep':
            if not a.file:
                p.error('require-deep requires --file')
            require_deep(run, a.file)
        else:
            result = finish(run); print(json.dumps(result, ensure_ascii=False, indent=2))
            return 1 if result['errors'] else 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        p.error(str(exc))
    return 0


if __name__ == '__main__':
    sys.exit(main())
