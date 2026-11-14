"""Passive timing for existing HST CLI calls; never a new completion gate."""
from contextvars import ContextVar
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from functools import wraps
import json
import os
from pathlib import Path
import sys
import time
import uuid

_current = ContextVar('hst_command_metrics', default=None)
POLL_ACTIONS = {'status', 'current', 'serve', 'metrics'}
INSTRUMENTED = ['run_control', 'run_progress (except serve)', 'audit_records', 'source_snapshot',
                'discover_sources', 'extract_evidence', 'tui_control (except polls)']


def stamp(value):
    try:
        result = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return result if result.tzinfo is not None else None
    except (AttributeError, ValueError):
        return None


def argument(argv, name):
    for i, value in enumerate(argv):
        if value == name and i + 1 < len(argv): return argv[i + 1]
        if value.startswith(name + '='): return value[len(name) + 1:]
    return None


@contextmanager
def section(name, phase=None):
    context = _current.get()
    if context is None:
        yield
        return
    before = time.perf_counter()
    depth = context['depth']; context['depth'] += 1
    try:
        yield
    finally:
        context['depth'] -= 1
        context['sections'].append({'name': name, 'phase': phase, 'depth': depth,
                                    'duration_ms': round((time.perf_counter() - before) * 1000, 3)})


def timed(name, phase_argument=None):
    def decorate(function):
        @wraps(function)
        def wrapped(*args, **kwargs):
            phase = kwargs.get('phase')
            if phase_argument is not None and len(args) > phase_argument:
                phase = args[phase_argument]
            with section(name, phase):
                return function(*args, **kwargs)
        return wrapped
    return decorate


def union_seconds(intervals, start=None, end=None):
    clipped = []
    for a, b in intervals:
        if start is not None: a = max(a, start)
        if end is not None: b = min(b, end)
        if b > a: clipped.append((a, b))
    merged = []
    for a, b in sorted(clipped):
        if merged and a <= merged[-1][1]: merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else: merged.append((a, b))
    return sum((b - a).total_seconds() for a, b in merged)


def waiting_intervals(events, end):
    opened = {}; intervals = []; by_reason = {}
    def close(key, at):
        if key not in opened: return
        began, reason = opened.pop(key)
        if at >= began:
            intervals.append((began, at)); by_reason.setdefault(reason, []).append((began, at))
    for event in events:
        at = stamp(event.get('at'))
        if at is None: continue
        phase = event.get('phase'); kind = event.get('kind'); state = event.get('state')
        key = (kind, phase, event.get('channel'))
        if state in {'waiting_user', 'waiting_approval'}:
            if key not in opened:
                reason = event.get('wait_reason') or ('user_input' if state == 'waiting_user' else 'tool_approval')
                opened[key] = (at, reason)
        else:
            close(key, at)
        if kind == 'phase' and state in {'completed', 'error', 'invalidated'}:
            for other in list(opened):
                if other[1] == phase: close(other, at)
    open_count = len(opened)
    for key in list(opened): close(key, end)
    return intervals, by_reason, open_count


def read_lines(path):
    if not path.exists(): return []
    if path.is_symlink(): raise ValueError('Metrics/journal must not be a symlink')
    return [json.loads(line) for line in path.read_text(encoding='utf-8-sig').splitlines() if line.strip()]


def summarize(run, *, now=None):
    run = Path(run).resolve(); output = run / 'outputs'
    events = read_lines(output / 'pipeline_events.jsonl')
    commands = read_lines(output / 'command_metrics.jsonl')
    config_path = run / 'run_config.json'
    config = json.loads(config_path.read_text(encoding='utf-8-sig')) if config_path.exists() else {}
    times = [stamp(e.get('at')) for e in events]; times = [t for t in times if t]
    finished = any(e.get('kind') == 'phase' and e.get('phase') == 'human_report' and e.get('state') == 'completed' for e in events)
    end = max(times) if finished and times else (now or datetime.now(timezone.utc))
    start = min(times) if times else end
    waits, reasons, open_waits = waiting_intervals(events, end)
    process_intervals = [(stamp(c.get('started_at')), stamp(c.get('ended_at'))) for c in commands]
    process_intervals = [(a, b) for a, b in process_intervals if a and b]
    duration = max(0, (end - start).total_seconds())
    waited = union_seconds(waits, start, end)
    script_union = union_seconds(process_intervals, start, end)
    explained = union_seconds(waits + process_intervals, start, end)
    actions = {}; sections = {}
    for command in commands:
        key = command['script'] + ':' + command['action']
        target = actions.setdefault(key, {'calls': 0, 'wall_ms_sum': 0, 'cpu_ms_sum': 0, 'nonzero_exit_calls': 0})
        target['calls'] += 1
        target['wall_ms_sum'] += command.get('duration_ms', 0)
        target['cpu_ms_sum'] += command.get('cpu_ms', 0)
        target['nonzero_exit_calls'] += int(command.get('exit_code', 0) != 0)
        for item in command.get('sections', []):
            key = item['name'] + (':' + item['phase'] if item.get('phase') else '')
            bucket = sections.setdefault(key, {'calls': 0, 'inclusive_wall_ms_sum': 0})
            bucket['calls'] += 1; bucket['inclusive_wall_ms_sum'] += item['duration_ms']
    attempts = [v for v in read_lines(output / 'validation_history.jsonl') if v.get('status') in {'PASS', 'FAIL', 'ERROR'}]
    return {'schema_version': 1, 'run': run.name, 'scope': 'recorded_journal_window', 'finished': finished,
            'elapsed_seconds': round(duration, 3), 'registered_wait_seconds': round(waited, 3),
            'wait_by_reason_seconds': {k: round(union_seconds(v, start, end), 3) for k, v in reasons.items()},
            'open_waits': open_waits, 'observed_script_wall_union_seconds': round(script_union, 3),
            'unattributed_seconds': round(max(0, duration - explained), 3),
            'instrumented_command_calls': len(commands), 'commands': actions, 'validation_sections': sections,
            'validation_attempts': len(attempts), 'failed_validation_attempts': sum(v['status'] in {'FAIL', 'ERROR'} for v in attempts),
            'framework_version': config.get('framework_version'), 'model_label': config.get('model_label'),
            'benchmark': config.get('benchmark'), 'coverage': 'instrumented_hst_commands' if commands else 'journal_only',
            'limitations': ['Unattributed time includes model work, uninstrumented tools and unrecorded pauses; it is not reasoning time.',
                            'Command wall sums and nested section sums overlap; do not add them to elapsed time.',
                            'Registered waits may overlap other work; they are not proof of whole-executor inactivity.',
                            'Journal timestamps have second precision. The time before the first event is excluded.',
                            'Timers run from script entry to main completion; interpreter startup and the final metric write are excluded. CPU excludes children/servers/LLM.',
                            'Standalone validate_runs is read-only and excluded; its function calls inside finish are timed.',
                            'Only these HST CLIs are measured: ' + ', '.join(INSTRUMENTED)]}


def persist(run, command):
    run = Path(run).resolve(); config_path = run / 'run_config.json'
    if not config_path.is_file(): return
    config = json.loads(config_path.read_text(encoding='utf-8-sig'))
    if config.get('timing_version') != 1: return  # Historical runs stay untouched.
    from run_progress import atomic, lock, output_dir
    output = output_dir(run)
    for name in ['command_metrics.jsonl', 'performance_summary.json']:
        if (output / name).is_symlink(): raise ValueError('Metrics file must not be a symlink')
    with lock(output, name='.metrics.lock'):
        with (output / 'command_metrics.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(command, ensure_ascii=False) + '\n')
        atomic(output / 'performance_summary.json', json.dumps(summarize(run), ensure_ascii=False, indent=2))


def execute(main, script, started, cpu_started):
    argv = sys.argv[1:]; action = argv[0] if argv and not argv[0].startswith('-') else 'validate'
    if action in POLL_ACTIONS or script == 'validate_runs': return main()
    context = {'depth': 0, 'sections': []}
    token = _current.set(context); exit_code = 0
    try:
        result = main()
        if type(result) is int: exit_code = result
        return result
    except BaseException as exc:
        code = getattr(exc, 'code', 1)
        exit_code = code if type(code) is int else 1
        raise
    finally:
        elapsed = time.perf_counter() - started
        cpu = time.process_time() - cpu_started
        ended = datetime.now(timezone.utc)
        _current.reset(token)
        run = argument(argv, '--run-dir')
        if not run and script == 'tui_control':
            workspace, request = argument(argv, '--workspace'), argument(argv, '--request')
            if workspace and request and len(request) == 32 and all(c in '0123456789abcdef' for c in request):
                path = Path(workspace) / '.hst/requests' / request / 'status.json'
                try:
                    value = json.loads(path.read_text(encoding='utf-8-sig'))
                    candidate = (Path(workspace) / value['run_dir']).resolve()
                    if candidate.is_relative_to(Path(workspace).resolve()): run = candidate
                except (OSError, ValueError, KeyError): pass
        if run:
            command = {'schema_version': 1, 'id': uuid.uuid4().hex, 'script': script, 'action': action,
                       'phase': argument(argv, '--phase'), 'origin': os.environ.get('HST_COMMAND_ORIGIN', 'unspecified'),
                       'started_at': (ended - timedelta(seconds=elapsed)).isoformat(), 'ended_at': ended.isoformat(),
                       'duration_ms': round(elapsed * 1000, 3), 'cpu_ms': round(cpu * 1000, 3),
                       'exit_code': exit_code, 'sections': context['sections']}
            try: persist(run, command)
            except (OSError, ValueError, KeyError, TypeError) as exc:
                print('Timing unavailable: ' + str(exc), file=sys.stderr)
