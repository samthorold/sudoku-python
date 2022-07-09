test-watch:
	find src tests -name "*.py" | entr venv/bin/python -m pytest src tests -vv

fmt-watch:
	find src tests -name "*.py" | entr venv/bin/python -m black src tests

types-watch:
	find src tests -name "*.py" | entr venv/bin/python -m mypy --no-strict-optional src tests
