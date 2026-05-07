.PHONY: install run test seed lint format clean docker-build docker-run

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

seed:
	python seed_data.py

test:
	pytest tests/ -v

lint:
	flake8 app/ tests/
	mypy app/

format:
	black app/ tests/
	isort app/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.db" -delete

docker-build:
	docker build -t uforce-cases-api .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down
