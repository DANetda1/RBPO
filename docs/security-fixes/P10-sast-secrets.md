# P10 — SAST & Secrets (Semgrep + Gitleaks)

## C1 (★★) — SAST — Semgrep с SARIF
- Workflow `.github/workflows/ci-sast-secrets.yml` автоматически запускает Semgrep при изменениях в `**/*.py`, `security/semgrep/**`, конфигах.
- Используется профиль `p/ci` и кастомные правила из `security/semgrep/rules.yml` (5 правил под проект: SQL injection, hardcoded secrets, unsafe deserialization, insecure random, unsafe HTML).
- SARIF-отчёт сохраняется в `EVIDENCE/P10/semgrep.sarif`, артефакты загружаются в Actions с именем `P10_EVIDENCE_{run_id}_{sha}`, retention 90 дней.
- Фиксированный образ `returntocorp/semgrep:latest`, результаты воспроизводимы при повторном прогоне.

## C2 (★★) — Сканирование секретов — Gitleaks
- Gitleaks запускается в CI как отдельный шаг workflow, использует конфиг `security/.gitleaks.toml`.
- Отчёт сохраняется в `EVIDENCE/P10/gitleaks.json`, сканируется текущая рабочая копия без истории коммитов.
- В `.gitleaks.toml` настроен allowlist для исключения ложноположительных срабатываний (EVIDENCE/, tests/, docs/, примеры localhost/test секретов).
- При обнаружении реальных секретов в PR описан план действий по их устранению.

## C3 (★★) — Артефакты и документация
- В `EVIDENCE/P10/` лежат: `semgrep.sarif`, `gitleaks.json`.
- Все файлы загружаются как артефакт в Actions, доступны через Actions → Artifacts, в PR описании есть ссылки на успешный job.
- Артефакты используются для DS-раздела: документирование результатов SAST (статический анализ кода), выявление потенциальных уязвимостей, обнаружение секретов, управление рисками безопасности.

## C4 (★★) — Триаж и работа с findings
- В PR или отдельном файле зафиксировано: количество проблем, найденных Semgrep (по severity), наличие реальных секретов по Gitleaks, план действий по критичным находкам.
- Все реальные замечания исправлены (обновлён код/конфиг) или создана Issue/задача с ссылкой на отчёт и описанием причины отложения (backlog) на следующий этап.
- Кастомные правила Semgrep адаптированы под проект Reading List API с учётом используемых технологий (FastAPI, SQLAlchemy, Pydantic).

## C5 (★★) — Интеграция в CI и гигиена
- Workflow триггерится на `workflow_dispatch`, `push` и `pull_request` по релевантным путям (код + security-конфиги), использует `contents: read`, таймаут 15 минут.
- Concurrency настроен (`${{ github.workflow }}-${{ github.ref }}`, `cancel-in-progress: true`), не конфликтует с `ci.yml` из P08 и `ci-sbom-sca.yml` из P09.
- Используется `|| true` для того, чтобы findings не останавливали разработку мгновенно, все шаги выполняются с `if: always()` для сохранения артефактов даже при ошибках.
- Планируется интеграция SARIF с GitHub Code Scanning для автоматического отображения findings в Security tab.
