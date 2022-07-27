test-watch:
	find src tests -name "*.py" | entr venv/bin/python -m pytest src tests -vv

test-cov:
	venv/bin/python -m coverage run -m pytest src tests -vv
	venv/bin/python -m coverage combine
	venv/bin/python -m coverage report --fail-under=100

fmt-watch:
	find src tests -name "*.py" | entr venv/bin/python -m black src tests

types-watch:
	find src tests -name "*.py" | entr venv/bin/python -m mypy src tests

types:
	venv/bin/python -m mypy src tests

install:
	venv/bin/python -m pip uninstall -y yass
	rm -rf build
	rm -rf src/yass.egg-info
	venv/bin/python -m pip install --upgrade ".[dev]"

