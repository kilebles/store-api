import os
from dotenv import load_dotenv

from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

from src.core.db import Base
import src.apps  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

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


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn,
                target_metadata=target_metadata,
            )
        )
        async def run_migrations_online() -> None:
            connectable = async_engine_from_config(
                config.get_section(config.config_ini_section),
                prefix="sqlalchemy.",
                poolclass=pool.NullPool,
            )

            async with connectable.connect() as connection:
                await connection.run_sync(
                    lambda sync_conn: context.configure(
                        connection=sync_conn,
                        target_metadata=target_metadata,
                    )
                )

                with context.begin_transaction():
                    context.run_migrations()
            await connection.run_sync(context.run_migrations)


def run_migrations() -> None:
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        import asyncio
        asyncio.run(run_migrations_online())


run_migrations()