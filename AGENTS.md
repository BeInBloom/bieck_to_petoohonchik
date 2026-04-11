# AGENTS.md

## Context

This repository is a rewrite of a legacy bulletin-board system.

Legacy code lives in `reference/`:
- `reference/bboard`: legacy backend
- `reference/bbclient`: legacy frontend

Use `reference/` only as a source of:
- functional behavior
- domain terminology
- user flows
- data relationships

Do not use legacy code as an architectural or stylistic template.

## Execution Mode

Do not write or modify code without explicit user instruction.

By default:
- analyze
- inspect files
- explain findings
- propose changes

If implementation was not clearly requested, do not code.

## Migration Rule

Preserve only required functional behavior from the legacy system.

Do not preserve unless explicitly requested:
- legacy architecture
- legacy structure
- legacy naming
- legacy framework patterns
- legacy UI implementation details
- accidental behavior caused by old technical constraints

Legacy behavior is the reference.
Legacy implementation is not.

## Engineering Principles

All code must be:
- rational
- maintainable
- extensible
- easy to read

Follow:
- `SOLID`
- `KISS`
- `DRY`

Apply them pragmatically:
- prefer simple solutions
- avoid premature abstraction
- remove unnecessary complexity
- keep responsibilities explicit
- design for safe extension

## Code Rules

Write code that reads like instructions.

Classes, methods, and functions must use intention-revealing names.

Prefer:
- small focused functions
- single-purpose classes
- explicit boundaries between HTTP, domain, persistence, and configuration
- readable control flow
- obvious business rules

Avoid:
- vague names like `process`, `handle`, `utils`, `manager`, `misc`
- multi-purpose classes
- mixing transport, business logic, and persistence
- clever abstractions that reduce readability
- copying legacy patterns when a simpler design is available

## Repository Shape

Main applications:
- `apps/api`: Litestar backend
- `apps/web`: SvelteKit frontend

Keep API and web concerns separate.
Do not introduce shared abstractions without a repeated and clear need.

## Validation

Validate the smallest relevant surface area.

Rules:
- add or update tests for behavior changes
- do not leave behavior-changing work unverified
- verify migrated behavior against intended legacy functionality
- state which checks were not run

## Change Strategy

Before non-trivial changes:
- inspect nearby code
- check for existing patterns
- consult `reference/` for migrated functionality

Plan and execute work one concrete step at a time.

Rules:
- choose the next action that can be completed here and now
- do not expand into multi-step future planning unless explicitly requested
- optimize for immediate progress on the current concrete step
- defer later-step design decisions until they become the next active task

When editing:
- make the smallest correct change
- avoid incidental refactors
- do not rewrite unrelated files for style only
- do not add dependencies without clear justification

## Decision Rule

Prefer the solution that is:
1. easier to understand
2. easier to test
3. easier to extend safely
4. more consistent with the existing structure

If `SOLID`, `KISS`, and `DRY` conflict:
- prefer clarity first
- prefer simplicity second
- abstract only when repetition or variation is real

## Completion

Before finishing, state:
- what changed
- whether `reference/` was consulted
- what checks were run
- whether follow-up work or migrations are required
