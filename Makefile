.PHONY: install test lint

install:
	pip install -r requirements.txt

test:
	python -m pytest -q

lint:
	python -m ruff check src tests
