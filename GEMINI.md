# Greenhouse Project Mandates

## Tech Stack
- Backend: Python 3.13+, Django 6.x, DRF 3.16.x.
- Frontend: Vue 3 (Composition API), Vite, TypeScript, Tailwind CSS 4.
- State/Routing: Pinia, Vue Router.
- Database: PostgreSQL (Alpine).
- Package Management: uv (Backend), pnpm (Frontend).
- Automation: Makefile.

## Infrastructure
- backend: Django application container (./dockerfiles/Dockerfile.app).
- backend-db: PostgreSQL database container (postgres:alpine).

## Backend Standards
- Authentication: django-rest-knox via CustomAuthentication (token cookie).
- Scoping: Always scope querysets to self.request.user.
- OpenAPI: Mandatory drf-spectacular decorators (@extend_schema).
- Validation: DRF Serializers only.
- Formatting: black (80 chars), isort.
- Linting: ruff, mypy (strict). Use 'make lint-backend'.

## Database Policy
- No manual schema changes.
- No manual creation or editing of migration files.
- Use Django migration system exclusively.

## Frontend Standards
- Component Style: Vue 3 <script setup lang="ts">.
- Routing: Vue Router mandatory.
- State: Pinia stores for global state.
- Data Fetching: @tanstack/vue-query.
- UI: shadcn/ui (reka-ui), Tailwind CSS 4.
- Validation: zod schemas.
- Formatting: prettier.
- Linting: oxlint, eslint. Use 'make lint-frontend'.

## Automation
- make dev-backend / dev-frontend
- make lint-backend / lint-frontend
- make test-backend / test-frontend

## Security
- No committed secrets (.env).
- Protected API endpoints by default.
