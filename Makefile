.PHONY: install run test lint typecheck security privacy check docker-build

install:
	python -m pip install -r requirements-dev.txt

run:
	uvicorn app.main:app --reload

test:
	pytest --cov=app --cov-report=term-missing --cov-fail-under=85

lint:
	ruff check app tests scripts
	ruff format --check app tests scripts

typecheck:
	mypy app

security:
	bandit -q -r app
	pip-audit -r requirements.txt

privacy:
	python scripts/privacy_check.py .

check: lint typecheck test security privacy

docker-build:
	docker build -t privacy-devsecops-demo:local .
