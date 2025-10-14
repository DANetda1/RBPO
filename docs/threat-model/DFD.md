## Контекстная диаграмма (Mermaid)

```mermaid
flowchart LR
  %% Trust Boundaries
  subgraph TB1["Client Boundary"]
    U["User / Client"]
  end

  subgraph TB2["Edge Boundary"]
    G["Reverse Proxy / API Gateway"]
  end

  subgraph TB3["Core Boundary"]
    A["FastAPI App (main.py)"]
    RL["ReadingList Service"]
  end

  subgraph TB4["Data Boundary"]
    S["Storage (In-Memory / DB)"]
    L["Logs / Metrics"]
  end

  %% Flows
  U -- "F1: HTTPS GET/POST" --> G
  G -- "F2: HTTP (internal)" --> A
  A -- "F3: Internal call" --> RL
  RL -- "F4: Read/Write" --> S
  A -- "F5: Errors/Events" --> L
  U -- "F6: CORS Preflight" --> G
  U -- "F7: Auth Headers/JWT?" --> G
  A -- "F8: Response + Security Headers" --> U
```

## Описание модели

Диаграмма отражает потоки данных и границы доверия для сервиса **Reading List API**.

**Уровни и границы доверия:**
- **Client Boundary** — браузер пользователя или фронтенд.
- **Edge Boundary** — обратный прокси или API Gateway, принимает внешние запросы.
- **Core Boundary** — основное приложение FastAPI и сервис управления списками чтения.
- **Data Boundary** — хранилище данных и система логирования/метрик.

**Основные потоки данных (F1–F8):**
| ID | Источник → Приёмник | Канал / Протокол | Описание |
|----|---------------------|------------------|-----------|
| F1 | Клиент → Gateway | HTTPS | Внешний запрос на API |
| F2 | Gateway → FastAPI | HTTP (internal) | Внутренний вызов приложения |
| F3 | FastAPI → Service | Internal call | Обработка бизнес-логики |
| F4 | Service → Storage | Read/Write | Запись/чтение данных |
| F5 | FastAPI → Logs | Internal | Ошибки, события |
| F6 | Клиент → Gateway | HTTPS | CORS preflight |
| F7 | Клиент → Gateway | HTTPS | Аутентификация (JWT Headers) |
| F8 | FastAPI → Клиент | HTTPS | Ответ с безопасными заголовками |
