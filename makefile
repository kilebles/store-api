up:
	docker compose --env-file ./backend/.env up -d

down:
	docker compose --env-file ./backend/.env down

build:
	docker compose --env-file ./backend/.env build

logs:
	docker compose --env-file ./backend/.env logs -f

restart:
	docker compose --env-file ./backend/.env restart

psql:
	docker compose --env-file ./backend/.env exec db psql -U $${POSTGRES_USER} -d $${POSTGRES_DB}

migrate:
	docker compose --env-file ./backend/.env exec backend alembic upgrade head

revision:
	docker compose --env-file ./backend/.env exec backend alembic revision --autogenerate -m "$(name)"

shell:
	docker compose --env-file ./backend/.env exec backend bash