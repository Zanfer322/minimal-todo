all: lint test

lint:
	black app tests
	isort app tests
	flake8 app tests
	mypy app tests

test:
	pytest tests --cov=app

.PHONY: all lint test
