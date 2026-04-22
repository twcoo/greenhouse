# Greenhouse

A self-hosted garden management app for tracking crops, varieties, planting locations, and plantings.

> **Note:** This is a development setup only. Not intended for production use.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6, Django REST Framework, PostgreSQL |
| Auth | django-rest-knox (HttpOnly cookie token) |
| API docs | drf-spectacular (ReDoc) |
| Frontend | Vue 3, Vite, TypeScript |
| UI | shadcn-vue, reka-ui, Tailwind CSS 4, Tabler Icons |
| State / Data | Pinia, TanStack Vue Query, TanStack Vue Table |
| Validation | Zod |
| Package managers | uv (Python), pnpm (JS) |

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) + Docker Compose
- [uv](https://docs.astral.sh/uv/) — `pip install uv`
- [pnpm](https://pnpm.io/installation) — `npm install -g pnpm`

---

## Development Setup

### 1. Configure environment variables

Create a `.env` file at the project root. All variables are required:

```env
SECRET_KEY=your-secret-key

ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
CSRF_COOKIE_SECURE=False
CSRF_TRUSTED_ORIGINS=http://localhost:8000

BACKEND_DB_HOST=backend-db
BACKEND_DB_USER=greenhouse
BACKEND_DB_PASSWORD=greenhouse
BACKEND_DB_NAME=greenhouse

BACKEND_TEST_DB_HOST=localhost

API_VERSION=v1
```

### 2. Start the backend

```bash
make dev-backend
```

Starts Django on `http://localhost:8000` and PostgreSQL via Docker Compose. The `./backend` directory is mounted as a live volume — code changes reload automatically. Migrations are applied on first run.

### 3. Start the frontend

```bash
make dev-frontend
```

Starts the Vite dev server on `http://localhost:5173`.

### 4. First-run setup

On first launch, the app will redirect to `/setup` where you create the admin account. This must be completed before any other routes are accessible.

---

## API

Base URL: `http://localhost:8000/api/v1/`

| Resource | Endpoints |
|---|---|
| Auth | `POST /auth/login/`, `POST /auth/logout/` |
| Setup | `GET /setup/status/`, `POST /setup/admin/` |
| Crops | `GET/POST /crops/`, `GET/PUT/PATCH/DELETE /crops/<id>/`, `PUT /crops/<id>/image/` |
| Varieties | `GET/POST /varieties/`, `GET/PUT/PATCH/DELETE /varieties/<id>/` |
| Planting Locations | `GET/POST /planting-locations/`, `GET/PUT/PATCH/DELETE /planting-locations/<id>/`, `PUT /planting-locations/<id>/image/` |
| Plantings | `GET/POST /plantings/`, `GET/PUT/PATCH/DELETE /plantings/<id>/` |

Interactive API docs (ReDoc): `http://localhost:8000/api/v1/docs`

---

## Features

- **First-run setup wizard** — create an admin account before accessing any routes
- **Crop catalogue** — track crops with scientific name, category, sunlight requirements, days to harvest, and an optional image
- **Variety management** — varieties scoped per crop with growth habit tracking
- **Planting locations** — manage ground beds, pots, and nursery pots with dimensions and an optional image
- **Plantings** — link a crop and variety together; track which planting location they're assigned to over time
- **Search** — all list endpoints support full-text search
- **Pagination** — all list endpoints are paginated
- **User isolation** — all data is scoped per authenticated user with no cross-user data leakage

---

## Code Quality

```bash
# Linting
make lint-backend    # black (80 chars), isort, ruff, mypy --strict
make lint-frontend   # prettier, oxlint, eslint, tsc build check

# Testing
make test-backend    # Django test runner + coverage report (≥80% required)
make test-frontend   # Vitest + coverage

# Run a single backend test class
uv run python backend/manage.py test greenhouse.tests.ClassName
```

---

## Database

```bash
# Wipe and recreate the local PostgreSQL container and volume
make clear-dev-backend-db
```

To run migrations manually (when the container is running):

```bash
uv run python backend/manage.py migrate
```

---

## AI Assistance

Parts of this codebase — including feature implementations and test suites — were developed with the assistance of [Claude Code](https://claude.ai/code) by Anthropic. All AI-generated code has been reviewed and integrated by the project author.

---

## License

Licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

Free to use, modify, and self-host. Anyone who distributes or runs a modified version as a service must release their source code under the same license. Commercial use is not permitted without explicit permission from the author.

See the [LICENSE](./LICENSE) file for full terms.
