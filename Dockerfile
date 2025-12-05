# --- Backend stage ---
FROM python:3.11-slim AS backend

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# --- Frontend stage ---
FROM node:24 AS frontend

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npx build-hexlet-devops-deploy-crud-frontend

# --- Final image ---
FROM python:3.11-slim

WORKDIR /app

# Копируем бэкенд
COPY --from=backend /app /app
# Копируем собранный фронтенд
COPY --from=frontend /app/dist /app/frontend/dist
# Копируем конфиг Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Устанавливаем Nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Переменные окружения для Render
ENV PORT=80

EXPOSE 80

# Запуск Nginx и FastAPI
CMD service nginx start && uvicorn main:app --host 0.0.0.0 --port 8080
