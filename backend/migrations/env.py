import os
from dotenv import load_dotenv

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from src.core.db import Base
import src.apps  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    # важно: заменить asyncpg на psycopg2 для alembic
    sync_url = DATABASE_URL.replace("asyncpg", "psycopg2")
    config.set_main_option("sqlalchemy.url", sync_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


def run_migrations() -> None:
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()


run_migrations()