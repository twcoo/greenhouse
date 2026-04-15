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

### Key Conventions

- All API endpoints require `IsAuthenticated` permission — no public endpoints except `/auth/login/`, `/auth/logout/`, and `/setup/`.
- camelCase/snake_case conversion is handled by the axios interceptors and the `humps` library on the backend serializers — do not manually convert field names in application code.
- Frontend formatting: no semicolons, single quotes (prettier defaults for this project).
- Backend line length: 80 characters.
