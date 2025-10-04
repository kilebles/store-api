DC=docker compose

up:
	$(DC) up backend frontend db minio -d

down:
	@if $(DC) ps -q frontend-dev >/dev/null 2>&1 && [ -n "`$(DC) ps -q frontend-dev`" ]; then \
		$(DC) stop frontend-dev; \
	fi; \
	if $(DC) ps -q frontend >/dev/null 2>&1 && [ -n "`$(DC) ps -q frontend`" ]; then \
		$(DC) stop frontend; \
	fi; \
	$(DC) down

build:
	$(DC) build

logs:
	$(DC) logs -f

restart:
	$(DC) restart

psql:
	$(DC) exec db psql -U $${POSTGRES_USER} -d $${POSTGRES_DB}

migrate:
	$(DC) exec backend alembic upgrade head

revision:
	$(DC) exec backend alembic revision --autogenerate -m "$(name)"

shell:
	$(DC) exec backend bash

tree:
	tree -L 3 -I "node_modules|.git|dist|__pycache__"

dev:
	$(DC) up frontend-dev backend db minio -d