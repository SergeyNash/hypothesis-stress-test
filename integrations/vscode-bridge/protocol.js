'use strict';
// This module is independent of VS Code for protocol tests with a faithful Cline API double.
async function processRequest(ctx, id, value, api, log) {
  if (value.state === 'queued') {
    try { value = await ctx.call('bootstrap', id); }
    catch (e) {
      log('Bootstrap failed: ' + e);
      try { await ctx.call('transition', id, ['--event', 'failed', '--message', String(e)]); } catch (error) {log(String(error));}
      return;
    }
  }
  if (value.state === 'prepared') {
    await ctx.call('transition', id, ['--event', 'dispatching', '--message', 'Вызываю публичный API Cline']);
    const prompt = [
      'Запусти полный HST через hst-run для существующего RUN_DIR: ' + value.run_dir,
      'Это явный запуск пользователя из HST TUI, запрос ' + id + '.',
      'Карточка и источники уже сохранены. Не запускай новый intake, не создавай другую папку и не спрашивай источники повторно.',
      'Первым действием подтверди приём через FRAMEWORK_DIR/scripts/tui_control.py: action acknowledge, --workspace KB_ROOT, --request ' + id + '. Разреши FRAMEWORK_DIR через .hst/workspace.json; передавай пути отдельными аргументами, не копируй JSON-экранированные строки в shell.',
      'Затем проверь семантику входа. Неуточнённые сервисные поля не являются фактами; уточни существенные пробелы через TUI.',
      'Все вопросы пользователю (уточнения карточки, полнота материалов, глубина анализа) направляй через tui_control.py ask. После записи вопроса закончи ответ и жди ответа из TUI; не дублируй вопрос в чате.',
      'Перед использованием ответа вызови tui_control.py consume для правильного request/question ID. После consume применяй обычные гейты анализа и подтверждений. Не меняй источники без нового явного выбора пользователя.',
      'Следуй .clinerules/55-tui-control.md. Разрешения инструментов Cline сохраняются. Заверши human_report.html и run_control finish; PASS не доказывает спрос.'
    ].join('\n');
    try {
      // startNewTask may resolve only after agent work; it must not block the workspace heartbeat.
      const pending = api.startNewTask(prompt);
      Promise.resolve(pending).catch(async e => {
        log('Cline launch error: ' + e);
        try { await ctx.call('transition', id, ['--event', 'failed', '--message', String(e)]); } catch (error) { log(String(error)); }
      });
      await ctx.call('transition', id, ['--event', 'dispatched', '--message', 'Запрос передан в Cline; ожидаю подтверждения из задачи']);
    } catch (e) {
      await ctx.call('transition', id, ['--event', 'failed', '--message', String(e)]);
    }
  }
  if (value.state === 'accepted' && value.question?.state === 'answered') {
    const q = value.question;
    try {
      await ctx.call('question-sent', id, ['--question-id', q.id]);
      await api.sendMessage('Ответ пользователя из HST TUI. RUN_DIR: ' + value.run_dir + '\nRequest: ' + id + '\nQuestion: ' + q.id + '\nСначала вызови FRAMEWORK_DIR/scripts/tui_control.py consume --workspace <KB_ROOT> --request ' + id + ' --question-id ' + q.id + ', затем продолжай этот прогон по сохранённому ответу. Не выполняй действия над другой папкой.');
    } catch (e) {
      log('Response delivery error (no automatic duplicate): ' + e);
      await ctx.call('transition', id, ['--event', 'failed', '--message', 'Ошибка доставки ответа: ' + String(e)]);
    }
  }
}
module.exports = {processRequest};
