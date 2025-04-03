SHELL := /bin/bash
PY_VERSION := 3.12.4
VENV_NAME := connector

.PHONY: setup pre-setup setup-venv setup-poetry deps shell test run

setup: setup-venv setup-poetry

pre-setup:
	@if ! command -v pyenv >/dev/null 2>&1; then \
		echo "pyenv not found. Installing..."; \
		if [ "$$(uname)" = "Darwin" ]; then \
			brew install pyenv; \
		else \
			apt update && apt install -y curl build-essential libssl-dev zlib1g-dev \
					libbz2-dev libreadline-dev libsqlite3-dev curl git \
					libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev; \
			curl https://pyenv.run | bash; \
			echo -e 'export PYENV_ROOT="${HOME}/.pyenv"' >> ~/.bashrc; \
			echo -e 'export PATH="${HOME}/.pyenv/bin:${PATH}"' >> ~/.bashrc; \
			echo -e 'eval "$$(pyenv init - bash)"\neval "$$(pyenv init --path)"\neval "$$(pyenv init -)"\neval "$$(pyenv virtualenv-init -)"' >> ~/.bashrc; \
			source ~/.bashrc; \
			exec ${SHELL}; \
		fi; \
	else \
		echo "pyenv is already installed."; \
	fi; \

setup-venv:
	pyenv install ${PY_VERSION}
	pyenv virtualenv ${PY_VERSION} ${VENV_NAME}
	pyenv local ${VENV_NAME}
	pyenv rehash

setup-poetry:
	python -m pip install --upgrade pip
	python -m pip install poetry
	pyenv rehash

deps:
	source "$$(poetry env info --path)/bin/activate"
	poetry install --no-root

shell:
	poetry run ipython

test:
	poetry run pytest tests

run:
	poetry run python run.py