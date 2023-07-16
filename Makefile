.PHONY: help tests tests-tox tests-coverage lint coverage coverage-html ci

.DEFAULT_GOAL := help

help: ## List all the command helps.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

tests: ## Run tests.
	@poetry run pytest tests/ -x -vv
	@poetry run mypy hyperfocus

tests-tox: ## Run tests on all python versions.
	@poetry run tox

tests-coverage: coverage ## Run tests.
	@poetry run mypy hyperfocus

lint: ## Check linter.
	@poetry run pre-commit run --all-files

coverage: ## Run tests with coverage.
	@poetry run pytest tests/ --cov=hyperfocus

coverage-html: ## Run tests with html output coverage.
	@poetry run pytest tests/ --cov=hyperfocus --cov-report html

ci: lint tests-coverage ## Run CI.
