# Greenhouse

A self-hosted garden management app for tracking crops, varieties, plantings, planting locations, location assignments, and daily observations.

---

## Table of Contents

- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Development Setup](#development-setup)
- [Backend Docker Image](#backend-docker-image)
- [Frontend Docker Image](#frontend-docker-image)
- [Docker Compose (self-hosted)](#docker-compose-self-hosted)
- [Helm (Kubernetes)](#helm-kubernetes)
- [Releases](#releases)
- [API](#api)
- [Features](#features)
- [Code Quality](#code-quality)
- [Database](#database)
- [License](#license)

---

## Tech Stack

| Layer            | Technology                                        |
| ---------------- | ------------------------------------------------- |
| Backend          | Django 6, Django REST Framework, PostgreSQL       |
| Auth             | django-rest-knox (HttpOnly cookie token)          |
| API docs         | drf-spectacular (ReDoc)                           |
| Frontend         | Vue 3, Vite, TypeScript                           |
| UI               | shadcn-vue, reka-ui, Tailwind CSS 4, Tabler Icons |
| State / Data     | Pinia, TanStack Vue Query, TanStack Vue Table     |
| Validation       | Zod                                               |
| Package managers | uv (Python), pnpm (JS)                            |

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

DB_HOST=backend-db
DB_USER=greenhouse
DB_PASSWORD=greenhouse
DB_NAME=greenhouse

TEST_DB_HOST=localhost

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

## Backend Docker Image

### Build

```bash
make build-backend REGISTRY=<your-registry>
```

Omit `REGISTRY` to tag as `localhost/greenhouse-backend:latest`. Use `IMAGE_TAG` to set a version:

```bash
make build-backend REGISTRY=harbor.yourdomain.com/greenhouse IMAGE_TAG=1.0.0
```

### Environment Variables

| Variable                     | Required | Default     | Description                                               |
| ---------------------------- | -------- | ----------- | --------------------------------------------------------- |
| `SECRET_KEY`                 | Yes      | —           | Django secret key                                         |
| `ALLOWED_HOSTS`              | Yes      | —           | Comma-separated list of allowed hosts                     |
| `DB_HOST`                    | Yes      | —           | PostgreSQL host                                           |
| `DB_USER`                    | Yes      | —           | PostgreSQL user                                           |
| `DB_PASSWORD`                | Yes      | —           | PostgreSQL password                                       |
| `DB_NAME`                    | Yes      | —           | PostgreSQL database name                                  |
| `CORS_ALLOWED_ORIGINS`       | Yes      | —           | Comma-separated CORS origins                              |
| `CSRF_TRUSTED_ORIGINS`       | Yes      | —           | Comma-separated CSRF trusted origins                      |
| `SUPERUSER_USERNAME`         | Yes      | —           | Superuser username, created on first startup              |
| `SUPERUSER_EMAIL`            | Yes      | —           | Superuser email, created on first startup                 |
| `SUPERUSER_PASSWORD`         | Yes      | —           | Superuser password, created on first startup              |
| `DEBUG`                      | No       | `False`     | Django debug mode                                         |
| `CSRF_COOKIE_SECURE`         | No       | `False`     | Require HTTPS for CSRF cookie; set `False` for plain HTTP |
| `TEST_DB_HOST`               | No       | `localhost` | PostgreSQL host used by the test runner only              |

### Local Test

Spin up a throwaway Postgres instance and the backend image on a shared network.

**Terminal 1 — network + Postgres:**

```bash
docker network create greenhouse-test

docker run --rm \
  --name greenhouse-db \
  --network greenhouse-test \
  -e POSTGRES_USER=greenhouse \
  -e POSTGRES_PASSWORD=greenhouse_pass \
  -e POSTGRES_DB=greenhouse \
  postgres:alpine
```

**Terminal 2 — backend:**

```bash
docker run --rm \
  --name greenhouse-backend \
  --network greenhouse-test \
  -p 8000:8000 \
  -e DEBUG=True \
  -e SECRET_KEY=test-secret-key \
  -e ALLOWED_HOSTS="0.0.0.0,localhost" \
  -e DB_HOST=greenhouse-db \
  -e DB_USER=greenhouse \
  -e DB_PASSWORD=greenhouse_pass \
  -e DB_NAME=greenhouse \
  -e CORS_ALLOWED_ORIGINS="http://localhost:5173" \
  -e CSRF_TRUSTED_ORIGINS="http://localhost:5173,http://0.0.0.0:8000" \
  -e CSRF_COOKIE_SECURE=False \
  -e SUPERUSER_USERNAME=admin \
  -e SUPERUSER_EMAIL=you@example.com \
  -e SUPERUSER_PASSWORD=yourpassword \
  -e TEST_DB_HOST=localhost \
  localhost/greenhouse-backend:latest
```

Once running, visit:

- `http://localhost:8000/admin/` — Django admin
- `http://localhost:8000/api/v1/docs` — API docs

### Cleanup

```bash
docker network rm greenhouse-test
```

---

## Frontend Docker Image

### Build

```bash
make build-frontend
```

Omit `REGISTRY` to tag as `localhost/greenhouse-frontend:latest`. Use `IMAGE_TAG` to set a version:

```bash
make build-frontend REGISTRY=harbor.yourdomain.com/greenhouse IMAGE_TAG=1.0.0
```

### Environment Variables

| Variable  | Required | Default | Description                                                                               |
| --------- | -------- | ------- | ----------------------------------------------------------------------------------------- |
| `API_URL` | Yes      | —       | Backend API base URL (e.g. `http://localhost:8000/api/v1`); injected at container startup |

### Local Test

Pass `API_URL` at runtime — no rebuild needed per environment.

```bash
docker run --rm -p 3000:80 \
  -e API_URL=http://localhost:8000/api/v1 \
  localhost/greenhouse-frontend:latest
```

Visit `http://localhost:3000`. Verify the config loaded correctly in browser devtools:

```js
window.appConfig // { apiUrl: "http://localhost:8000/api/v1" }
```

---

## Docker Compose (self-hosted)

Use the pre-built GHCR images to run Greenhouse on any machine with Docker — no build step required.

**1. Download the example compose file:**

```bash
curl -O https://raw.githubusercontent.com/twcoo/greenhouse/main/docker-compose.example.yml
```

**2. Create a `.env` file in the same directory:**

```env
DEBUG=True
SECRET_KEY=change-me-use-a-long-random-string

ALLOWED_HOSTS=localhost

DB_HOST=db
DB_USER=greenhouse
DB_PASSWORD=change-me-db-password
DB_NAME=greenhouse

SUPERUSER_USERNAME=admin
SUPERUSER_EMAIL=admin@example.com
SUPERUSER_PASSWORD=change-me-superuser-password

CORS_ALLOWED_ORIGINS=http://localhost:8080
CSRF_COOKIE_SECURE=False
CSRF_TRUSTED_ORIGINS=http://localhost:8080

# Must be the URL the browser can reach — not a docker-internal hostname
API_URL=http://localhost:8000/api/v1
```

**3. Start:**

```bash
docker compose -f docker-compose.example.yml up -d
```

The backend runs on port `8000` and the frontend on port `8080`. Visit `http://localhost:8080`.

---

## Helm (Kubernetes)

The chart lives at `helm/greenhouse/`. It deploys the backend, frontend, and a PostgreSQL database (Bitnami subchart) to a Kubernetes cluster.

### Prerequisites

- [Helm 3](https://helm.sh/docs/intro/install/)
- A Kubernetes cluster with [Longhorn](https://longhorn.io/) for storage
- Images pushed to a container registry accessible by the cluster
- A `harbor-regcred` image pull secret in the target namespace (if using a private registry)
- Gateway API CRDs installed (for HTTPRoute)

### Setup

**1. Copy and edit values:**

```bash
cp helm/greenhouse/values.example.yaml helm/greenhouse/values.yaml
```

Edit `values.yaml` — at minimum update:
- `backend.image.repository` / `frontend.image.repository`
- `backend.config.ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`
- `backend.secret.SECRET_KEY`, `DB_PASSWORD`, `SUPERUSER_*`
- `postgresql.auth.password`
- `frontend.config.API_URL`
- `httproute.host` and `httproute.parentRef` (if enabling HTTPRoute)

**2. Create namespace:**

```bash
kubectl create namespace greenhouse
```

**3. Create image pull secret (if using a private registry):**

```bash
kubectl create secret docker-registry harbor-regcred \
  --namespace greenhouse \
  --docker-server=your-registry \
  --docker-username=<user> \
  --docker-password=<password>
```

**4. Install:**

```bash
helm install greenhouse ./helm/greenhouse --namespace greenhouse
```

### Commands

```bash
# Install
helm install greenhouse ./helm/greenhouse --namespace greenhouse

# Upgrade after values or image changes
helm upgrade greenhouse ./helm/greenhouse --namespace greenhouse

# Force restart all pods (e.g. after pushing a new image)
kubectl rollout restart deployment -n greenhouse

# Uninstall
helm uninstall greenhouse --namespace greenhouse
```

### Build and push images

`REGISTRY` defaults to `localhost`. When `localhost`, the image is built locally and **not pushed**. Provide a real registry to build and push in one step.

```bash
# Build locally (no push)
make build-backend
make build-frontend

# Build + push a versioned tag to a registry (requires docker buildx)
make build-backend REGISTRY=your-registry IMAGE_TAG=v1.2.3
make build-frontend REGISTRY=your-registry IMAGE_TAG=v1.2.3

# Build + push a versioned tag AND also tag/push latest in one command
make build-backend REGISTRY=your-registry IMAGE_TAG=v1.2.3 EXTRA_TAG=latest
make build-frontend REGISTRY=your-registry IMAGE_TAG=v1.2.3 EXTRA_TAG=latest

# Custom platform (default: linux/amd64)
make build-backend REGISTRY=your-registry IMAGE_TAG=v1.2.3 PLATFORM=linux/arm64
```

> Push requires `docker buildx`. Run `docker buildx create --use` if not already set up.

### Values reference

| Key | Description |
|-----|-------------|
| `backend.image.repository` | Backend image repository |
| `backend.image.tag` | Image tag (default: `latest`) |
| `backend.image.pullPolicy` | `Always` recommended with `latest` tag |
| `backend.config.*` | Non-sensitive env vars (ConfigMap) |
| `backend.secret.*` | Sensitive env vars (Secret) |
| `backend.persistence.size` | Media storage PVC size |
| `backend.persistence.storageClassName` | Storage class (default: `longhorn`) |
| `backend.service.mediaPort` | Port for the nginx media sidecar (default: `9000`) |
| `backend.mediaNginx.image` | nginx sidecar image (default: `nginxinc/nginx-unprivileged:alpine`) |
| `backend.mediaNginx.resources` | CPU/memory requests and limits for the nginx sidecar |
| `frontend.image.repository` | Frontend image repository |
| `frontend.config.API_URL` | Backend API base URL seen by the browser |
| `postgresql.enabled` | Deploy bundled PostgreSQL subchart |
| `postgresql.primary.persistence.size` | PostgreSQL PVC size |
| `httproute.enabled` | Create Gateway API HTTPRoute |
| `httproute.host` | Hostname (no `https://` prefix) |
| `httproute.parentRef.name` | Gateway resource name |
| `httproute.parentRef.namespace` | Gateway resource namespace |

> `DB_HOST` is automatically set to `<release-name>-postgresql` when `postgresql.enabled=true` — do not set it manually.

### Media serving

In production (`DEBUG=False`), Django does not serve uploaded media files. The chart handles this with an **nginx sidecar** running inside the backend pod (`nginxinc/nginx-unprivileged:alpine`). It mounts the same media PVC (read-only) and serves `/media/` on port `9000`. The HTTPRoute routes `/media/` traffic directly to the nginx sidecar port — Django is not involved in media delivery.

---

## Releases

Images are published to [GitHub Container Registry (GHCR)](https://ghcr.io/twcoo) via GitHub Actions. A release always produces two tags: the version tag and `latest`.

### Tagging convention

Releases follow [Semantic Versioning](https://semver.org/): `vMAJOR.MINOR.PATCH` (e.g. `v1.2.3`).

### How to release

**Option A — push a git tag (recommended):**

```bash
git tag v1.2.3
git push origin v1.2.3
```

This triggers the `Publish Images` workflow automatically. No manual steps needed.

**Option B — manual workflow dispatch:**

Go to **Actions → Publish Images → Run workflow** and enter the tag (e.g. `v1.2.3`).

### What the CI does

1. Runs backend and frontend lint + tests
2. Builds both images and pushes to GHCR with the version tag
3. Tags and pushes `latest` to GHCR

Images published:

```
ghcr.io/twcoo/greenhouse-backend:v1.2.3
ghcr.io/twcoo/greenhouse-backend:latest
ghcr.io/twcoo/greenhouse-frontend:v1.2.3
ghcr.io/twcoo/greenhouse-frontend:latest
```

### Deploying after a release

Update `values.yaml` with the new tag and upgrade the Helm release:

```bash
helm upgrade greenhouse ./helm/greenhouse --namespace greenhouse \
  --set backend.image.tag=v1.2.3 \
  --set frontend.image.tag=v1.2.3
```

### Mirroring to a private registry (e.g. Harbor)

Use `EXTRA_TAG=latest` to build, push the version tag, and also update `latest` in one command:

```bash
make build-backend REGISTRY=harbor.yourdomain.com/greenhouse IMAGE_TAG=v1.2.3 EXTRA_TAG=latest
make build-frontend REGISTRY=harbor.yourdomain.com/greenhouse IMAGE_TAG=v1.2.3 EXTRA_TAG=latest
```

---

## API

Base URL: `http://localhost:8000/api/v1/`

| Resource                      | Endpoints                                                                                                                |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Auth                          | `POST /auth/login/`, `POST /auth/logout/`                                                                                |
| Setup                         | `GET /setup/status/`, `POST /setup/admin/`                                                                               |
| Crops                         | `GET/POST /crops/`, `GET/PUT/PATCH/DELETE /crops/<id>/`, `PUT /crops/<id>/image/`                                        |
| Varieties                     | `GET/POST /varieties/`, `GET/PUT/PATCH/DELETE /varieties/<id>/`                                                          |
| Planting Locations            | `GET/POST /planting-locations/`, `GET/PUT/PATCH/DELETE /planting-locations/<id>/`                                       |
| Plantings                     | `GET/POST /plantings/`, `GET/PUT/PATCH/DELETE /plantings/<id>/`                                                          |
| Planting Location Assignments | `GET/POST /plantings/<id>/locations/`, `GET/PUT/DELETE /plantings/<id>/locations/<id>/`                                  |
| Planting Daily Observations   | `GET/POST /plantings/<id>/observations/`, `GET/PUT/DELETE /plantings/<id>/observations/<id>/`                            |
| Planting Location Statuses    | `GET/POST /planting-locations/<id>/statuses/`                                                                            |

Interactive API docs (ReDoc): `http://localhost:8000/api/v1/docs`

---

## Features

- **First-run setup wizard** — create an admin account before accessing any routes
- **Crop catalogue** — track crops with scientific name, category, sunlight requirements, days to harvest, and an optional image
- **Variety management** — varieties scoped per crop with growth habit tracking
- **Planting locations** — manage ground beds, pots, and nursery pots with dimensions and an optional image
- **Plantings** — link a crop and variety together; track which planting location they're assigned to over time
- **Location assignments** — assign a planting to a physical location with a start date and optional end date; full history of where each planting has lived
- **Location status tracking** — record status changes for each location (Available, In Use, Damaged, Destroyed, Retired) with optional notes and image; prevents status updates while a location is in use
- **Daily observations** — log comprehensive daily observations per planting: health status, pest pressure, disease symptoms, growth metrics (height, leaf count), environmental readings (temperature, humidity, light hours), soil metrics (moisture, pH, EC), free-text notes, and an optional photo
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
