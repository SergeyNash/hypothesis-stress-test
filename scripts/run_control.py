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

from run_progress import atomic, init, record, NAMES
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


def stamp_viewer(run, url):
    config = load_config(run)
    if config.get('audit_version') == 2:
        config['viewer'] = {'status': 'ready', 'url': url, 'verified_at': datetime.now(timezone.utc).isoformat()}
        save_config(run, config)


def viewer(run):
    import uuid
    state_path = run / 'outputs/.viewer-state.json'
    config = json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {}
    identity = run / 'outputs/.viewer-identity.json'
    if not identity.exists():
        atomic(identity, json.dumps({'token': uuid.uuid4().hex}))
    if config.get('viewer_url'):
        try:
            actual = verify_viewer(config['viewer_url'], run)
            stamp_viewer(run, config['viewer_url'])
            return actual
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
                stamp_viewer(run, url)
                return actual
            if process.poll() is not None:
                break
            time.sleep(.1)
        raise ValueError('viewer did not become ready; use run_progress.py serve in a separate terminal')
    except Exception:
        process.terminate()
        raise


def prepare(run, mode, workspace=None):
    errors = validate_input(run, check_folder_id=True)
    if errors:
        if (run / 'outputs/startup_events.jsonl').is_file():
            record(run, phase='validation', state='error', message='Ошибка входных данных: ' + ', '.join(errors)[:3000])
        raise ValueError(', '.join(errors))
    config = load_config(run)
    if not config and any((run / 'outputs').glob('*.marker')):
        raise ValueError('Legacy run: use viewer/read-only validation; an explicit protocol upgrade is required.')
    if not config:
        config = {'protocol_version': 2, 'audit_version': 2, 'execution_mode': mode, 'language': 'ru',
                  'heavy_analysis': 'ask', 'analysis_choices': [], 'source_selection_version': 1, 'lifecycle_version': 1,
                  'phase_handoff_version': 1}
        save_config(run, config)
        from audit_records import initialize
        initialize(run)
    init(run)
    from run_progress import events
    prior=events(run/'outputs')
    for phase in ['intake', 'validation']:
        last=next((e for e in reversed(prior) if e['kind']=='phase' and e['phase']==phase),None)
        if not last or last['state']!='completed':
            record(run, phase=phase, state='completed', message='Входные данные проверены')
    from active_run import publish
    publish(run, workspace)  # Publish after valid bootstrap, before HTTP startup.
    config=load_config(run);config['viewer']={'status':'starting'};save_config(run,config);init(run)
    try:
        url=viewer(run)
        init(run)
        return url
    except Exception as exc:
        config=load_config(run);config['viewer']={'status':'error','reason':str(exc)};save_config(run,config);init(run)
        raise


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


def write_validation(run, report):
    from run_progress import output_dir
    output=output_dir(run)
    report=dict(report,at=datetime.now(timezone.utc).isoformat(),target=str(run))
    # Persist the latest result even if history/journal recording later fails.
    atomic(output/('run_validation.json' if report['scope']=='run' else 'phase_validation.json'),json.dumps(report,ensure_ascii=False,indent=2))
    with (output/'validation_history.jsonl').open('a',encoding='utf-8') as history:
        history.write(json.dumps(report,ensure_ascii=False)+'\n')
    return report


def complete(run,phase,status='completed'):
    if phase=='human_report':return finish(run)
    from phase_checks import check,require_previous,spec_for,payload
    from run_progress import events
    errors=[]
    try:
        require_previous(run,phase)
        require_entered(run,phase)
        errors=check(run,phase,marker=False,status=status)
    except Exception as exc:
        errors=['PHASE_CHECK_ERROR:'+type(exc).__name__+': '+str(exc)]
    report={'scope':'phase','phase':phase,'status':'FAIL' if errors else 'PASS','errors':errors}
    if errors:
        write_validation(run,report)
        record(run,phase=phase,state='error',message='Проверка этапа не пройдена; см. phase_validation.json')
        return report
    try:
        name,_=spec_for(phase)
        atomic(run/'outputs'/name,json.dumps(payload(phase,status),ensure_ascii=False,indent=2))
        last=next((e for e in reversed(events(run/'outputs')) if e['kind']=='phase' and e['phase']==phase),None)
        if not last or last['state']!='completed':
            record(run,phase=phase,state='completed',message='Этап проверен и завершён: '+NAMES[phase],_transition=True)
    except Exception as exc:
        report.update(status='ERROR',errors=['PHASE_COMMIT_ERROR:'+type(exc).__name__+': '+str(exc)])
    saved=write_validation(run,report)
    if report['status']=='PASS':
        try:auto_enter(run)
        except Exception as exc:
            # The completed phase stays completed; report the failure on the next phase.
            saved['handoff_error']=str(exc)
            next_phase=payload(phase,status)['next_phase']
            try:record(run,phase=next_phase,state='error',message='Не удалось подготовить этап: '+str(exc)[:1000])
            except Exception:pass  # The persisted handoff_error survives a journal failure.
            saved=write_validation(run,saved)
    return saved


def require_entered(run,phase):
    if load_config(run).get('phase_handoff_version')!=1:return
    from run_progress import events
    entries=[e for e in events(run/'outputs') if e['kind']=='phase' and e['phase']==phase]
    invalidated=max((i for i,e in enumerate(entries) if e['state']=='invalidated'),default=-1)
    if not any(e['state']=='running' for e in entries[invalidated+1:]):
        raise ValueError('Phase has no recorded start: '+phase+'; call start BEFORE generating its outputs')


def auto_enter(run):
    """Full-run handoff includes phase preparation, before the model writes outputs."""
    from run_progress import PHASES,events
    config=load_config(run)
    if config.get('tui_request_pending'):return
    if config.get('phase_handoff_version')!=1 or config.get('execution_mode')!='full':return
    if not config.get('source_selection',{}).get('confirmed'):return
    rows=events(run/'outputs')
    for phase in PHASES[2:]:
        last=next((e for e in reversed(rows) if e['kind']=='phase' and e['phase']==phase),None)
        if last and last['state']=='completed':continue
        if last:return  # Preserve errors, inventory waits and invalidations until explicit resume.
        view=config.get('viewer',{})
        if phase=='facilitator' and view.get('status')!='ready' and not (view.get('status')=='unavailable' and view.get('notified')):return
        record(run,phase=phase,state='running',message='Подготовка к этапу: '+NAMES[phase])
        return


def finish(run):
    from phase_checks import enabled,require_previous,payload,spec_for
    run=Path(run).resolve()
    report={'scope':'run','status':'running','errors':[],
            'limitations':'Contracts and source-bound consistency; not source truth, demand or research completeness.'}
    write_validation(run,report)
    try:
        config=load_config(run)
        report['audit_version']=config.get('audit_version',1)
        report['checks']='source-bound consistency and explicit review' if report['audit_version']==2 else 'declared consistency'
        if enabled(run):require_previous(run,'human_report')
        require_entered(run,'human_report')
        errors=check_run(run,pending_human_report=True) if enabled(run) else check_run(run)
        report.update(status='FAIL' if errors else 'PASS',errors=errors)
        if not errors:
            if enabled(run):
                name,_=spec_for('human_report')
                atomic(run/'outputs'/name,json.dumps(payload('human_report'),ensure_ascii=False,indent=2))
            record(run,phase='human_report',state='completed',message='Проверен текущий RUN_DIR: PASS; решение принимает человек',_transition=True)
            p=run/'input/hypothesis.md'
            text=p.read_text(encoding='utf-8-sig')
            text=re.sub(r'(?im)^(\s*[-*]\s+(?:\*\*)?(?:Статус|Status):(?:\*\*)?\s*)(?:\*\*|`)?(?:running|draft|выполняется|в работе)(?:\*\*|`)?\s*$',r'\g<1>completed',text)
            atomic(p,text)
    except Exception as exc:
        report.update(status='ERROR',errors=['COMPLETION_ERROR:'+type(exc).__name__+': '+str(exc)])
    if report['status']!='PASS':
        try:record(run,phase='human_report',state='error',message='Проверка текущего прогона: '+report['status']+'; см. run_validation.json')
        except Exception as exc:report['errors'].append('JOURNAL_WRITE_ERROR:'+str(exc))
    return write_validation(run,report)


def start(run, phase):
    from source_selection import require, COLLECTION_PHASES
    if phase in COLLECTION_PHASES:require(run)
    config = load_config(run)
    if not config:
        url = prepare(run, 'full')
    else:
        init(run)
        view = config.get('viewer', {})
        url = None if view.get('status') == 'unavailable' and view.get('notified') else viewer(run)
    from phase_checks import require_previous
    require_previous(run,phase)
    from run_progress import events
    last=next((e for e in reversed(events(run/'outputs')) if e['kind']=='phase' and e['phase']==phase),None)
    if not last or last['state']!='running':
        record(run, phase=phase, state='running', message='Начат этап: ' + NAMES[phase])
    return url


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['prepare', 'viewer', 'finish', 'analysis-choice', 'require-deep', 'viewer-unavailable', 'start', 'activate', 'sources-options', 'sources-set', 'require-source', 'complete', 'check-phase'])
    p.add_argument('--run-dir', type=Path, required=True)
    p.add_argument('--workspace',type=Path,help='Workspace root for an active-run pointer in a custom run layout')
    p.add_argument('--mode', choices=['full', 'phase'], default='full')
    p.add_argument('--choice', choices=['quick', 'deep', 'skip'])
    p.add_argument('--file', action='append', default=[])
    p.add_argument('--purpose', default='')
    p.add_argument('--reason', default='')
    p.add_argument('--completion-status',choices=['completed','skipped_missing_context'],default='completed')
    for channel in ['local', 'confluence', 'internet']:
        p.add_argument('--'+channel, choices=['yes', 'no'])
    p.add_argument('--local-path', action='append', default=[], help='Allowed local folder relative to workspace; repeatable')
    p.add_argument('--remember', action='store_true', help='Save a proposal for future runs; confirmation still required')
    p.add_argument('--channel', choices=['local', 'confluence', 'internet'])
    p.add_argument('--path', type=Path, help='Local path to check before access')
    from run_progress import PHASES
    p.add_argument('--phase', choices=PHASES)
    a = p.parse_args()
    run = a.run_dir.resolve()
    try:
        if a.action in {'complete','check-phase'}:
            if not a.phase or a.phase in {'intake','validation'}:p.error('Select an output phase with --phase')
            if a.action=='complete':result=complete(run,a.phase,a.completion_status)
            else:
                from phase_checks import check
                try:errors=check(run,a.phase,marker=False,status=a.completion_status)
                except Exception as exc:errors=['PHASE_CHECK_ERROR:'+type(exc).__name__+': '+str(exc)]
                result=write_validation(run,{'scope':'phase','phase':a.phase,'status':'FAIL' if errors else 'PASS','errors':errors})
            print(json.dumps(result,ensure_ascii=False,indent=2))
            return 0 if result['status']=='PASS' else 1
        elif a.action == 'sources-options':
            from source_selection import options
            print(json.dumps(options(run,a.workspace),ensure_ascii=False,indent=2))
        elif a.action == 'sources-set':
            from source_selection import select, CHANNELS
            if any(getattr(a,k) is None for k in CHANNELS):p.error('sources-set requires --local, --confluence and --internet yes/no')
            print(json.dumps(select(run,{k:getattr(a,k)=='yes' for k in CHANNELS},a.local_path,a.workspace,a.remember,a.reason),ensure_ascii=False,indent=2))
        elif a.action == 'require-source':
            from source_selection import require
            if not a.channel:p.error('require-source requires --channel')
            require(run,a.channel,a.path)
            print('Source enabled: '+a.channel)
        elif a.action == 'prepare':
            print(prepare(run, a.mode, a.workspace))
        elif a.action == 'activate':
            from active_run import publish
            errors=validate_input(run,check_folder_id=True)
            if errors:raise ValueError(', '.join(errors))
            pointer=publish(run,a.workspace)
            if pointer is None:raise ValueError('Custom run layout requires --workspace')
            print('Активный прогон: '+run.name)
        elif a.action == 'viewer':
            init(run); print(viewer(run))
        elif a.action == 'start':
            if not a.phase:
                p.error('start requires --phase')
            url = start(run, a.phase)
            print(url or 'Viewer unavailable; reason has been reported to the user.')
        elif a.action == 'viewer-unavailable':
            if not a.reason:
                p.error('record the actual failure explained to the user in --reason')
            config = load_config(run)
            config['viewer'] = {'status': 'unavailable', 'reason': a.reason, 'notified': True}
            save_config(run, config)
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
