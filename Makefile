.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: install-dev
install-dev: install
	pip install -r requirements-dev.txt
	python setup.py develop

.PHONY: lint
lint:
	flake8 chaostoxi/ tests/
	isort --check-only --profile black chaostoxi/ tests/
	black --check --diff chaostoxi/ tests/

.PHONY: format
format:
	isort --profile black chaostoxi/ tests/
	black chaostoxi/ tests/

.PHONY: tests
tests:
	pytest
