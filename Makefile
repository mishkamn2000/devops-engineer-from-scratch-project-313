.PHONY: install test lint run build clean

install:
	uv venv
	uv pip install -r pyproject.toml

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check .

format:
	uv run ruff format .

run:
	uv run fastapi dev --host 0.0.0.0 --port 8080

build:
	docker build -t url-shortener .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
