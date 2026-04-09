.PHONY: lint-backend dev-backend test-backend clear-dev-backend-db

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
	@uv run python backend/manage.py test greenhouse

test-frontend:
	@pnpm test

clear-dev-backend-db:
	@docker rm -f backend-db
	@docker volume rm greenhouse_backend-db-data


