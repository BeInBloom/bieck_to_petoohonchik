# AGENTS.md

## Scope

These instructions apply to `apps/web`.

Use the root `AGENTS.md` for repository-wide rules.
Use this file for frontend-specific architecture and validation rules.

## Frontend Architecture

This application is a SvelteKit frontend.

Keep responsibilities clear between:
- route files in `src/routes`
- reusable browser or app logic in `src/lib`
- API client code in `src/lib/api`
- auth-related client logic in `src/lib/auth`
- static or content-like frontend assets in `src/lib/content` and `src/lib/assets`

Prefer simple SvelteKit-native solutions.
Keep route and component responsibilities narrow and obvious.

## Frontend Rules

Prefer:
- clear route-driven structure
- small focused components and modules
- straightforward state flow
- simple client code over indirection

Avoid:
- unnecessary client-side complexity
- framework-like abstractions inside the frontend
- mixing unrelated UI, networking, and state concerns in one module
- editing generated SvelteKit output manually

Do not edit:
- `.svelte-kit/*`

## Legacy Guidance

When frontend functionality comes from `reference/bbclient`:
- preserve required user-visible behavior
- preserve UX intent when relevant
- do not copy Angular-era structure or conventions
- rewrite with SvelteKit-native patterns and current project structure

## Validation

For frontend changes:
- validate the smallest relevant frontend surface
- run relevant frontend checks for type, behavior, or build impact
- mention any checks that were not run

Behavior-changing frontend work should usually include or update tests when practical.
