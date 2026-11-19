from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from terminal_progress import elapsed,selected_run,view


class MarkdownProgress(unittest.TestCase):
    def test_observer_never_changes_files_and_renders_partial_markdown(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);run=root/'runs/HYP-2026-11-16-001';run.mkdir(parents=True)
            (root/'.hst').mkdir();(root/'.hst/active-run.md').write_text('# Active\nПрогон: runs/HYP-2026-11-16-001\n',encoding='utf-8')
            path=run/'progress.md';path.write_text('# Работа\nНачало: 2026-11-16T09:00:00+03:00\nСтатус: выполняется\n\nЧитаю материал\n| незавершённая таблица',encoding='utf-8')
            before={p.relative_to(root):p.read_bytes() for p in root.rglob('*') if p.is_file()}
            title,timer,text=view(workspace=root)
            self.assertEqual(run.name,title);self.assertIn('Читаю',text)
            self.assertEqual(before,{p.relative_to(root):p.read_bytes() for p in root.rglob('*') if p.is_file()})
            result=subprocess.run([sys.executable,str(ROOT/'scripts/terminal_progress.py'),'--workspace',str(root),'--once'],capture_output=True,encoding='utf-8')
            self.assertEqual(0,result.returncode);self.assertIn('Читаю',result.stdout)

    def test_no_latest_run_guessing_and_missing_note_is_not_pipeline_failure(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);(root/'runs/HYP-2026-11-16-001').mkdir(parents=True)
            self.assertIsNone(selected_run(root));self.assertIn('Ожидаю',view(workspace=root)[1])
            (root/'.hst').mkdir();(root/'.hst/active-run.md').write_text('Прогон: runs/HYP-2026-11-16-001',encoding='utf-8')
            self.assertIn('Ожидаю progress.md',view(workspace=root)[1])

    def test_timer_restores_and_freezes_from_markdown(self):
        now=datetime(2026,11,16,7,0,tzinfo=timezone.utc)
        text='Начало: 2026-11-16T09:00:00+03:00\nСтатус: выполняется'
        self.assertEqual('Общее время: 01:00:00',elapsed(text,now))
        text+='\nОкончание: 2026-11-16T09:25:30+03:00\nСтатус: завершён'
        self.assertEqual('Общее время: 00:25:30',elapsed(text,now))
        self.assertIn('не указано',elapsed('Начало: неизвестно',now))

    def test_traversal_and_terminal_escapes_are_not_executed_or_displayed(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);state=root/'.hst';state.mkdir()
            (state/'active-run.md').write_text('Прогон: ../HYP-2026-11-16-001',encoding='utf-8')
            with self.assertRaises(ValueError):selected_run(root)
            run=root/'runs/HYP-2026-11-16-001';run.mkdir(parents=True)
            (run/'progress.md').write_text('\x1b[31mhello\x1b[0m',encoding='utf-8')
            self.assertEqual('hello',view(run_dir=run)[2])

    def test_stage_progress_through_once_and_run_switch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pointer = root / '.hst/active-run.md'
            pointer.parent.mkdir()
            for step, stage, percent, status in [
                (0, '1. Роли', 0, 'выполняется'),
                (3, '4. Рынок', 38, 'выполняется'),
                (3, '4. Рынок', 38, 'ожидание ответа'),
                (4, '5. Синтез', 50, 'выполняется'),
                (5, '6. План проверки', 63, 'остановлен'),
                (7, '8. Итог', 88, 'сохранён Markdown'),
                (8, '8. Итог', 100, 'завершён'),
            ]:
                with self.subTest(step=step, status=status):
                    run = root / f'runs/HYP-2026-11-19-{step:03d}'
                    run.mkdir(parents=True, exist_ok=True)
                    pointer.write_text(f'Прогон: {run.relative_to(root)}', encoding='utf-8')
                    note = (f'# Ход проверки\nСтатус: {status}\nЗавершено этапов: {step}/8\n'
                            f'Текущий этап: {stage}\n\n## Сейчас\nПояснение\n')
                    (run / 'progress.md').write_text(note, encoding='utf-8')
                    output = subprocess.check_output(
                        [sys.executable, str(ROOT/'scripts/terminal_progress.py'),
                         '--workspace', str(root), '--once'], encoding='utf-8')
                    header, body = output.split('# Ход проверки')
                    self.assertIn(f'{step}/8 · {percent}%', header)
                    self.assertIn(stage, header)
                    self.assertIn(status, body)
                    self.assertIn('Пояснение', body)

    def test_unknown_counts_and_journal_entries(self):
        from terminal_progress import progress_lines

        for value in ['', '3/', '/8', '3/0', '9/8', '-1/8', '3/8?', '3/8\nЗавершено этапов: 4/8']:
            with self.subTest(value=value):
                note = f'Завершено этапов: {value}\n\n## Выполнено\nЗавершено этапов: 3/8'
                self.assertEqual(['Доля этапов пока неизвестна'], progress_lines(note))
        self.assertEqual(['Доля этапов пока неизвестна'], progress_lines('# Старая заметка'))
        self.assertEqual([], progress_lines(None))

    def test_narrow_live_screen_keeps_progress_without_colour(self):
        try:
            from rich.console import Console
            from rich.live_render import LiveRender
        except ImportError:
            self.skipTest('Rich is optional for --once')
        from terminal_progress import render_panel

        note = 'Завершено этапов: 3/8\nТекущий этап: 4. Рынок\n## Сейчас\n' + 'Событие\n\n' * 100
        console = Console(width=32, height=12, color_system=None)
        with console.capture() as frame:
            console.print(LiveRender(render_panel('Прогон', 'Таймер', note), vertical_overflow='crop'))
        screen = frame.get()
        for label in ['3/8 · 38%', '███░░░░░', 'Рынок', 'Таймер']:
            self.assertIn(label, screen)
        self.assertLessEqual(len(screen.splitlines()), 12)
