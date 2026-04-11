# AGENTS.md

## Scope

These instructions apply to `apps/api`.

Use the root `AGENTS.md` for repository-wide rules.
Use this file for backend-specific architecture and validation rules.

## Backend Architecture

This application is a Litestar backend.

Preserve and extend the current separation between:
- HTTP layer in `src/app/http`
- domain models in `src/app/domain`
- repositories in `src/app/repositories`
- services in `src/app/services`
- configuration in `src/app/config`
- application wiring in `src/app/asgi.py` and `src/app/cli.py`

Keep wiring explicit.
Do not collapse controllers, services, repositories, and configuration into the same unit.

## Backend Rules

Prefer:
- thin controllers
- explicit dependency wiring
- business rules in services
- persistence concerns in repositories
- domain concepts expressed in domain and service models

Avoid:
- placing business logic in controllers
- mixing HTTP transport concerns with persistence
- bypassing service or repository boundaries without a clear reason
- introducing parallel architectural patterns for the same concern

## Migrations

Treat schema changes as migration work.

Rules:
- represent persistent schema changes through Alembic migrations
- do not hand-wave database changes in code without matching migration intent
- keep migrations aligned with the current backend model behavior

## Legacy Guidance

When backend functionality comes from `reference/bboard`:
- preserve required backend behavior
- preserve domain intent
- do not copy Django-era structure or patterns
- rewrite for clarity, testability, and explicit boundaries

## Validation

For backend changes:
- validate the smallest relevant backend surface
- run backend linting for structural or formatting changes
- run backend tests for behavior changes
- mention any checks that were not run

Behavior-changing backend work should usually include or update tests.
