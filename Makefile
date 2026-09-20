.PHONY: format mypy

format:
	.venv/bin/black .
	.venv/bin/isort .

mypy:
	mypy .
