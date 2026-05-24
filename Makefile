.PHONY: lint-backend dev-backend test-backend test-frontend clear-dev-backend-db build-backend build-frontend

lint-backend:
	@uv run black --line-length 80 backend
	@uv run isort backend
	@uv run ruff check backend
	@uv run mypy --explicit-package-bases \
		--fast-module-lookup \
		--ignore-missing-imports \
		--strict backend

lint-frontend:
	@pnpm format
	@pnpm lint
	@pnpm build

dev-backend:
	@docker compose up --build --force-recreate

dev-frontend:
	@pnpm dev

test-backend:
	@uv run coverage run --source=backend/greenhouse backend/manage.py test greenhouse
	@uv run coverage report

test-frontend:
	@pnpm test:coverage

REGISTRY ?= localhost
IMAGE_TAG ?= latest

build-backend:
	@docker build \
		-f dockerfiles/Dockerfile.backend \
		-t $(REGISTRY)/greenhouse-backend:$(IMAGE_TAG) \
		.

build-frontend:
	@docker build \
		-f dockerfiles/Dockerfile.frontend \
		-t $(REGISTRY)/greenhouse-frontend:$(IMAGE_TAG) \
		.

clear-dev-backend-db:
	@docker rm -f backend-db
	@docker volume rm greenhouse_backend-db-data


