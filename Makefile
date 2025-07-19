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
	PYTHONPATH=$(SRC):$(TESTS) pipenv run pytest $(TESTS)

.PHONY: test-all-versions
test-all-versions: ## Run tests across all supported Python versions with pyenv + pipenv
	@for PY in 3.9 3.10 3.11 3.12; do \
		echo "\n>>> Running tests with Python $$PY"; \
		PYTHON_BIN=$$(pyenv prefix $$PY)/bin/python; \
		VENV_DIR=.venv-$$PY; \
		$$PYTHON_BIN -m venv $$VENV_DIR && \
		$$VENV_DIR/bin/pip install --upgrade pip && \
		$$VENV_DIR/bin/pip install pipenv && \
		cd $(PWD) && \
		$$VENV_DIR/bin/pipenv install --dev --deploy && \
		PYTHONPATH=./src:./tests $$VENV_DIR/bin/pipenv run pytest ./tests/unit || exit 1; \
		rm -rf $$VENV_DIR; \
	done

.PHONY: test-version
test-version: ## Run tests with a specific Python version via pyenv + pipenv. Usage: make test-version PY=3.10
	@if [ -z "$(PY)" ]; then \
		echo "❌ PY is required. Usage: make test-version PY=3.10"; exit 1; \
	fi
	PYTHON_BIN=$$(pyenv prefix $(PY))/bin/python; \
	VENV_DIR=.venv-$(PY); \
	$$PYTHON_BIN -m venv $$VENV_DIR && \
	$$VENV_DIR/bin/pip install --upgrade pip && \
	$$VENV_DIR/bin/pip install pipenv && \
	cd $(PWD) && \
	$$VENV_DIR/bin/pipenv install --dev --deploy && \
	PYTHONPATH=./src:./tests $$VENV_DIR/bin/pipenv run pytest ./tests/unit || exit 1; \
	rm -rf $$VENV_DIR

##########################################################################
# DOCS
##########################################################################

.PHONY: sphinx-quickstart
sphinx-quickstart: ## run the sphinx quickstart
	pipenv run docker run -it --rm -v $(PWD)/docs:/docs sphinxdoc/sphinx sphinx-quickstart

.PHONY: sphinx-html
sphinx-html: ## build the sphinx html
	pipenv run make -C docs html

.PHONY: sphinx-rebuild
sphinx-rebuild: ## re-build the sphinx docs
	cd $(DOCS) && \
	pipenv run make clean && pipenv run make html

.PHONY: sphinx-autobuild
sphinx-autobuild: ## activate autobuild of docs
	cd $(DOCS) && \
	pipenv run sphinx-autobuild . _build/html --watch $(SRC)

################################################################################
# RELEASE (LOCALLY)
################################################################################

.PHONY: build
build: ## build the python package
	pipenv run python setup.py sdist bdist_wheel

.PHONY: clean
clean: ## clean the build
	python setup.py clean
	rm -rf build dist
	find . -type f -name '*.py[co]' -delete
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name '*.egg-info' -exec rm -rf {} +

.PHONY: upload-test
upload-test: ## upload package to testpypi repository
	TWINE_USERNAME=$(PYPI_USERNAME_TEST) TWINE_PASSWORD=$(PYPI_PASSWORD_TEST) pipenv run twine upload --repository testpypi --skip-existing --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: upload
upload: ## upload package to pypi repository
	TWINE_USERNAME=$(PYPI_USERNAME) TWINE_PASSWORD=$(PYPI_PASSWORD) pipenv run twine upload --skip-existing dist/*

.PHONY: act-release
act-release: ## Run release workflow locally with act
	@act push --job release -P ubuntu-latest=catthehacker/ubuntu:act-latest

.PHONY: test-install-all-py
test-install-all-py:
	@for PY in 3.9 3.10 3.11 3.12; do \
		echo "\n>>> Testing with Python $$PY"; \
		PYTHON_BIN=$$(pyenv prefix $$PY)/bin/python; \
		VENV_DIR=.venv-$$PY; \
		$$PYTHON_BIN -m venv $$VENV_DIR && \
		$$VENV_DIR/bin/pip install --upgrade pip && \
		$$VENV_DIR/bin/pip install --index-url https://test.pypi.org/simple/ \
		                             --extra-index-url https://pypi.org/simple \
		                             codius && \
		mkdir -p /tmp/test-codius && \
		$$VENV_DIR/bin/codius /tmp/test-codius --version || echo "❌ Failed to run codius with Python $$PY"; \
		rm -rf $$VENV_DIR /tmp/test-codius; \
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
	pipenv run black --line-length 88 $(SRC)

.PHONY: black-check
black-check: ## check code don't violate black formatting rules
	pipenv run black --check --line-length 88 $(SRC)

.PHONY: flake
flake: ## lint code with flake
	pipenv run flake8 --max-line-length=200 $(SRC)

.PHONY: pre-commit-install
pre-commit-install: ## install the pre-commit git hook
	pipenv run pre-commit install

.PHONY: pre-commit-run
pre-commit-run: ## run the pre-commit hooks
	pipenv run pre-commit run --all-files

################################################################################
# PIPENV
################################################################################

.PHONY: pipenv-rm
pipenv-rm: ## remove the virtual environment
	pipenv --rm

.PHONY: pipenv-install
pipenv-install: ## setup the virtual environment
	pipenv install --dev

.PHONY: pipenv-install-package
pipenv-install-package: ## install a package (uses PACKAGE)
	pipenv install $(PACKAGE)

.PHONY: pipenv-install-package-dev
pipenv-install-package-dev: ## install a dev package (uses PACKAGE)
	pipenv install --dev $(PACKAGE)

.PHONY: pipenv-graph
pipenv-graph: ## Check installed packages
	pipenv graph

.PHONY: pipenv-generate-requirements
pipenv-generate-requirements: ## Check a requirements.txt
	pipenv lock -r > requirements.txt

.PHONY: pipenv-shell
pipenv-shell: ## Activate the virtual environment
	pipenv shell

.PHONY: pipenv-venv
pipenv-venv: ## Show the path to the venv
	pipenv --venv

.PHONY: pipenv-lock-and-install
pipenv-lock-and-install: ## Lock the pipfile and install (after updating Pipfile)
	pipenv lock && \
	pipenv install --dev

.PHONY: pipenv-pip-freeze
pipenv-pip-freeze: ## Run pip freeze in the virtual environment
	pipenv run pip freeze

.PHONY: pipenv-sync-setup
pipenv-sync-setup: ## Update install_requires in setup.py from Pipfile
	pipenv run python scripts/sync_setup.py --sync Pipfile setup.py

.PHONY: pipenv-sync-setup-dry-run
pipenv-sync-setup-dry-run: ## Dry run: preview install_requires from Pipfile
	pipenv run python scripts/sync_setup.py --dry-run Pipfile setup.py

.PHONY: pipenv-install-cli-editable
pipenv-install-cli-editable: ## Install the package in editable mode (for CLI use)
	pipenv run pip install -e .

