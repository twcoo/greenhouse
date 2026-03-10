.PHONY: lint-backend dev-backend test-backend clear-dev-backend-db

lint-backend:
	@uv run black --line-length 80 .
	@uv run isort .
	@uv run ruff check .
	@uv run mypy --explicit-package-bases \
		--fast-module-lookup \
		--ignore-missing-imports \
		--strict .

lint-frontend:
	@pnpm format
	@pnpm lint
	
dev-backend:
	@docker compose up --build --force-recreate 

dev-frontend:
	@pnpm dev

test-backend:
	@uv run python backend/manage.py test greenhouse

clear-dev-backend-db:
	@docker rm -f greenhouse-db
	@docker volume rm greenhouse_app-db-data


