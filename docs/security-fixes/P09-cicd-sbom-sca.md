# P09 — SBOM & SCA (Dependencies Vulnerability Management)

## C1 (★★) — SBOM — покрытие и автоматизация
- Workflow `.github/workflows/ci-sbom-sca.yml` автоматически генерирует SBOM через Syft (CycloneDX JSON) при push/PR по `**/*.py`, `requirements*.txt` или workflow файлу.
- Результат сохраняется в `EVIDENCE/P09/sbom.json`, метаданные (коммит, run ID, ветка, timestamp) в `EVIDENCE/P09/sbom_metadata.txt`.
- Артефакты загружаются в Actions с именем `P09_EVIDENCE_{run_id}_{sha}`, retention 90 дней.
- Используется фиксированный образ `anchore/syft:latest`, структура EVIDENCE/P09/ описана в PR/README.

## C2 (★★) — SCA — отчёт и сводка по уязвимостям
- SCA выполняется через Grype на основе SBOM, отчёты сохраняются в `EVIDENCE/P09/sca_report.json` и `EVIDENCE/P09/sca_summary.md`.
- В `sca_summary.md` автоматически генерируется статистика по severity и список Critical/High уязвимостей (первые 20) с планом действий.
- При повторном прогоне на том же коммите результаты воспроизводимы (фиксированные Docker образы).

## C3 (★★) — Артефакты и трассировка (Evidence & DS1)
- В `EVIDENCE/P09/` лежат: `sbom.json`, `sbom_metadata.txt`, `sca_report.json`, `sca_summary.md`.
- Все файлы загружаются как артефакт в Actions, доступны через Actions → Artifacts, в PR описании есть ссылки на успешные job.
- Артефакты используются для DS-раздела: документирование зависимостей (SBOM), анализ уязвимостей (SCA), управление рисками (waivers), трассируемость (метаданные с коммитами).

## C4 (★★) — Политика и waivers
- Файл `policy/waivers.yml` содержит структуру для исключений с полями: id, package, version, severity, reason, issue, expires_at, approved_by.
- Политика работы: Critical/High — немедленное внимание, Medium — 30 дней, Low — 90 дней.
- В PR описано, как использовать waivers для документирования принятых рисков при недоступности фиксов.

## C5 (★★) — Интеграция в CI и гигиена
- Workflow триггерится на `workflow_dispatch`, `push` и `pull_request` по релевантным путям, использует `contents: read`, таймаут 15 минут.
- Concurrency настроен (`${{ github.workflow }}-${{ github.ref }}`, `cancel-in-progress: true`), не конфликтует с `ci.yml` из P08.
- Не используются секреты, артефакты загружаются через `actions/upload-artifact@v4`, обработка ошибок через `if: always()`.
