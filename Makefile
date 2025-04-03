SHELL := /bin/bash
PY_VERSION := 3.12.4
VENV_NAME := connector

.PHONY: setup pre-setup setup-venv setup-poetry deps deps-all shell test run

setup: pre-setup setup-venv setup-poetry deps

pre-setup:
	@if ! command -v pyenv >/dev/null 2>&1; then \
		echo "pyenv not found. Installing..."; \
		if [ "$$(uname)" = "Darwin" ]; then \
			brew install pyenv; \
		else \
			apt update && apt install -y curl build-essential; \
			curl https://pyenv.run | bash; \
			echo -e 'export PYENV_ROOT="$HOME/.pyenv"\nexport PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc; \
			echo -e 'eval "$(pyenv init --path)"\neval "$(pyenv init -)"\neval "$(pyenv virtualenv-init -)"' >> ~/.bashrc; \
		fi; \
	else \
		echo "pyenv is already installed."; \
	fi; \


setup-venv:
	pyenv install ${PY_VERSION}
	pyenv virtualenv ${PY_VERSION} ${VENV_NAME}
	pyenv local ${VENV_NAME}
	pyenv activate
	pyenv rehash

setup-poetry:
	python -m pip install --upgrade pip
	python -m pip install poetry

deps:
	poetry install --only main --sync

deps-all:
	poetry sync

shell:
	poetry run ipython

test:
	poetry run pytest tests

run:
	poetry run python run.py