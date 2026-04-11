API_DIR := apps/api
WEB_DIR := apps/web
API_TYPES_DIR := packages/api-types
OPENAPI_SCHEMA := $(API_TYPES_DIR)/openapi.json

.PHONY: fmt lint test \
	api-fmt api-lint api-test api-dev api-openapi \
	types-generate \
	web-install web-dev web-check web-build web-test \
	hooks-install

fmt: api-fmt

lint: api-lint

test: api-test

api-fmt:
	cd $(API_DIR) && uv run ruff format .
	cd $(API_DIR) && uv run ruff check --fix .

api-lint:
	cd $(API_DIR) && uv run ruff format --check .
	cd $(API_DIR) && uv run ruff check .

api-test:
	cd $(API_DIR) && uv run pytest || test $$? -eq 5

api-dev:
	cd $(API_DIR) && uv run api-dev

api-openapi:
	cd $(API_DIR) && uv run python scripts/export_openapi.py ../../$(OPENAPI_SCHEMA)

types-generate: api-openapi
	bun run --filter @pets/api-types generate

web-install:
	bun install

web-dev:
	bun run --filter @pets/web dev

web-check:
	bun run --filter @pets/web check

web-build:
	bun run --filter @pets/web build

web-test:
	bun run --filter @pets/web test

hooks-install:
	git config core.hooksPath .githooks
	chmod +x .githooks/pre-commit .githooks/pre-push
