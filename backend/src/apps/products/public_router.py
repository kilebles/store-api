from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.apps.products.schemas import ProductOut
from src.apps.products.service import ProductService

router = APIRouter()


@router.get("/", response_model=list[ProductOut])
async def list_products(
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> list[ProductOut]:
    """
    Публичный список активных товаров.
    """
    service = ProductService(db)
    items = await service.list_public(limit=limit, offset=offset)
    return [ProductOut.model_validate(p, from_attributes=True) for p in items]


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
) -> ProductOut:
    """
    Публичная карточка товара.
    """
    service = ProductService(db)
    try:
        product = await service.get_public(product_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return ProductOut.model_validate(product, from_attributes=True)