Feature: Проверка нефункциональных требований безопасности (NFR)



&nbsp; # NFR-1: Ответы API содержат обязательные security-заголовки

&nbsp; Scenario: Проверка наличия security-заголовков в ответе API

&nbsp;   Given запущено FastAPI-приложение

&nbsp;   When я отправляю GET запрос на "/health"

&nbsp;   Then статус ответа равен 200

&nbsp;   And заголовок "X-Content-Type-Options" равен "nosniff"

&nbsp;   And заголовок "X-Frame-Options" равен "DENY"

&nbsp;   And заголовок "Referrer-Policy" равен "no-referrer"

&nbsp;   And заголовок "Content-Security-Policy" содержит "default-src 'none'"



&nbsp; @negative

&nbsp; # NFR-2: Ограничение размера тела запроса

&nbsp; Scenario: Запрос с телом больше 1 МБ отклоняется

&nbsp;   Given максимальный размер тела запроса установлен в 1 МБ

&nbsp;   When я отправляю POST запрос на "/reading-list" с телом размером больше 1 МБ

&nbsp;   Then сервер возвращает статус 413

&nbsp;   And тело ответа содержит JSON с полем "error.code" равным "payload\_too\_large"



&nbsp; @negative

&nbsp; # NFR-3: Ограничение частоты запросов

&nbsp; Scenario: Превышение лимита частоты запросов вызывает 429

&nbsp;   Given лимит установлен на 10 запросов в секунду с одного IP

&nbsp;   When я отправляю 11 запросов GET на "/health" за 1 секунду

&nbsp;   Then последний ответ возвращает статус 429

&nbsp;   And тело ответа содержит JSON с полем "error.code" равным "rate\_limited"



&nbsp; # NFR-4: Проверка CORS — разрешены только доверенные источники

&nbsp; Scenario: Запрос с недоверенного источника не получает разрешающий CORS-заголовок

&nbsp;   Given разрешен только источник "http://localhost:3000"

&nbsp;   When я отправляю запрос с заголовком Origin "https://evil.example"

&nbsp;   Then статус ответа равен 200

&nbsp;   And в ответе отсутствует заголовок "Access-Control-Allow-Origin"



&nbsp; # NFR-5: Обработка ошибок — всегда JSON-ответ

&nbsp; Scenario: Ошибка 404 возвращается в формате JSON

&nbsp;   Given приложение использует общий обработчик ошибок

&nbsp;   When я запрашиваю несуществующий ресурс "/reading-list/999999"

&nbsp;   Then сервер возвращает статус 404

&nbsp;   And тело ответа содержит JSON с полем "error.code" равным "not\_found"
