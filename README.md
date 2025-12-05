[![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/ci.yml)

# FastAPI ping service

Минимальное FastAPI-приложение.

## Установка

```bash
make install
Запуск
bash
Copy code
make run
# или напрямую
uv run fastapi dev --host 0.0.0.0 --port 8080
Проверка
bash
Copy code
make check
# ожидаемый вывод:
# "pong"

## Деплой

Приложение развёрнуто на Render: https://<YOUR_RENDER_SUBDOMAIN>.onrender.com

### Переменные окружения

- PORT=8080
- DATABASE_URL=<ваш URL базы данных>
- SENTRY_DSN=<ваш DSN для Sentry>
