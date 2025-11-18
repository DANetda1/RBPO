# P08 — CI/CD Minimal

## C1 (★★) — Сборка и тесты
- Матрица тестирования: Python 3.11 и 3.12 на `ubuntu-latest`, параллельное выполнение.
- Кэш pip по хэшу `requirements*.txt` и `pyproject.toml`, кэш Docker layers через Buildx.
- Таймауты: 15 минут для тестов, 20 минут для сборки.

## C2 (★★) — Кэширование/конкурренси
- Кэш pip: ключ `${{ runner.os }}-pip-${{ matrix.python-version }}-${{ hashFiles('**/requirements*.txt', '**/pyproject.toml') }}`.
- Кэш Docker: Buildx cache для слоёв образа.
- Concurrency настроен для предотвращения дубликатов запусков.

## C3 (★★) — Секреты и конфиги
- GitHub Secrets: `DATABASE_URL`, `RAILWAY_TOKEN`, `RAILWAY_SERVICE_ID` (опционально).
- Все секреты используются через `${{ secrets.SECRET_NAME }}`, автоматическое маскирование в логах.
- Fallback значения для локального тестирования.

## C4 (★★) — Артефакты/репорты
- JUnit XML отчёты для каждой версии Python (`reports/junit-*.xml`).
- Coverage отчёты (HTML + XML) в `reports/coverage-*/`.
- Docker образ сохраняется как артефакт (`secdev-app-ci.tar.gz`).
- Артефакты доступны в Actions → Artifacts, retention 7 дней (Docker) / 90 дней (reports).

## C5 (★★) — CD/промоушн (эмуляция)
- Деплой на Railway только при push в `main`, после успешного прохождения `test` и `build`.
- Используется Railway CLI, environment `railway-staging` для разграничения окружений.
- Токен хранится в GitHub Secrets, деплой через `railway up`.

## Бонус: Railway деплой (+0.5)
- Проект подключён к Railway, автоматический деплой из ветки `main`.
- URL приложения доступен в Railway dashboard, логи деплоя в Actions.
