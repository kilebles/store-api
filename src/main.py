from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from fastapi import FastAPI

from .core.settings import Settings
from .core.middleware import use_middleware
from .core.exceptions import use_exceptions_handlers
from .router import apply_routes


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    settings = Settings()
    print(f"{settings.POSTGRES_DB=} | {settings.MINIO_BUCKET=}")
    yield
    print("App shutdown")


def create_app() -> FastAPI:
    settings = Settings()

    app = FastAPI(
        lifespan=lifespan,
        docs_url="/docs",
        openapi_url="/docs.json",
        title="store-api",
    )

    use_middleware(app, settings.CORS_ORIGINS)
    use_exceptions_handlers(app, settings)
    apply_routes(app)

    return app


app = create_app()
