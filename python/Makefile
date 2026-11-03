VENV ?= .venv
PYTHON ?= $(VENV)/bin/python
PIP ?= $(VENV)/bin/pip
PYTEST ?= $(VENV)/bin/pytest

.PHONY: all setup test run clean docker-build

all: setup test

$(VENV):
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip --index-url https://pypi.org/simple

setup: $(VENV)
	$(PIP) install -e .[dev] --index-url https://pypi.org/simple

test: setup
	$(PYTEST) -v tests/

run-stdio: setup
	$(PYTHON) -m mcp_server_starter.server --transport stdio

run-http: setup
	$(PYTHON) -m mcp_server_starter.server --transport http --port 8080

docker-build:
	docker build -t mcp-starter-python:latest .

clean:
	rm -rf $(VENV) build dist *.egg-info .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
