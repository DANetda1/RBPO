# STRIDE — Reading List API

| Узел/Поток | Угроза | STRIDE | Риск-кейс (кратко) | Контроль | Связанный NFR | Проверка |
|---|---|---|---|---|---|---|
| F1 (HTTPS от клиента) | Подмена источника | Spoofing | Поддельный Origin | CORS allowlist | NFR-4 | pytest/curl |
| F1/F7 | Перехват токена | Tampering/Info Disclosure | Кража/повтор JWT | TTL токена, HTTPS, `secure` куки | NFR-6/NFR-4 | тесты/ревью |
| F2 (Edge→App) | Downgrade/митм внутри сети | Tampering | Неавторизованный доступ к внутреннему API | mTLS/сегментация сети | NFR-5 | ревью/инфраструктура |
| F3 (App→Service) | Эскалация прав | Elevation of Privilege | Неправильные проверки | Валидация входа, схемы | NFR-7 | pytest |
| F4 (Service→Storage) | Неконтролируемая запись | Tampering | Переполнение/инъекция | Валидация, лимиты | NFR-2/NFR-7 | pytest |
| F5 (Ошибки/Логи) | Утечка PII/секретов | Information Disclosure | Секреты в логах | Маскирование/фильтры | NFR-5 | ревью/линтер |
| F6 (CORS Preflight) | Неверный CORS | Repudiation | Разрешение злоумышленного источника | Жёсткий allowlist | NFR-4 | pytest |
| F8 (Ответы клиенту) | Отсутствие sec-заголовков | Tampering | XSS/Clickjacking | Security Headers | NFR-1 | pytest/curl |
| Узел App | Зависимости с CVE | Denial of Service | Уязвимости в пакетах | `pip-audit` в CI | NFR-8 | CI |
| Узел App | Высокая латентность | Denial of Service | p95 выше порога | Оптимизация/профилинг | NFR-6 | нагруз. тест |
