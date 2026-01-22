.PHONY: lint-app dev test

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

test:
	@uv run python app/manage.py test greenhouse

