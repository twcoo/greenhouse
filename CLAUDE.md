# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Development
make dev-backend        # Start Django + PostgreSQL via Docker Compose
make dev-frontend       # Start Vite dev server (http://localhost:5173)

# Linting
make lint-backend       # black (80 chars), isort, ruff, mypy --strict
make lint-frontend      # prettier, oxlint, eslint, build

# Testing
make test-backend       # Django test runner: uv run python backend/manage.py test greenhouse
make test-frontend      # Vitest

# Database
make clear-dev-backend-db  # Destroy and recreate PostgreSQL container + volume

# Production image
make build-backend               # Build backend image tagged localhost/greenhouse-backend:latest
make build-backend REGISTRY=x    # Build with registry prefix
make build-backend IMAGE_TAG=x   # Build with custom tag
```

`make dev-backend` requires a `.env` file at the repo root (consumed by the `backend` container). The `./backend` directory is mounted as a live volume, so code changes are reflected without rebuilding.

To run a single backend test: `uv run python backend/manage.py test greenhouse.tests.TestClassName`

## Architecture

**Monorepo** with a Django REST Framework backend and Vue 3 frontend, managed via Makefile.

### Backend (`backend/`)

- **Models** (`backend/greenhouse/models/`): `Crop`, `Planting`, `PlantingLocation`, `Variety`, `PlantingDailyObservation`, `PlantingGrowthStage`, `PlantingLocationStatus`, `PlantingLocationAssignment`
- **Views** (`backend/greenhouse/views/`): DRF APIViews/generics. All viewsets must use `@extend_schema` decorators for OpenAPI docs and scope querysets to `self.request.user`.
- **Serializers** (`backend/greenhouse/serializers/`): All validation goes through DRF Serializers — no other validation mechanism.
- **Authentication**: django-rest-knox via `CustomAuthentication` — token stored as an HttpOnly cookie.
- **URL structure**: `/api/v1/auth/`, `/api/v1/crops/`, `/api/v1/planting-locations/`, `/api/v1/setup/`
- **OpenAPI docs**: `/api/v1/schema/redoc/`

Database: PostgreSQL only. Never manually create or edit migration files — use Django's migration system exclusively.

### Frontend (`frontend/src/`)

- **API client** (`api/client.ts`): Axios instance with interceptors that auto-convert camelCase ↔ snake_case and inject CSRF tokens. Redirects to `/login` on 401/403.
- **Services** (`api/services/`): One service file per resource (`cropsService`, `plantingLocationService`, `authService`, `setupService`).
- **State** (`stores/`): Pinia stores for auth (`authStore`) and setup (`setupStore`). Use Vue Query (`@tanstack/vue-query`) for server data fetching — Pinia is for client-only global state.
- **Router** (`router/index.ts`): Vue Router with route guards; unauthenticated users redirect to `/login` or `/setup`.
- **Views** (`views/`): Page-level components. Feature components live in `components/crops/` and `components/planting-locations/`.
- **UI**: reka-ui (shadcn/ui port) + Tailwind CSS 4. All components use `<script setup lang="ts">`.
- **Validation**: Zod schemas for all form/request validation.

### Settings (`backend/core/settings.py`)

Do not modify `settings.py`. If a task requires a settings change (e.g. adding a new env var, changing a default, registering an app), stop and tell the user what change is needed and why — let them decide whether to apply it.

### Environment Variables

Backend reads all config via `python-decouple` `config()`. Reference `.env.example` for the full list.

**Required (no default — app will not start without these):**

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts |
| `BACKEND_DB_HOST` | PostgreSQL host |
| `BACKEND_DB_USER` | PostgreSQL user |
| `BACKEND_DB_PASSWORD` | PostgreSQL password |
| `BACKEND_DB_NAME` | PostgreSQL database name |
| `CORS_ALLOWED_ORIGINS` | Comma-separated CORS origins |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated CSRF trusted origins |
| `BACKEND_SUPERUSER_USERNAME` | Superuser username (created on first startup) |
| `BACKEND_SUPERUSER_EMAIL` | Superuser email (created on first startup) |
| `BACKEND_SUPERUSER_PASSWORD` | Superuser password (created on first startup) |

**Optional (have defaults):**

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `False` | Django debug mode |
| `CSRF_COOKIE_SECURE` | `False` | Require HTTPS for CSRF cookie — set `False` on plain HTTP |
| `BACKEND_TEST_DB_HOST` | `localhost` | PostgreSQL host used by test runner only |

### Key Conventions

- All API endpoints require `IsAuthenticated` permission — no public endpoints except `/auth/login/`, `/auth/logout/`, and `/setup/`.
- camelCase/snake_case conversion is handled by the axios interceptors and the `humps` library on the backend serializers — do not manually convert field names in application code.
- Frontend formatting: no semicolons, single quotes (prettier defaults for this project).
- Backend line length: 80 characters.
