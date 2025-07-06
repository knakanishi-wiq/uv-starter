SHELL := /bin/bash

.PHONY: help
help:
	@cat $(MAKEFILE_LIST) | grep -e "^[a-zA-Z0-9_\-]*: *.*## *" | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

TAG ?= uv-starter

setup: ## Setup venv for development
	uv sync --all-groups && \
	pre-commit install

pytest: ## [Unit test] Run all unit tests
	uv run pytest

pytest-integration: ## [Integration test] Run all integration tests
	uv run pytest --runintegration

lint: ## [Linting] Run lint checking across code
	uv run ruff check .
	uv run ruff format --check .

costs:
	npx ccusage@latest
