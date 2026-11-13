#!/usr/bin/env python3
"""Local HST event journal and live progress viewer (stdlib, loopback only)."""
from __future__ import annotations
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import sys
import time
import uuid
from urllib.parse import unquote, urlsplit

from validate_runs import MARKER_REGISTRY, validate_input, validate_marker, check_run

ROOT = Path(__file__).resolve().parents[1]
PHASES = ['intake', 'validation'] + [v['completed_phase'] for v in MARKER_REGISTRY.values()]
STATES = {'pending', 'running', 'waiting_user', 'completed', 'error', 'invalidated'}
CHANNEL_STATES = {'query_started', 'found', 'read', 'used', 'completed', 'no_results',
                  'partial', 'unavailable', 'auth_error', 'error', 'waiting_approval', 'declined'}
NAMES = {'intake': 'Подготовка гипотезы', 'validation': 'Проверка входных данных',
         'facilitator': 'Стресс-тест ролей', 'local_evidence': 'Локальные материалы',
         'business_context': 'Бизнес-контекст и исследование', 'market': 'Проверка рынка',
         'synthesis': 'Сопоставление сигналов', 'customer_discovery_planning': 'План проверки',
         'decision_review': 'Критический разбор', 'human_report': 'Итоговый отчёт'}


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def output_dir(run):
    run = Path(run).resolve()
    output = run / 'outputs'
    if output.is_symlink():
        raise ValueError('outputs must not be a symlink')
    output.mkdir(parents=True, exist_ok=True)
    for name in ['pipeline_events.jsonl', 'progress.json', 'progress.html', '.progress.lock']:
        if (output / name).is_symlink():
            raise ValueError('progress files must not be symlinks')
    return output


@contextmanager
def lock(output):
    path = output / '.progress.lock'
    for attempt in range(41):
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            break
        except FileExistsError:
            if attempt == 40:raise ValueError('Progress journal is locked; check for another writer or interrupted process: '+str(path))
            time.sleep(.05)
    try:
        os.close(fd)
        yield
    finally:
        path.unlink()


def events(output):
    p = output / 'pipeline_events.jsonl'
    return [json.loads(line) for line in p.read_text(encoding='utf-8').splitlines() if line.strip()] if p.exists() else []


def snapshot(run, rows):
    from source_selection import config
    from phase_checks import diagnose
    states = {p: {'state': 'pending', 'message': ''} for p in PHASES}
    for row in rows:
        if row['kind'] == 'phase':
            states[row['phase']] = {k: row[k] for k in ['state', 'message', 'at']}
    return {'schema_version': 1, 'run': Path(run).name, 'updated_at': rows[-1]['at'] if rows else None,
            'phases': [dict(id=p, name=NAMES[p], **states[p]) for p in PHASES],
            'events': rows, 'completed': sum(s['state'] == 'completed' for s in states.values()),
            'total': len(states), 'source_selection': config(run).get('source_selection'),
            'source_selection_required': config(run).get('source_selection_version') == 1,
            'viewer': config(run).get('viewer',{}), 'warnings': diagnose(run,rows)}


def atomic(path, content):
    tmp = path.with_name('.'+path.name+'.'+uuid.uuid4().hex+'.tmp')
    fd = os.open(tmp, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(content)
        for attempt in range(21):
            try:
                os.replace(tmp, path)
                break
            except PermissionError:
                if attempt == 20:raise
                time.sleep(.05)
    finally:
        if tmp.exists():
            tmp.unlink()


def record(run, *, phase, state, message, channel=None, query='', urls=None, _transition=False):
    from source_selection import require, COLLECTION_PHASES, OPERATIONS
    if channel and state in OPERATIONS:require(run,channel)
    if not channel and phase in COLLECTION_PHASES and state == 'running':require(run)
    from phase_checks import enabled, require_previous, check
    if not channel and enabled(run):
        if state=='completed' and phase not in {'intake','validation'} and not _transition:
            raise ValueError('Use run_control.py complete/finish to verify and persist phase completion')
        if state in {'running','completed'} and phase not in {'intake','validation'}:require_previous(run,phase)
        if state == 'completed' and phase not in {'intake','validation'}:
            errors=check(run,phase)
            if errors:raise ValueError('Phase verification failed: '+', '.join(errors))
    if phase not in PHASES or state not in (CHANNEL_STATES if channel else STATES):
        raise ValueError('invalid phase/state')
    if channel not in {None, 'local', 'confluence', 'internet'}:
        raise ValueError('invalid channel')
    if len(message) > 4000 or len(query) > 1000 or len(urls or []) > 30:
        raise ValueError('event fields exceed limits')
    if not channel and state == 'completed':
        if phase == 'validation':
            problems = validate_input(Path(run), check_folder_id=True)
        elif phase == 'intake':
            problems = [] if (Path(run) / 'input/hypothesis.md').is_file() else ['missing input']
        else:
            name, spec = next((k, v) for k, v in MARKER_REGISTRY.items() if v['completed_phase'] == phase)
            p = Path(run) / 'outputs' / name
            problems = validate_marker(p, spec) if p.is_file() else ['missing marker']
            if phase == 'local_evidence':
                from validate_runs import validate_evidence
                problems += validate_evidence(Path(run) / 'outputs/evidence_inventory.md')
        if phase == 'human_report':
            problems += check_run(run)
        if problems:
            raise ValueError('completion verification failed: ' + ', '.join(problems))
    if phase == 'facilitator' and state == 'running' and not channel:
        config_path = Path(run) / 'run_config.json'
        config = json.loads(config_path.read_text(encoding='utf-8-sig')) if config_path.exists() else {}
        if config.get('audit_version') == 2:
            viewer = config.get('viewer', {})
            if viewer.get('status') == 'ready':
                from run_control import verify_viewer
                try:
                    verify_viewer(viewer['url'], Path(run).resolve())
                except (OSError, ValueError, KeyError) as exc:
                    raise ValueError('Viewer unavailable before facilitator; restart viewer and show URL, or report actual failure.') from exc
            elif not (viewer.get('status') == 'unavailable' and viewer.get('notified') and viewer.get('reason')):
                raise ValueError('Prepare and show the verified progress URL before facilitator.')
    output = output_dir(run)
    with lock(output):
        rows = events(output)
        previous = next((r for r in reversed(rows) if r['phase'] == phase and r['kind'] == 'phase'), None)
        if not channel and previous and previous['state'] == 'completed' and state == 'running':
            raise ValueError('invalidate completed phase before rerun')
        row = {'id': len(rows) + 1, 'at': now(), 'kind': 'source' if channel else 'phase',
               'phase': phase, 'state': state, 'message': message}
        if channel:
            row.update(channel=channel, query=query, urls=urls or [])
        with (output / 'pipeline_events.jsonl').open('a', encoding='utf-8') as f:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')
        rows.append(row)
        atomic(output / 'progress.json', json.dumps(snapshot(run, rows), ensure_ascii=False, indent=2))
    return row


class Viewer(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def guess_type(self, path):
        suffix = Path(path).suffix.lower()
        # Generated run text is UTF-8. Raw Markdown has no HTML meta tag, so
        # direct browser navigation needs the charset in the HTTP response.
        if suffix in {'.md', '.markdown', '.txt', '.log', '.jsonl', '.srt', '.vtt'}:
            return 'text/plain; charset=utf-8'
        if suffix in {'.json', '.marker'}:
            return 'application/json; charset=utf-8'
        content_type = super().guess_type(path)
        if content_type.startswith('text/') or suffix == '.js':
            return content_type + '; charset=utf-8'
        return content_type

    def send_head(self):
        request = unquote(urlsplit(self.path).path)
        if request == '/':
            self.send_response(302)
            self.send_header('Location', '/outputs/progress.html')
            self.end_headers()
            return None
        path = Path(self.translate_path(self.path)).resolve()
        root = Path(self.directory).resolve()
        if request == '/outputs/progress.json':
            import io
            try:
                journal=root/'outputs/pipeline_events.jsonl'
                if not journal.resolve().is_relative_to(root) or journal.is_symlink():
                    raise ValueError('Journal outside run')
                content=json.dumps(snapshot(root,events(root/'outputs')),ensure_ascii=False).encode('utf-8')
            except (OSError,ValueError,KeyError,TypeError):
                self.send_error(503,'Progress journal temporarily unreadable');return None
            self.send_response(200)
            self.send_header('Content-Type','application/json; charset=utf-8')
            self.send_header('Content-Length',str(len(content)))
            self.end_headers()
            return io.BytesIO(content)
        # Only serve explicit run files, never directory listings or outside symlinks.
        if not path.is_relative_to(root) or not path.is_file():
            self.send_error(404)
            return None
        return super().send_head()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'")
        super().end_headers()


def init(run):
    output = output_dir(run)
    with lock(output):
        atomic(output / 'progress.html', (ROOT / 'templates/progress.html').read_text(encoding='utf-8'))
        atomic(output / 'progress.json', json.dumps(snapshot(run, events(output)), ensure_ascii=False, indent=2))
    return output


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['init', 'event', 'serve'])
    p.add_argument('--run-dir', type=Path, required=True)
    p.add_argument('--phase', choices=PHASES)
    p.add_argument('--state')
    p.add_argument('--message', default='')
    p.add_argument('--channel', choices=['local', 'confluence', 'internet'])
    p.add_argument('--query', default='')
    p.add_argument('--url', action='append', default=[])
    p.add_argument('--port', type=int, default=0)
    args = p.parse_args()
    run = args.run_dir.resolve()
    if not run.is_dir():
        p.error('run directory does not exist')
    try:
        if args.action == 'event':
            if not args.phase or not args.state:
                p.error('event requires --phase and --state')
            print(json.dumps(record(run, phase=args.phase, state=args.state,
                  message=args.message, channel=args.channel, query=args.query, urls=args.url), ensure_ascii=False))
        else:
            init(run)
            if args.action == 'init':
                print('Created outputs/progress.html and progress.json; live view requires serve.')
            else:
                server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(Viewer, directory=str(run)))
                print(f'http://127.0.0.1:{server.server_port}/', flush=True)
                try:
                    server.serve_forever()
                except KeyboardInterrupt:
                    pass
                finally:
                    server.server_close()
    except (ValueError, FileExistsError, json.JSONDecodeError) as exc:
        p.error(str(exc))


if __name__ == '__main__':
    main()
