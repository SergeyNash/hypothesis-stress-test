---
name: hst-start
description: Start an isolated hypothesis investigation through dialogue and Markdown files, without scripts or machine-readable runtime contracts.
---
# Новый прогон

1. Прими гипотезу в свободной форме. Уточни только существенные пробелы, предложи профиль digital_product/service_business и нужные роли. Сохрани исходную формулировку. Используй conversational-hypothesis-intake и templates/input-schema.md по необходимости.
2. Согласуй источники и глубину; уже сообщённые настройки не спрашивай снова. Для новой гипотезы не читай содержимое других runs. Для свободного ID достаточно имён папок.
3. После ясного разрешения создай RUN_DIR/input/hypothesis.md, run.md и progress.md обычными файловыми инструментами. Перезапись существующего каталога не допускается без отдельного согласования.
4. Запиши .hst/active-run.md для HST Progress Task по 30-run-observability. Это запись Markdown, не запуск Python. Отсутствие монитора не мешает работе.
5. Проверь смысл и полноту входа по инструкции hypothesis-input-validation; если нужно изменить карточку, объясни вариант и спроси. Затем веди hst-run.

Все решения — в чате. Нет TUI, bridge, HTML-прогресса, предварительной инвентаризации всего проекта, CLI-старта и JSON. Для явно указанного RUN_DIR продолжай только его, не создавая новую папку.
