#!/usr/bin/env python3
"""Read-only HST terminal progress viewer. Demo events never touch run artifacts."""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re
import sys
import time

try:
    import click
    from rich.console import Console, Group
    from rich.live import Live
    from rich.panel import Panel
    from rich.progress import Progress, BarColumn, TextColumn
    from rich.table import Table
    from rich.text import Text
except ImportError:
    print('Установите зависимости: python -m pip install -r requirements-terminal.txt', file=sys.stderr)
    raise SystemExit(2)

PHASES = [('intake','Подготовка гипотезы'),('validation','Входные данные'),
          ('facilitator','Стресс-тест ролей'),('local_evidence','Локальные материалы'),
          ('business_context','Бизнес-контекст'),('market','Проверка рынка'),
          ('synthesis','Сопоставление сигналов'),('customer_discovery_planning','План проверки'),
          ('decision_review','Критический разбор'),('human_report','Итоговый отчёт')]
NAMES = dict(PHASES)
LABELS = {'pending':'Ожидает','running':'Выполняется','completed':'Готово',
          'waiting_user':'Нужен ответ','waiting_approval':'Нужно разрешение','error':'Ошибка',
          'invalidated':'Нужно обновить','query_started':'Поиск','found':'Найдено',
          'read':'Прочитано','used':'Использовано','partial':'Частично',
          'unavailable':'Недоступно','auth_error':'Ошибка доступа','declined':'Пропущено',
          'no_results':'Нет результатов'}
COLORS = {'running':'cyan','completed':'green','waiting_user':'yellow','waiting_approval':'yellow',
          'error':'red','auth_error':'red','unavailable':'yellow','invalidated':'yellow'}
CHANNELS = {'local':'Локальные','confluence':'Confluence','internet':'Интернет'}
MSK = timezone(timedelta(hours=3))


def safe(value):
    """Never interpret markup or terminal escapes from run data."""
    text=str(value)
    text=re.sub(r'\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)', '', text)
    text=re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', text)
    return re.sub(r'[\x00-\x1f\x7f-\x9f\u202a-\u202e\u2066-\u2069]', ' ', text)


def stamp(value):
    try:
        parsed=datetime.fromisoformat(value.replace('Z','+00:00'))
        return parsed if parsed.tzinfo is not None else None
    except (ValueError,AttributeError):return None


def event_state(events, run='DEMO · HYP-TEST-001'):
    phases={k:{'id':k,'name':v,'state':'pending','message':''} for k,v in PHASES}
    for e in events:
        if e['kind']=='phase':
            phases[e['phase']].update(state=e['state'],message=e['message'],at=e['at'])
    return {'run':run,'phases':list(phases.values()),'events':events,
            'updated_at':events[-1]['at'] if events else None}


def demo_events(scenario='normal'):
    rows=[]
    def add(phase,state,message,channel=None):
        e={'id':len(rows)+1,'at':datetime.now(timezone.utc).isoformat(),
           'phase':phase,'state':state,'message':message,'kind':'source' if channel else 'phase'}
        if channel:e['channel']=channel;e['query']='Тестовый запрос';e['urls']=[]
        rows.append(e)
        return event_state(list(rows))
    yield event_state([])
    for phase,_ in PHASES:
        yield add(phase,'running','Начинаю этап')
        if phase=='facilitator':
            yield add(phase,'running','Разбираю перспективы заказчика и поставщика · 3 из 5 ролей')
        if phase=='local_evidence':
            yield add(phase,'query_started','Ищу материалы по гипотезе','local')
            yield add(phase,'found','В демонстрации найдено 5 файлов','local')
            yield add(phase,'read','Читаю Excel · лист «Анализ» · файл 2 из 5','local')
            yield add(phase,'waiting_user','Быстро / подробно / пропустить? Требуется выбор глубины анализа')
            if scenario=='waiting':return
            yield add(phase,'running','ДЕМО: смоделирован выбор «быстро», продолжаю')
            yield add(phase,'used','Сохраняю привязки к ячейкам и ограничения извлечения','local')
        if phase=='business_context':
            yield add(phase,'query_started','Ищу контекст сервисного направления','confluence')
            if scenario=='error':
                yield add(phase,'auth_error','ДЕМО: HTTP 401, требуется восстановить доступ','confluence')
                yield add(phase,'waiting_user','Confluence недоступен: восстановить доступ или продолжить с пробелом?')
                return
            yield add(phase,'read','Прочитаны сервисный процесс и каталог','confluence')
            yield add(phase,'query_started','Ищу предложения поддержки и альтернативы','internet')
            yield add(phase,'read','ДЕМО: прочитана страница поставщика','internet')
            yield add(phase,'used','ДЕМО: предложение учтено с ограничениями','internet')
        if phase=='decision_review':
            yield add(phase,'running','Сверяю цифры, периоды, противоречия и условия пилота')
        yield add(phase,'completed','Этап завершён' if phase!='human_report' else 'ДЕМО завершено · исследование не выполнялось')


def validate_state(data):
    if not isinstance(data,dict) or not isinstance(data.get('phases'),list) or not isinstance(data.get('events'),list):
        raise ValueError('Некорректная структура progress.json')
    if not data['phases'] or any(not isinstance(p,dict) or not all(isinstance(p.get(k),str) for k in ['id','name','state']) for p in data['phases']):
        raise ValueError('В журнале нет корректного списка этапов')
    if len({p['id'] for p in data['phases']}) != len(data['phases']):
        raise ValueError('В журнале повторяются этапы')
    if any(not isinstance(e,dict) or not all(isinstance(e.get(k),str) for k in ['kind','phase','state','at','message']) or (e.get('channel') is not None and not isinstance(e['channel'],str)) for e in data['events']):
        raise ValueError('Некорректное событие журнала')
    return data


def read_state(path):
    if path.stat().st_size>16*1024*1024:raise ValueError('Журнал больше 16 МБ; нужен ограниченный просмотр')
    journal=path.with_name('pipeline_events.jsonl')
    if journal.is_file():
        if journal.is_symlink() or journal.stat().st_size>16*1024*1024:raise ValueError('Некорректный или слишком большой журнал')
        from run_progress import snapshot,events
        return validate_state(snapshot(path.parent.parent,events(path.parent)))
    return validate_state(json.loads(path.read_text(encoding='utf-8-sig')))


def html_address(run):
    """Read the URL published by run_control, never guess a port or start a server."""
    if run is None:return None
    try:
        from source_selection import config
        if config(run).get('viewer',{}).get('status') in {'starting','error','unavailable'}:return None
        path=Path(run)/'outputs/.viewer-state.json'
        if path.stat().st_size>16384:return None
        data=json.loads(path.read_text(encoding='utf-8-sig'))
        url=data.get('viewer_url') if isinstance(data,dict) else None
        match=re.fullmatch(r'http://127\.0\.0\.1:([0-9]{1,5})/',url) if isinstance(url,str) else None
        if match and 1<=int(match[1])<=65535:
            return url+'outputs/progress.html'
    except (OSError,ValueError):pass
    return None


def render(data, width=110, height=36, demo=False, issue=None):
    phases=data['phases'];events=data['events']
    names={p['id']:safe(p['name']) for p in phases}
    latest={}
    for i,e in enumerate(events):
        if e['kind']=='phase':latest[e['phase']]=i
    active=[p for p in phases if p['state'] in {'running','waiting_user','waiting_approval','error'}]
    current=max(active,key=lambda p:latest.get(p['id'],-1)) if active else None
    completed=sum(p['state']=='completed' for p in phases)
    finished=completed==len(phases)
    status='Демонстрация завершена' if demo and finished else ('Этапы завершены · см. результат проверки' if finished else 'Ожидание событий')
    if current:status=LABELS.get(current['state'],current['state'])+' · '+safe(current['name'])
    status_color=COLORS.get(current['state'],'white') if current else ('green' if finished else 'dim')
    header=Table.grid(expand=True);header.add_column(ratio=1);header.add_column(justify='right')
    header.add_row(Text('HST  /  ХОД ПРОВЕРКИ',style='bold cyan'),Text(safe(data.get('run','Прогон')),style='bold'))
    header.add_row(Text(status,style=status_color),Text('ДЕМО · синтетические события' if demo else 'Просмотр · только чтение',style='yellow' if demo else 'dim'))
    progress=Progress(TextColumn('Завершено {task.completed:.0f}/{task.total:.0f}'),BarColumn(bar_width=None,style="grey35",complete_style="green",finished_style="green"),TextColumn('{task.percentage:>3.0f}%'),expand=True)
    progress.add_task('',total=len(phases),completed=completed)
    seen=stamp(data.get('updated_at'))
    age=max(0,int((datetime.now(timezone.utc)-seen).total_seconds())) if seen else None
    ago='Событий пока нет' if age is None else f'Последнее событие: {age} с назад · МСК'
    note=Text(ago+'  |  Полоса показывает этапы, не оставшееся время',style='dim')
    action=safe(current.get('message','')) if current else ('Демо ничего не записывает в runs/' if demo else 'Ожидаю данные журнала')
    if current:
        recent=next((e for e in reversed(events) if e['phase']==current['id']),None)
        if recent:action=safe(recent['message'])
    elif issue:
        action=safe(issue)
    alerts=[Text(safe(w),style='yellow') for w in data.get('warnings',[])[:2]]
    if issue and action!=safe(issue):alerts.append(Text(safe(issue),style='bold yellow'))
    if age is not None and age>180 and not finished:
        alerts.append(Text('Давно нет событий. Работа может продолжаться; проверьте Cline.',style='yellow'))
    html=Text('HTML: ',style='dim')
    url=data.get('html_url')
    if url:html.append(url,style='underline cyan link '+url)
    else:
        view=data.get('viewer',{})
        detail='ошибка: '+safe(view.get('reason','не удалось запустить')) if view.get('status') in {'error','unavailable'} else 'запускается' if view.get('status')=='starting' else 'ожидаю адрес HTML-прогресса'
        html.append('недоступен в демо' if demo else detail)
    checked=stamp(data.get('checked_at'))
    polling=Text('Проверка журнала: '+(checked.astimezone(MSK).strftime('%H:%M:%S')+' МСК' if checked else '—')+
                 f' · событий: {len(events)}',style='dim')
    summary=Panel(Group(header,progress,html,polling,note,Text(action,style='white'),*alerts),border_style=status_color,padding=(0,1))
    # Three compact links open the corresponding channel history in the HTML viewer.
    sources=Text('Источники: ',style='dim')
    selection=data.get('source_selection') or {}
    for i,(key,title) in enumerate(CHANNELS.items()):
        if i:sources.append('   ·   ',style='dim')
        enabled=selection.get('channels',{}).get(key)
        style='underline '+('dim' if enabled is False else 'cyan')
        if url:style+=' link '+url+'#source-'+key
        sources.append(title,style=style)
    # Numbered stages follow pipeline order rather than jumping on every update.
    stage_table=Table.grid(expand=True,padding=(0,1))
    columns=2 if width>=100 else 1
    for _ in range(columns):
        stage_table.add_column(ratio=1)
        stage_table.add_column(no_wrap=True)
    items=[]
    for i,p in enumerate(phases):
        is_current=current is not None and p['id']==current['id']
        symbol='▶' if is_current else '✓' if p['state']=='completed' else '·'
        style='bold cyan' if is_current else COLORS.get(p['state'],'dim')
        name=Text(f"{symbol} {i+1:02d}  "+safe(p['name']),style=style)
        label=Text(LABELS.get(p['state'],safe(p['state'])),style=style)
        items.append((name,label))
    for i in range(0,len(items),columns):
        row=[]
        for name,label in items[i:i+columns]:row.extend([name,label])
        while len(row)<columns*2:row.append(Text(''))
        stage_table.add_row(*row)
    stage_panel=Panel(stage_table,title='Этапы · по порядку',border_style='dim',padding=(0,1))
    measuring=Console(width=width)
    def rows_used(content):
        return len(measuring.render_lines(content,measuring.options,pad=False))
    compact=height<20
    # Reserve actual wrapped header/stage heights; do not guess by character count.
    overhead=rows_used(Group(summary,sources,stage_panel))+1
    show_stages=not compact and height-overhead>=7
    if not show_stages:overhead-=rows_used(stage_panel)
    budget=max(1,height-overhead-3) if not compact else max(1,height-13-len(alerts))
    log=Table(box=None,expand=True,padding=(0,1),show_header=True)
    log.add_column('МСК',width=8,no_wrap=True,style='dim')
    log.add_column('Журнал · новые сверху',ratio=1,overflow='fold')
    used=0
    for e in reversed(events):
        date=stamp(e['at']);clock=date.astimezone(MSK).strftime('%H:%M:%S') if date else '—'
        line=Text(LABELS.get(e['state'],safe(e['state']))+' · ',style=COLORS.get(e['state'],'dim'))
        line.append(CHANNELS.get(e.get('channel'),names.get(e['phase'],safe(e['phase'])))+' · ',style='cyan')
        line.append(safe(e['message']))
        wrapped=line.wrap(measuring,max(10,width-16))
        if used+len(wrapped)>budget:
            if used:break
            # A single very long event must leave room for the status and controls.
            line=Text('\n').join(wrapped[:max(1,budget-1)])
            line.append('\n… Полное сообщение — в HTML-журнале.',style='dim')
            log.add_row(clock,line)
            break
        log.add_row(clock,line);used+=len(wrapped)
    if not events:log.add_row('—','Ожидаю события. Счётчик не продвигается сам по себе.')
    body=Group(Panel(log,border_style='dim'),stage_panel) if show_stages else Panel(log,border_style='dim')
    footer=Text('Ctrl+C — закрыть просмотр. Пайплайн продолжит работу.',style='dim')
    if demo:footer=Text('ДЕМО · паузы и ответы смоделированы · Ctrl+C — выход',style='dim')
    if height<20:
        return Group(Text('HST · '+safe(data.get('run','Прогон')),style='bold cyan'),
                     Text('ДЕМО · синтетические события' if demo else 'Только чтение',style='yellow'),
                     Text(status,style=status_color),progress,html,polling,Text(action,overflow='ellipsis',no_wrap=True),
                     *alerts,sources,Panel(log,border_style='dim'),footer)
    return Group(summary,sources,body,footer)


@click.command(context_settings={'help_option_names':['-h','--help']})
@click.option('--run-dir',type=click.Path(path_type=Path,file_okay=False),help='Читать outputs/progress.json существующего прогона.')
@click.option('--workspace',type=click.Path(path_type=Path,file_okay=False,exists=True),help='Ждать активный прогон рабочей папки VS Code.')
@click.option('--demo',is_flag=True,help='Показать демонстрацию без записи файлов (по умолчанию без --workspace/--run-dir).')
@click.option('--scenario',type=click.Choice(['normal','waiting','error']),default='normal',show_default=True)
@click.option('--speed',type=click.FloatRange(min=.1,max=20),default=1.,show_default=True,help='Скорость демонстрации.')
@click.option('--once',is_flag=True,help='Один снимок без обновления, удобно для проверки.')
@click.option('--preview',type=click.Path(path_type=Path,dir_okay=False),help='Экспортировать тестовый снимок в SVG.')
@click.option('--width',type=click.IntRange(60,200),default=None,help='Ширина снимка; живой экран использует размер терминала.')
def main(run_dir,workspace,demo,scenario,speed,once,preview,width):
    """HST: тестовый терминальный просмотр для Windows Terminal и VS Code."""
    if sum(bool(x) for x in [run_dir,workspace,demo])>1:raise click.UsageError('Выберите --demo, --workspace или --run-dir.')
    console=Console(width=width)
    is_demo=run_dir is None and workspace is None
    path=run_dir/'outputs/progress.json' if run_dir else None
    stream=iter(demo_events(scenario)) if is_demo else None
    from active_run import Follow
    follower=Follow(workspace) if workspace else None
    note=None
    state=event_state([],run=run_dir.name if run_dir else 'Новый прогон') if not is_demo else event_state([])
    def get():
        nonlocal note
        if follower:
            value,note,active=follower.poll(read_state)
            snapshot=value if value is not None else event_state([],run=active.name if active else 'Новый прогон')
            return dict(snapshot,html_url=html_address(active),checked_at=datetime.now(timezone.utc).isoformat())
        return next(stream) if stream else dict(read_state(path),html_url=html_address(run_dir),checked_at=datetime.now(timezone.utc).isoformat())
    if once or preview or not console.is_terminal:
        if is_demo:
            states=list(stream)
            state=states[-1] if scenario!='normal' else next(s for s in states if any(e['state']=='read' and e.get('channel')=='local' for e in s['events']))
        else:
            try:state=get()
            except (OSError,ValueError,TypeError,KeyError) as exc:raise click.ClickException(str(exc))
        if preview:
            recording=Console(record=True,width=width or 114)
            recording.print(render(state,width or 114,38,is_demo,note))
            recording.save_svg(str(preview),title='HST · терминальный просмотр')
        else:console.print(render(state,console.size.width,console.size.height,is_demo,note))
        return
    issue=None;finished_demo=False
    try:
        with Live(render(state,console.size.width,console.size.height,is_demo),console=console,screen=True,refresh_per_second=4,vertical_overflow='crop') as live:
            deadline=0.
            while True:
                if time.monotonic()>=deadline and not finished_demo:
                    try:
                        state=get();issue=note
                    except StopIteration:finished_demo=True
                    except (OSError,ValueError,KeyError,TypeError) as exc:issue=str(exc)
                    deadline=time.monotonic()+(1.1/speed if is_demo else 1.)
                live.update(render(state,console.size.width,console.size.height,is_demo,issue))
                time.sleep(.25)
    except KeyboardInterrupt:
        console.print('Демонстрация закрыта.' if is_demo else 'Просмотр закрыт. Файлы прогона не изменены.')


if __name__=='__main__':
    main()
