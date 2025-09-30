from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.apps.products.schemas import ProductIn, ProductOut, ProductUpdate
from src.apps.products.service import ProductService

router = APIRouter()


@router.post("/", response_model=ProductOut)
async def create_product(payload: ProductIn, db: AsyncSession = Depends(get_db)) -> ProductOut:
    """
    Создание товара.
    """
    
    service = ProductService(db)
    product = await service.create(payload)
    return ProductOut.model_validate(product, from_attributes=True)


@router.get("/", response_model=list[ProductOut])
async def list_products(
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> list[ProductOut]:
    """
    Список товаров с постраничной выборкой.
    """
    
    service = ProductService(db)
    items = await service.list(limit=limit, offset=offset)
    return [ProductOut.model_validate(p, from_attributes=True) for p in items]


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)) -> ProductOut:
    """
    Детальная информация о товаре.
    """
    
    service = ProductService(db)
    product = await service.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return ProductOut.model_validate(product, from_attributes=True)


@router.patch("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: AsyncSession = Depends(get_db),
) -> ProductOut:
    """
    Частичное обновление товара.
    """
    
    service = ProductService(db)
    product = await service.update(product_id, payload)
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return ProductOut.model_validate(product, from_attributes=True)


@router.delete("/{product_id}", response_model=dict)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    """
    Удаление товара.
    """
    
    service = ProductService(db)
    ok = await service.delete(product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return {"ok": True}