.PHONY: format mypy run

format:
	.venv/bin/isort .
	.venv/bin/black .

mypy:
	.venv/bin/mypy .

run:
	.venv/bin/streamlit run main.py
