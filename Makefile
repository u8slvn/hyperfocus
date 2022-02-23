.PHONY: help tests quality coverage coverage-html

.DEFAULT_GOAL := help

help: ## List all the command helps.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

tests: ## Run tests.
	@poetry run pytest tests/ -x -vv

quality: ## Check quality.
	@poetry run flake8 hyperfocus tests
	@poetry run isort --check hyperfocus tests
	@poetry run black --check hyperfocus tests
	@poetry run mypy hyperfocus

format: ## Format files.
	@poetry run isort hyperfocus tests
	@poetry run black hyperfocus tests

coverage: ## Run tests with coverage.
	@poetry run pytest tests/ --cov=hyperfocus

coverage-html: ## Run tests with html output coverage.
	@poetry run pytest tests/ --cov=hyperfocus --cov-report html

ci: quality coverage ## Run CI.
