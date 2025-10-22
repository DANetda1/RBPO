# ADR-001 — Ошибки RFC 7807 + Correlation ID

## Context
В сервисе Reading List API требуется единый формат ошибок и трассировка запросов. Сейчас ошибки уже нормализуются, но не соответствуют RFC 7807 и нет сквозного correlation_id.

Связи:
- P03 / NFR-7 «Обработка ошибок».
- P04 / DFD: F1 (входящий HTTPS), F8 (ответ клиенту); RISKS: R2, R6.

## Decision
1. Ввести middleware, который проставляет `X-Correlation-ID` (uuid4) в `request.state.correlation_id` и в заголовок ответа.
2. Все ошибки возвращать в формате **application/problem+json** (RFC 7807): поля `type`, `title`, `status`, `detail`, `correlation_id`.
3. Для валидационных/бизнес-ошибок маппинг на проблем-объект.

## Alternatives
- **Оставить текущий произвольный формат.** +Ничего не менять; −Нестандартный контракт, хуже поддержка инструментов.
- **Логи без ID.** +Просто; −Нельзя трассировать цепочку запросов.
- **Вендорный APM-агент.** +Готовая трассировка; −Сложнее/дороже, не требуется сейчас.

## Consequences / Security impact
- Улучшение наблюдаемости и расследования инцидентов (по correlation_id).
- Маскирование деталей ошибок (избегаем утечки стека/секретов).
- Соответствие NFR-7; связь с R2/R6 из модели угроз.

## Rollout plan (DoD)
- Middleware и хендлеры ошибок реализованы.
- Тесты: problem+json, наличие `X-Correlation-ID`.
- CI зелёный.
- PR: p05-secure-coding → main, ссылка на этот ADR.

## Links
- NFR: NFR-7 (P03)
- DFD: F1, F8 (P04)
- RISKS: R2, R6 (P04)
- Tests: `tests/test_security_p05.py::test_problem_json_with_correlation_id`
