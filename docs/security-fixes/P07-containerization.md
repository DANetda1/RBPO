# P07 — Контейнеризация и харднинг

## C1 (★★) — Многостадийный Dockerfile
- Билд-стейдж использует `python:3.11-slim`, собирает wheels и гоняет pytest, dev-зависимости не попадают в рантайм.
- Рантайм-стейдж создаёт отдельное venv, копирует только `app`, `alembic`, `alembic.ini`, запускается под пользователем `app`, добавлен `HEALTHCHECK`.
- Проверка размера и слоёв:
  ```
  docker build --target runtime -t secdev-app:local .
  docker history secdev-app:local
  docker images secdev-app:local
  ```

## C3 (★★) — docker compose
- `docker-compose.yml` описывает реальный стек приложения: FastAPI-контейнер + PostgreSQL + именованный volume.
- healthcheck для БД (`pg_isready`) и приложения (`/health`), завязка через `depends_on.condition=service_healthy`.
- Конфигурация не хранит секреты в git: значения берутся из `.env` (см. `env.example`).
- Верификация:
  ```
  cp env.example .env
  docker compose up --build
  docker compose ps
  ```
  Логи `docker compose logs -f app` содержат строку `Application startup complete`.

## C5 (★★) — Контейнеризация собственного сервиса
- В CI (`.github/workflows/ci.yml`) добавлены шаги, которые собирают docker-образ и валидируют compose-файл — интеграция в pipeline.
- Образ использует `uvicorn` entrypoint; сервис доступен по `http://localhost:8000` (см. README).
- Для ручной проверки:
  ```
  docker compose up --build
  curl http://localhost:8000/health
  docker compose down -v
  ```
