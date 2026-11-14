"""Explicit per-run channel choices; workspace preferences are proposals, never consent."""
import json
from pathlib import Path
from datetime import datetime, timezone

CHANNELS = {'local': 'Локальная база знаний', 'confluence': 'Confluence', 'internet': 'Интернет'}
OPERATIONS = {'query_started', 'found', 'read', 'used', 'completed', 'no_results', 'partial'}
COLLECTION_PHASES = {'local_evidence', 'business_context', 'market'}


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def config(run):
    path = Path(run)/'run_config.json'
    return read(path) if path.exists() else {}


def workspace_for(run, workspace=None):
    run = Path(run).resolve()
    root = Path(workspace).resolve() if workspace else (run.parent.parent if run.parent.name == 'runs' else None)
    if root is None or not run.is_relative_to(root):
        raise ValueError('Source selection requires --workspace containing RUN_DIR')
    return root


def valid(selection):
    return (isinstance(selection, dict) and selection.get('confirmed') is True
            and isinstance(selection.get('channels'), dict)
            and set(selection['channels']) == set(CHANNELS)
            and all(type(v) is bool for v in selection['channels'].values())
            and isinstance(selection.get('local_paths'), list)
            and all(isinstance(p, str) for p in selection['local_paths'])
            and isinstance(selection.get('workspace'), str))


def options(run, workspace=None):
    c = config(run)
    root = workspace_for(run, workspace)
    path = root/'.hst/source-preferences.json'
    proposed = read(path) if path.is_file() else {'channels': dict.fromkeys(CHANNELS, True), 'local_paths': []}
    return {'current': c.get('source_selection'), 'proposal': proposed, 'confirmation_required': not valid(c.get('source_selection'))}


def require(run, channel=None, path=None):
    c = config(run)
    if c.get('tui_request_pending'):
        raise ValueError('TUI launch has not been acknowledged by Cline')
    if c.get('source_selection_version') != 1:return  # Preserve historical run behavior.
    selected = c.get('source_selection')
    if not valid(selected):
        raise ValueError('Choose sources with the user before collection: run_control.py sources-set')
    if channel is None:return
    if channel not in CHANNELS:raise ValueError('Invalid source channel')
    if not selected['channels'][channel]:
        raise ValueError(channel+' disabled by user; do not call this source')
    if channel == 'local' and path is not None:
        root = Path(selected['workspace']).resolve()
        target = Path(path).resolve()
        allowed = [(root/p).resolve() for p in selected['local_paths']] or [root]
        if not target.is_relative_to(root) or not any(target.is_relative_to(p) and p.is_relative_to(root) for p in allowed):
            raise ValueError('Local path outside user-selected folders')


def select(run, channels, paths, workspace=None, remember=False, reason=''):
    from run_progress import atomic, init, record, events, output_dir
    run = Path(run).resolve();c = config(run)
    if not c:raise ValueError('prepare run first')
    if set(channels) != set(CHANNELS) or any(type(v) is not bool for v in channels.values()):
        raise ValueError('Choose yes/no for all three channels')
    if not reason.strip():raise ValueError('Record the actual user source choice in --reason')
    if c.get('benchmark') and channels != c['benchmark']['channels']:
        raise ValueError('Benchmark source channels are fixed; create a normal run to change them')
    root = workspace_for(run, workspace)
    clean = []
    if paths and not channels['local']:raise ValueError('Local folders require local=yes')
    for p in paths:
        relative = Path(p)
        target = (root/relative).resolve()
        if relative.is_absolute() or not target.is_relative_to(root) or not target.is_dir():
            raise ValueError('Local folders must exist inside the workspace')
        clean.append(target.relative_to(root).as_posix())
    state = root/'.hst'
    preference = state/'source-preferences.json'
    if remember and (state.is_symlink() or preference.is_symlink()):
        raise ValueError('Workspace preferences must not be symlinks')
    selected = {'confirmed': True, 'channels': channels, 'local_paths': clean,
                'workspace': str(root), 'at': datetime.now(timezone.utc).isoformat(), 'reason': reason}
    first_choice=not valid(c.get('source_selection'))
    rows = events(output_dir(run))
    c['source_selection_version'] = 1
    c['source_selection'] = selected
    c.setdefault('source_selection_history', []).append(dict(selected, after_event_id=rows[-1]['id'] if rows else 0))
    atomic(run/'run_config.json', json.dumps(c, ensure_ascii=False, indent=2))
    if remember:
        state.mkdir(exist_ok=True)
        atomic(preference,json.dumps({'channels':channels,'local_paths':clean},ensure_ascii=False,indent=2))
    for channel, enabled in channels.items():
        if not enabled:
            record(run, phase='local_evidence' if channel=='local' else 'business_context',
                   channel=channel, state='declined', message=CHANNELS[channel]+' — отключён пользователем')
    lines = ['# Выбор источников', '', 'Изменение выбора не удаляет ранее собранные данные.', '']
    for item in c['source_selection_history']:
        lines.append('## '+item['at'])
        lines.extend('- '+CHANNELS[k]+(' — включён' if v else ' — отключён пользователем') for k,v in item['channels'].items())
        lines.extend(['- Папки: '+(', '.join(item['local_paths']) or 'вся база при включённом локальном канале'), '- Основание: '+item['reason'], ''])
    atomic(run/'outputs/source_selection.md', '\n'.join(lines))
    init(run)
    if first_choice:
        from run_control import auto_enter
        auto_enter(run)
    return selected


def validate(run):
    c = config(run)
    if 'source_selection_version' not in c:return []
    if c['source_selection_version'] != 1:return ['INVALID_SOURCE_SELECTION_VERSION']
    selected = c.get('source_selection')
    if not valid(selected):return ['MISSING_SOURCE_SELECTION']
    history = c.get('source_selection_history', [])
    if not history or any(not valid(h) or type(h.get('after_event_id')) is not int for h in history):
        return ['INVALID_SOURCE_SELECTION_HISTORY']
    if {k:v for k,v in history[-1].items() if k!='after_event_id'} != selected:
        return ['SOURCE_SELECTION_HISTORY_MISMATCH']
    from run_progress import events
    errors = []
    for e in events(Path(run)/'outputs'):
        if e.get('channel') and e['state'] in OPERATIONS:
            effective = next((h for h in reversed(history) if e['id']>h['after_event_id']), None)
            if effective is None or not effective['channels'].get(e['channel']):
                errors.append('SOURCE_OPERATION_WITHOUT_PERMISSION:'+e['channel'])
    report = Path(run)/'outputs/human_report.html'
    if report.is_file():
        from html import unescape
        import re
        text = re.sub(r'\s+', ' ', unescape(re.sub('<[^>]+>', ' ', report.read_text(encoding='utf-8-sig'))))
        for k,v in selected['channels'].items():
            if not v and CHANNELS[k]+' — отключён пользователем' not in text:
                errors.append('MISSING_SOURCE_LIMITATION:'+k)
    return sorted(set(errors))
