VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

PKG_NAME = $(shell grep -A 1 '\[project\]' pyproject.toml | grep 'name' | sed 's/.*=\s*//' | sed 's/"//g')

.PHONY: build check clean develop setup test
.SILENT: check

check:
	if [ -z "$(PKG_NAME)" ]; then \
		echo "Project name could not be found. Please make sure the 'name' field is the first line within the [project] section of your pyproject.toml"; \
		exit 1; \
	fi

build: setup test
	$(PIP) install build
	$(PYTHON) -m build .

develop: check setup
	$(PIP) show $(PKG_NAME) > /dev/null || $(PIP) install -e .

test: check setup requirements-test.txt
	$(PIP) install -r requirements-test.txt
	$(PIP) show $(PKG_NAME) > /dev/null || $(PIP) install -e .
	$(PYTHON) -m unittest discover tests

setup: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	python -m venv $(VENV)
	$(PIP) install -r requirements.txt

clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};
	rm -rf src/*.egg-info
	rm -rf dist
	rm -rf venv
	
