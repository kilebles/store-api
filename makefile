up:
	docker compose up -d
down:
	docker compose down
logs:
	docker compose logs -f
psql:
	docker compose exec db psql -U $$POSTGRES_USER -d $$POSTGRES_DB
migrate:
	docker compose exec backend alembic upgrade head
revision:
	docker compose exec backend alembic revision --autogenerate -m "$(name)"
shell:
	docker compose exec backend bash
restart:
	docker compose restart