.PHONY: install run check test lint

install:
	pip install -r requirements.txt
	pip install pytest ruff

run:
	uv run fastapi dev --host 0.0.0.0 --port 8080

check:
	curl -s http://localhost:8080/ping

	pytest -q

lint:
	ruff check .

test_links:
	pytest -q tests/test_links.py

test_pagination:
	pytest -q tests/test_links_pagination.py
