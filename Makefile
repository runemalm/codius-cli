##########################################################################
# This is the project's Makefile.
##########################################################################

##########################################################################
# VARIABLES
##########################################################################

HOME := $(shell echo ~)
PWD := $(shell pwd)
SRC := $(PWD)/src
TESTS := $(PWD)/tests
DOCS := $(PWD)/docs

# Load env file
include env.make
export $(shell sed 's/=.*//' env.make)

##########################################################################
# MENU
##########################################################################

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

##########################################################################
# TEST
##########################################################################

.PHONY: test
test: ## run test suite
	PYTHONPATH=$(SRC):$(TESTS) poetry run pytest $(TESTS)

.PHONY: test-all-versions
test-all-versions: ## Run tests across all supported Python versions with pyenv + poetry
	@for PY in 3.9 3.10 3.11 3.12; do \
		echo "\n>>> Running tests with Python $$PY"; \
		PYTHON_BIN=$$(pyenv prefix $$PY)/bin/python; \
		VENV_DIR=.venv-$$PY; \
		$$PYTHON_BIN -m venv $$VENV_DIR && \
		. $$VENV_DIR/bin/activate && \
		pip install --upgrade pip && \
		pip install poetry && \
		poetry install --with dev && \
		PYTHONPATH=./src:./tests poetry run pytest ./tests || exit 1; \
		deactivate && rm -rf $$VENV_DIR; \
	done

.PHONY: test-version
test-version: ## Run tests with a specific Python version via pyenv + poetry. Usage: make test-version PY=3.10
	@if [ -z "$(PY)" ]; then \
		echo "❌ PY is required. Usage: make test-version PY=3.10"; exit 1; \
	fi
	PYTHON_BIN=$$(pyenv prefix $(PY))/bin/python; \
	VENV_DIR=.venv-$(PY); \
	$$PYTHON_BIN -m venv $$VENV_DIR && \
	. $$VENV_DIR/bin/activate && \
	pip install --upgrade pip && \
	pip install poetry && \
	poetry install --with dev && \
	PYTHONPATH=./src:./tests poetry run pytest ./tests || exit 1; \
	deactivate && rm -rf $$VENV_DIR

################################################################################
# RELEASE
################################################################################

.PHONY: build
build: ## build the python package
	poetry build

.PHONY: clean
clean: ## clean the build
	rm -rf build dist
	find . -type f -name '*.py[co]' -delete
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name '*.egg-info' -exec rm -rf {} +

.PHONY: upload-test
upload-test: ## upload package to test.pypi.org
	poetry publish --repository testpypi

.PHONY: upload
upload: ## upload package to PyPI
	poetry publish

.PHONY: act-release
act-release: ## Run release workflow locally with act
	@act push --job release -P ubuntu-latest=catthehacker/ubuntu:act-latest

.PHONY: test-install-all-py
test-install-all-py:
	@for PY in 3.9 3.10 3.11 3.12; do \
		( \
			set -e; \
			echo "\n>>> Testing with Python $$PY"; \
			PYTHON_BIN=$$(pyenv prefix $$PY)/bin/python; \
			VENV_DIR=.venv-$$PY; \
			TRAP_CMD="rm -rf $$VENV_DIR /tmp/test-codius"; \
			trap "$$TRAP_CMD" EXIT; \
			$$PYTHON_BIN -m venv $$VENV_DIR; \
			$$VENV_DIR/bin/pip install --upgrade pip; \
			$$VENV_DIR/bin/pip install --index-url https://test.pypi.org/simple/ \
			                             --extra-index-url https://pypi.org/simple \
			                             codius; \
			mkdir -p /tmp/test-codius; \
			$$VENV_DIR/bin/codius /tmp/test-codius --version; \
		) || exit 1; \
	done

.PHONY: test-install-version
test-install-version: ## Test installing package from TestPyPI with a specific Python version. Usage: make test-install-version PY...
	@if [ -z "$(PY)" ]; then \
		echo "❌ PY is required. Usage: make test-install-version PY=3.10"; exit 1; \
	fi
	PYTHON_BIN=$$(pyenv prefix $(PY))/bin/python; \
	VENV_DIR=.venv-$(PY); \
	$$PYTHON_BIN -m venv $$VENV_DIR && \
	$$VENV_DIR/bin/pip install --upgrade pip && \
	$$VENV_DIR/bin/pip install --index-url https://test.pypi.org/simple/ \
	                             --extra-index-url https://pypi.org/simple \
	                             codius && \
	mkdir -p /tmp/test-codius && \
	$$VENV_DIR/bin/codius /tmp/test-codius --version || echo "❌ Failed to run codius with Python $(PY)"; \
	rm -rf $$VENV_DIR /tmp/test-codius

################################################################################
# PRE-COMMIT HOOKS
################################################################################

.PHONY: black
black: ## format code using black
	poetry run black --line-length 88 $(SRC)

.PHONY: black-check
black-check: ## check code don't violate black formatting rules
	poetry run black --check --line-length 88 $(SRC)

.PHONY: flake
flake: ## lint code with flake
	poetry run flake8 --max-line-length=200 $(SRC)

.PHONY: pre-commit-install
pre-commit-install: ## install the pre-commit git hook
	poetry run pre-commit install

.PHONY: pre-commit-run
pre-commit-run: ## run the pre-commit hooks
	poetry run pre-commit run --all-files

################################################################################
# POETRY
################################################################################

.PHONY: poetry-install-with-dev
poetry-install-with-dev: ## Install all dependencies including dev group
	poetry install --with dev

.PHONY: poetry-env-remove
poetry-env-remove: ## Remove the Poetry virtual environment
	poetry env info --path >/dev/null 2>&1 && poetry env remove python || echo "No Poetry environment found."

.PHONY: poetry-shell
poetry-shell: ## Activate the Poetry virtual environment
	poetry shell

.PHONY: poetry-env-info-path
poetry-env-info-path: ## Show the path to the Poetry virtual environment
	poetry env info --path

.PHONY: poetry-add
poetry-add: ## Install a runtime package (uses PACKAGE)
	@if [ -z "$(PACKAGE)" ]; then \
		echo "❌ PACKAGE is required. Usage: make poetry-add PACKAGE=your-package"; exit 1; \
	fi
	poetry add $(PACKAGE)

.PHONY: poetry-add-dev
poetry-add-dev: ## Install a dev package (uses PACKAGE)
	@if [ -z "$(PACKAGE)" ]; then \
		echo "❌ PACKAGE is required. Usage: make poetry-add-dev PACKAGE=your-package"; exit 1; \
	fi
	poetry add --group dev $(PACKAGE)

.PHONY: poetry-show-tree
poetry-show-tree: ## Show dependency tree
	poetry show --tree

.PHONY: poetry-export-requirements-txt
poetry-export-requirements-txt: ## Export requirements.txt (for Docker or CI)
	poetry export --without-hashes --format=requirements.txt > requirements.txt

.PHONY: poetry-show-codius
poetry-show-codius: ## Show installed details for the codius package
	poetry run pip show -f codius || echo "❌ codius is not installed yet. Run 'make poetry-install'"
