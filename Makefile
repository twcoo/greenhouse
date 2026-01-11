.PHONY: dev

lint-app:
	@uv run black --line-length 80 .
	@uv run isort .
	@uv run ruff check .
	@uv run mypy --explicit-package-bases \
		--fast-module-lookup \
		--ignore-missing-imports \
		--strict .
	
dev-app:
	@docker compose up --build --force-recreate 
