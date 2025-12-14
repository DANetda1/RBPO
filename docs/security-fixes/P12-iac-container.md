# P12 — IaC & Container Security

## C1 (★★) — Hadolint проверка Dockerfile
- Workflow `.github/workflows/ci-p12-iac-container.yml` запускает Hadolint через Docker-образ `hadolint/hadolint` с конфигурацией из `security/hadolint.yaml`.
- Сканирование выполняется для `Dockerfile` в корне проекта, отчёт сохраняется в `EVIDENCE/P12/hadolint_report.json` в формате JSON.
- Конфигурация `security/hadolint.yaml` настроена под проект, используется формат JSON для машинной обработки результатов.
- Все предупреждения Hadolint проанализированы: Dockerfile использует фиксированные версии образов (`python:3.11-slim`), non-root пользователь (`app`), многоступенчатая сборка для уменьшения размера образа.

## C2 (★★) — Checkov проверка IaC
- Checkov запускается в CI через Docker-образ `bridgecrew/checkov` с конфигурацией из `security/checkov.yaml`.
- Сканирование выполняется для каталога `k8s/` (Kubernetes манифесты: deployment.yaml, service.yaml, secret.yaml), отчёт сохраняется в `EVIDENCE/P12/checkov_report.json`.
- Конфигурация `security/checkov.yaml` настроена для проверки Kubernetes, Dockerfile и docker-compose, используется compact формат вывода.
- Находки Checkov осмысленно отработаны: в Kubernetes манифестах настроен `securityContext` с `runAsNonRoot: true`, ограничены ресурсы контейнеров, используется `ClusterIP` вместо `NodePort` для сервиса.

## C3 (★★) — Trivy проверка образа
- Trivy запускается в CI по собранному образу `app:local` (собирается в том же workflow), отчёт сохраняется в `EVIDENCE/P12/trivy_report.json`.
- Сканирование выполняется через Docker-образ `aquasec/trivy` с форматом JSON, проверяются уязвимости (vuln) и конфигурация (config).
- Критичные и высокие findings разобраны: обновлены базовые образы до актуальных версий, уязвимости в зависимостях отслеживаются через регулярные обновления requirements.txt.
- В описании PR зафиксирован summary по результатам Trivy: количество найденных уязвимостей по уровням критичности, план действий по исправлению.

## C4 (★★) — Меры харднинга Dockerfile и IaC
- В Dockerfile реализованы базовые меры: фиксированная версия базового образа (`python:3.11-slim`), non-root пользователь (`app:app`), многоступенчатая сборка для уменьшения поверхности атаки.
- Дополнительно: контейнер запускается от non-root пользователя с корректной настройкой прав (`USER app`), конфигурация вынесена в переменные окружения, секреты не хардкодятся в образ.
- В IaC (Kubernetes): настроен `securityContext` с `runAsNonRoot: true` и `runAsUser: 1000`, ограничены ресурсы контейнеров (requests/limits), используется `ClusterIP` для внутреннего доступа, секреты хранятся в Kubernetes Secrets.
- Оформлен `hardening_summary.md` в `EVIDENCE/P12/` с описанием применённых мер харднинга до и после проверок.

## C5 (★★) — Интеграция в CI
- Workflow `.github/workflows/ci-p12-iac-container.yml` триггерится на `workflow_dispatch`, `push` по релевантным путям (`Dockerfile`, `iac/**`, `k8s/**`, `docker-compose.yml`, `security/**`), использует `contents: read`, таймаут 30 минут.
- Concurrency настроен (`${{ github.workflow }}-${{ github.ref }}`, `cancel-in-progress: true`), не конфликтует с другими workflows (ci.yml, ci-p11-dast.yml, ci-sast-secrets.yml).
- Все три отчёта (Hadolint, Checkov, Trivy) попадают в `EVIDENCE/P12/` и загружаются как артефакт `P12_EVIDENCE_{run_id}_{sha}` с retention 90 дней.
- Workflow аккуратно вписан в общую схему CI/CD, проверки IaC и контейнеров выполняются при изменении инфраструктуры и Dockerfile.
