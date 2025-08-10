.PHONY: dev lint format test up down run

dev:
	python3 -m venv .venv && . .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt && pre-commit install

lint:
	. .venv/bin/activate && ruff src/ && black --check src/

format:
	. .venv/bin/activate && black src/

test:
	. .venv/bin/activate && pytest -q --tb=short --cov=src --cov-report=html

up:
	docker-compose up -d

down:
	docker-compose down

run:
	. .venv/bin/activate && python -m src.pipelines.run_local
