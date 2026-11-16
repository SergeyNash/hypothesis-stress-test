#!/usr/bin/env python3
"""Read-only HST Progress Task. Displays Markdown; never runs or validates research."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import re
import sys
import time


def read_bounded(path, limit=1024*1024):
    if path.is_symlink() or path.stat().st_size > limit:
        raise ValueError('Файл просмотра недоступен или слишком велик')
    return path.read_text(encoding='utf-8-sig')


def selected_run(workspace):
    workspace=Path(workspace).resolve()
    pointer=workspace/'.hst/active-run.md'
    if not pointer.exists():return None
    text=read_bounded(pointer,8192)
    match=re.search(r'^Прогон:\s*(.+?)\s*$',text,re.M)
    if not match:raise ValueError('В active-run.md пока нет строки «Прогон: runs/HYP-…»')
    relative=Path(match[1])
    run=(workspace/relative).resolve()
    if relative.is_absolute() or not run.is_relative_to(workspace) or not re.fullmatch(r'HYP-\d{4}-\d{2}-\d{2}-\d{3}',run.name):
        raise ValueError('Путь выбранного прогона некорректен')
    return run


def stamp(value):
    try:
        date=datetime.fromisoformat(value.replace('Z','+00:00'))
        return date if date.tzinfo else None
    except (ValueError,AttributeError):return None


def elapsed(text, now=None):
    fields=dict(re.findall(r'^(Начало|Окончание|Статус):\s*(.*?)\s*$',text,re.M))
    start=stamp(fields.get('Начало'))
    if not start:return 'Общее время: не указано начало'
    end=stamp(fields.get('Окончание'))
    if fields.get('Статус','').casefold() in {'завершён','завершен','остановлен','отменён','отменен'} and not end:
        return 'Прогон остановлен; время окончания не указано'
    seconds=max(0,int(((end or now or datetime.now(timezone.utc))-start).total_seconds()))
    return f'Общее время: {seconds//3600:02d}:{seconds//60%60:02d}:{seconds%60:02d}'


def view(workspace=None, run_dir=None):
    try:
        run=Path(run_dir).resolve() if run_dir else selected_run(workspace)
        if run is None:return 'HST · Прогресс','Ожидаю новый прогон в чате Cline.',''
        path=run/'progress.md'
        if not path.exists():return run.name,'Ожидаю progress.md. Анализ от просмотра не зависит.',''
        text=read_bounded(path)
        # Strip terminal control sequences. Markdown remains data, never a command.
        text=re.sub(r'\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)|\x1b\[[0-?]*[ -/]*[@-~]','',text)
        text=''.join(c for c in text if c in '\n\t' or (ord(c)>=32 and not 127<=ord(c)<=159))
        return run.name,elapsed(text),text
    except (OSError,ValueError) as error:
        return 'HST · Прогресс','Просмотр временно недоступен. Исследование можно продолжать.',str(error)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    target=p.add_mutually_exclusive_group(required=True)
    target.add_argument('--workspace',type=Path)
    target.add_argument('--run-dir',type=Path)
    p.add_argument('--once',action='store_true')
    args=p.parse_args(argv)
    if args.once or not sys.stdout.isatty():
        title,timer,text=view(args.workspace,args.run_dir)
        print(title+'\n'+timer+'\n\n'+text)
        return
    try:
        from rich.console import Console,Group
        from rich.live import Live
        from rich.markdown import Markdown
        from rich.panel import Panel
    except ImportError:
        print('Для просмотра установи requirements-terminal.txt через setup --terminal.',file=sys.stderr)
        return 2
    console=Console()
    def render():
        title,timer,text=view(args.workspace,args.run_dir)
        return Panel(Group(timer,Markdown(text or 'Ожидаю данные…')),title=title,subtitle='Только чтение · Q не требуется, Ctrl+C закрывает просмотр')
    try:
        with Live(render(),console=console,screen=True,refresh_per_second=1) as live:
            while True:
                time.sleep(1)
                live.update(render())
    except KeyboardInterrupt:pass
    return 0


if __name__=='__main__':raise SystemExit(main())
