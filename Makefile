.PHONY: format

format:
	.venv/bin/black .
	.venv/bin/isort .
