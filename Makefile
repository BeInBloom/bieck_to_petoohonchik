API_DIR := apps/api

.PHONY: fmt lint test hooks-install

fmt:
	cd $(API_DIR) && uv run ruff format .
	cd $(API_DIR) && uv run ruff check --fix .

lint:
	cd $(API_DIR) && uv run ruff format --check .
	cd $(API_DIR) && uv run ruff check .

test:
	cd $(API_DIR) && uv run pytest || test $$? -eq 5

hooks-install:
	git config core.hooksPath .githooks
	chmod +x .githooks/pre-commit .githooks/pre-push
