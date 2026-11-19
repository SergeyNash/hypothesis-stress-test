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
        if run is None:return 'HST · Прогресс','Ожидаю новый прогон в чате Cline.',None
        path=run/'progress.md'
        if not path.exists():return run.name,'Ожидаю progress.md. Анализ от просмотра не зависит.',None
        text=read_bounded(path)
        # Strip terminal control sequences. Markdown remains data, never a command.
        text=re.sub(r'\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)|\x1b\[[0-?]*[ -/]*[@-~]','',text)
        text=''.join(c for c in text if c in '\n\t' or (ord(c)>=32 and not 127<=ord(c)<=159))
        return run.name,elapsed(text),text
    except (OSError,ValueError) as error:
        return 'HST · Прогресс',f'Просмотр временно недоступен. Исследование можно продолжать.\n{error}',None


def progress_lines(text, *, show_bar=False):
    """Read only explicit metadata before the first journal section."""
    if text is None:
        return []
    header = re.split(r'^#{2,6}(?:[ \t]|$)', text, maxsplit=1, flags=re.M)[0]
    counts = re.findall(r'^Завершено этапов:[ \t]*(.*)$', header, re.M)
    stage = re.search(r'^Текущий этап:[ \t]*(.+)$', header, re.M)
    match = re.fullmatch(r'([0-9]{1,9})/([0-9]{1,9})', counts[0].strip()) if len(counts) == 1 else None
    summary = 'Доля этапов пока неизвестна'
    if match:
        done, total = map(int, match.groups())
        if total and done <= total:
            percent = (200 * done + total) // (2 * total)
            summary = f'{done}/{total} · {percent}%'
            if show_bar:
                filled = 8 * done // total
                summary += '  ' + '█' * filled + '░' * (8 - filled)
            summary += '  Общий прогресс'
    lines = [summary]
    if stage and stage[1].strip():
        lines.append('Текущий этап: ' + stage[1].strip())
    return lines


def render_panel(title, timer, text):
    from rich.console import Group
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.text import Text

    lines = [Text(line) for line in progress_lines(text, show_bar=True)]
    return Panel(Group(*lines, Text(timer), Markdown(text or 'Ожидаю данные…')),
                 title=Text(title), subtitle='Только чтение · Ctrl+C закрывает просмотр')


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    target=p.add_mutually_exclusive_group(required=True)
    target.add_argument('--workspace',type=Path)
    target.add_argument('--run-dir',type=Path)
    p.add_argument('--once',action='store_true')
    args=p.parse_args(argv)
    if args.once or not sys.stdout.isatty():
        title,timer,text=view(args.workspace,args.run_dir)
        print('\n'.join([title, *progress_lines(text), timer, '', text or '']))
        return
    try:
        from rich.console import Console
        from rich.live import Live
    except ImportError:
        print('Для просмотра установи requirements-terminal.txt через setup --terminal.',file=sys.stderr)
        return 2
    console=Console()
    def render():
        return render_panel(*view(args.workspace, args.run_dir))
    try:
        with Live(render(),console=console,screen=True,vertical_overflow="crop",refresh_per_second=1) as live:
            while True:
                time.sleep(1)
                live.update(render())
    except KeyboardInterrupt:pass
    return 0


if __name__=='__main__':raise SystemExit(main())
