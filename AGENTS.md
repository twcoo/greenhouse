# AGENTS.md

## Workflow preferences

- Linting, database migrations, and running the backend/frontend test suites are executed **manually by the user**, not by the assistant. Do not run `make lint-backend`, `make lint-frontend`, `make test-backend`, `make test-frontend`, `makemigrations`, or `migrate` unless explicitly asked.
- You may still write code, tests, and generate migration files via `makemigrations` only if the user explicitly requests it.
