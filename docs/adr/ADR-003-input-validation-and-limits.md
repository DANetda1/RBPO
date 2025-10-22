# ADR-003 — Валидация входа и лимиты размеров

## Context
Нужна строгая валидация данных Reading List и лимит размера тела запроса для предотвращения DoS/инъекций.

Связи:
- P03: NFR-2 (лимит размера), NFR-7 (валидация/ошибки).
- P04: DFD F1 (вход), F4 (хранилище); RISKS: R4, R10.

## Decision
1. Pydantic-схемы для элементов Reading List: длины строк, валидация URL (http/https).
2. Middleware: отклонять запросы с `Content-Length > 1MB` кодом **413**.
3. Все отказы в формате RFC 7807 (ADR-001).

## Alternatives
- **Без явной схемы.** +Минимум кода; −Выше риск ошибок и загрязнения хранилища.
- **Сложные WAF-правила.** +Сильнее; −Слишком тяжело для учебной цели.

## Consequences / Security impact
- Снижение поверхности атак, соответствие NFR-2/NFR-7.
- Детерминированные ошибки для клиентов.

## Rollout plan (DoD)
- Схемы и middleware реализованы.
- Тесты: плохой URL → 422/problem+json; большой payload → 413/problem+json.
- CI зелёный; PR содержит ссылки.

## Links
- NFR: NFR-2, NFR-7 (P03)
- DFD: F1, F4 (P04)
- RISKS: R4, R10 (P04)
- Tests: `tests/test_security_p05.py::test_large_payload_returns_413`, `::test_invalid_url_validation`
