FROM python:3.11-slim AS backend

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Сборка фронтенда
FROM node:24 AS frontend
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npx build-hexlet-devops-deploy-crud-frontend

FROM python:3.11-slim

WORKDIR /app

COPY --from=backend /app /app
COPY --from=frontend /app/dist /app/frontend/dist
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

# Устанавливаем необходимые пакеты и запускаем все процессы
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

CMD bash -c "uv run fastapi dev --host 0.0.0.0 --port 8080 & nginx -g 'daemon off;'"
