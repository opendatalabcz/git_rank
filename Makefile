# Variables
SHELL := /usr/bin/env bash
PYTHON := python
PYTHONPATH := `pwd`

# Docker variables
IMAGE := git_rank
VERSION := latest

# Poetry
.PHONY: poetry-download
poetry-download:
	curl -sSL https://install.python-poetry.org | $(PYTHON) -

.PHONY: poetry-remove
poetry-remove:
	curl -sSL https://install.python-poetry.org | $(PYTHON) - --uninstall

# Installation
.PHONY: init
init:
	poetry lock -n && poetry export --without-hashes > requirements.txt
	poetry install -n
	-poetry run mypy --install-types --non-interactive ./

.PHONY: install
install:
	poetry install

.PHONY: pre-commit-install
pre-commit-install:
	poetry run pre-commit install

# Formatters
.PHONY: codestyle
codestyle:
	poetry run pyupgrade --exit-zero-even-if-changed --py39-plus **/*.py
	poetry run isort --settings-path pyproject.toml ./
	poetry run black --config pyproject.toml ./

.PHONY: formatting
formatting: codestyle

# Linting
.PHONY: test
test:
	PYTHONPATH=$(PYTHONPATH) poetry run pytest -c pyproject.toml --cov-report=html --cov=git_rank tests/
	poetry run coverage-badge -o assets/images/coverage.svg -f

.PHONY: check-codestyle
check-codestyle:
	poetry run isort --diff --check-only --settings-path pyproject.toml ./
	poetry run black --diff --check --config pyproject.toml ./
	poetry run darglint --verbosity 2 git_rank tests

.PHONY: mypy
mypy:
	poetry run mypy --config-file pyproject.toml ./

.PHONY: lint
lint: test check-codestyle mypy

# Docker
.PHONY: docker-build
docker-build:
	@echo Building docker $(IMAGE):$(VERSION) ...
	docker build \
		-t $(IMAGE):$(VERSION) . \
		-f ./docker/Dockerfile --no-cache

.PHONY: docker-remove
docker-remove:
	@echo Removing docker $(IMAGE):$(VERSION) ...
	docker rmi -f $(IMAGE):$(VERSION)

# Cleaning
.PHONY: pycache-remove
pycache-remove:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

.PHONY: dsstore-remove
dsstore-remove:
	find . | grep -E ".DS_Store" | xargs rm -rf

.PHONY: mypycache-remove
mypycache-remove:
	find . | grep -E ".mypy_cache" | xargs rm -rf

.PHONY: ipynbcheckpoints-remove
ipynbcheckpoints-remove:
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf

.PHONY: pytestcache-remove
pytestcache-remove:
	find . | grep -E ".pytest_cache" | xargs rm -rf

.PHONY: build-remove
build-remove:
	rm -rf build/

.PHONY: cleanup
cleanup: pycache-remove dsstore-remove mypycache-remove ipynbcheckpoints-remove pytestcache-remove
