FROM python:3.11-slim as builder

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv venv && uv pip install --system -r pyproject.toml

COPY . .

RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
RUN apt-get install -y nodejs
RUN npm install @hexlet/project-devops-deploy-crud-frontend

RUN apt-get install -y nginx

COPY nginx.conf /etc/nginx/nginx.conf

RUN cp -r node_modules/@hexlet/project-devops-deploy-crud-frontend/dist/* /var/www/html/

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY --from=builder /app /app

COPY --from=builder /etc/nginx /etc/nginx
COPY --from=builder /var/www/html /var/www/html

RUN apt-get update && apt-get install -y nginx && apt-get clean

EXPOSE 80

CMD ["sh", "-c", "nginx && uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers"]
