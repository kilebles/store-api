from fastapi import FastAPI

from src.apps.health.router import router as health_router
from src.apps.products.admin_router import router as admin_products_router
from src.apps.products.public_router import router as products_router


def apply_routes(app: FastAPI) -> None:
    """
    Подключает все роуты приложения.
    """
    
    app.include_router(health_router, prefix="/health", tags=["Health"])
    app.include_router(admin_products_router, prefix="/api/admin/products", tags=["Admin:products"])
    app.include_router(products_router, prefix="/api/products", tags=["Products"])