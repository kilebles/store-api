from fastapi import FastAPI

from src.apps.health.router import router as health_router


def apply_routes(app: FastAPI) -> None:
    """
    Подключает все роуты приложения.
    """
    
    app.include_router(health_router, prefix="/health", tags=["Health"])