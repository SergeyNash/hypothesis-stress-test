# Excerpt custdev — AppSec Lead (2025-03)

Интервьюер: Как вы сейчас решаете, что сканировать первым?

AppSec Lead: Вручную. У нас нет автоматики по business-criticality — кто-то должен вспомнить пометить tier-1. Business-critical apps не идут первыми автоматически.

Интервьюер: Что мешает?

AppSec Lead: Нет единого источника правды о критичности. CISO хочет policy, мы делаем exceptions в Slack. Audit спрашивает «почему этот проект прыгнул в очереди» — ответа формального нет.

Интервьюер: Снизило бы это production risk?

AppSec Lead: Не уверен. Скорее мы быстрее увидим findings в важных репозиториях. Risk в проде — это remediation и ownership, не только порядок скана.
