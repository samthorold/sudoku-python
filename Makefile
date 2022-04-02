test-watch:
	find . -name "*.py" -not -path "./venv/*" | entr venv/bin/python -m pytest
