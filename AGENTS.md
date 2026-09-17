# AGENTS.md

## Workflow preferences

- Linting, type-checking, database migrations, and the backend/frontend test suites are run **manually by the user**, not the assistant. Do not run `make lint-backend`, `make lint-frontend`, `make test-backend`, `make test-frontend`, `makemigrations`, or `migrate` unless explicitly asked.
- You may write code and tests. If a model change needs a migration file, write it by hand (matching the numbering in `backend/greenhouse/migrations/`) or ask the user to run `makemigrations`; never run it yourself.
- If a task requires a change to `backend/core/settings.py`, stop and tell the user what is needed and why instead of editing it.
- Avoid em-dashes (and en-dashes) in prose and copy in this repository, including user-facing strings.

## Commands

- Dev servers: `make dev-backend` (Django + Postgres via Docker Compose; needs a `.env` at repo root, live-mounts `backend/`) and `make dev-frontend` (Vite, http://localhost:5173; needs `frontend/.env` with `VITE_API_URL`).
- Single backend test (Postgres must be running): `uv run python backend/manage.py test greenhouse.tests.<module>.<ClassName>`
- Single frontend test: `pnpm vitest run <path/to/file.spec.ts>`
- CI (`make lint-backend` = black/isort/ruff/mypy `--strict`; `make lint-frontend` = prettier/oxlint/eslint/vue-tsc build) runs before tests. Coverage is enforced: backend >=80%, frontend lines >=80% / functions >=70%.

## Layout

Monorepo: `backend/` (Django 6 + DRF; app is `greenhouse/`, project config is `core/`) and `frontend/` (Vue 3 + Vite + TS). Helm/Docker-image/release details live in `README.md`.

## Backend (`backend/greenhouse/`)

- Per-entity modules: `models/`, `serializers/`, `views/`, `urls/`, and `openapi/<entity>/` (examples/parameters/responses). Adding a resource requires: register the model/serializer/view in their `__init__.py`, add `urls/<entity>.py` and include it in `core/urls.py`, and decorate views with `@extend_schema`/`@extend_schema_view` for the ReDoc schema.
- Responses are wrapped in a JSend envelope `{status, data, message}` by `JSendRenderer`; lists use `StandardResultSetPagination` (`page`/`page_size` → `count`/`results`).
- All views use `IsAuthenticated` and must scope querysets to `request.user`.
- Config is env-driven via `python-decouple`; do not touch `settings.py`.

## Backend tests

- Django `APITestCase`s live in `backend/greenhouse/tests/<entity>.py` (files are *not* named `test_*`). Discovery depends on `tests/__init__.py` re-exporting each class; **add any new test class there or it will silently not run**.
- Shared helpers: `tests/commons/factories.py` (factory-boy) and `tests/commons/mixins.py` (`RequiredAuthTestsMixin`, `ResponseUtilsMixin`).
- Tests use Postgres via `TEST_DB_HOST` (default `localhost:5432`).

## Frontend (`frontend/src/`)

- `@` aliases `frontend/src`. Vue Query handles server data (`composables/`); Pinia is for client-only state (`stores/authStore.ts`, `setupStore.ts`). Zod schemas in `schemas/`, API calls in `api/services/` (one per resource).
- `api/client.ts` axios interceptors auto-convert camelCase<->snake_case via `humps` and expose the JSend `data` as `response.data.data`; do not hand-convert field names.
- Prettier: **no semicolons, double quotes**, 100-char width. ESLint: no TS `enum` (use literal unions or `as const`), no `else`/`else if` (early returns/ternary), PascalCase component names in templates, camelCase props, kebab-case events.
- Tests are `*.spec.ts` under `frontend/src/tests/` mirroring `src/`; Vitest auto-discovers them. `components/ui/` is excluded from lint and coverage.
