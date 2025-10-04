from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.apps.products.schemas import (
    CategoryIn, CategoryOut,
    ProductIn, ProductOut, ProductUpdate,
    TagIn, TagOut,
)
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


@router.get("/categories", response_model=list[CategoryOut])
async def list_categories(db: AsyncSession = Depends(get_db)) -> list[CategoryOut]:
    """
    Получить список категорий с тегами.
    """
    
    service = ProductService(db)
    items = await service.list_categories()
    return [CategoryOut.model_validate(c, from_attributes=True) for c in items]


@router.post("/categories", response_model=CategoryOut)
async def create_category(payload: CategoryIn, db: AsyncSession = Depends(get_db)) -> CategoryOut:
    """
    Создание категории.
    """
    
    service = ProductService(db)
    category = await service.create_category(payload.name)

    await db.refresh(category, attribute_names=["id", "name", "tags"])

    return CategoryOut.model_validate(category, from_attributes=True)


@router.patch("/categories/{category_id}", response_model=CategoryOut)
async def update_category(category_id: int, payload: CategoryIn, db: AsyncSession = Depends(get_db)) -> CategoryOut:
    """
    Обновление категории.
    """
    
    service = ProductService(db)
    category = await service.update_category(category_id, payload.name)

    await db.refresh(category, attribute_names=["id", "name", "tags"])

    return CategoryOut.model_validate(category, from_attributes=True)


@router.delete("/categories/{category_id}", response_model=dict)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    """
    Удаление категории.
    """
    
    service = ProductService(db)
    ok = await service.delete_category(category_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return {"ok": True}


@router.get("/categories/{category_id}/tags", response_model=list[TagOut])
async def list_tags_by_category(category_id: int, db: AsyncSession = Depends(get_db)) -> list[TagOut]:
    """
    Получить список тегов по категории.
    """

    service = ProductService(db)
    items = await service.list_tags_by_category(category_id)
    return [TagOut.model_validate(t, from_attributes=True) for t in items]


@router.post("/tags", response_model=TagOut)
async def create_tag(payload: TagIn, db: AsyncSession = Depends(get_db)) -> TagOut:
    """
    Создание тега.
    """

    service = ProductService(db)
    tag = await service.create_tag(payload.name, payload.category_id)
    return TagOut.model_validate(tag, from_attributes=True)


@router.patch("/tags/{tag_id}", response_model=TagOut)
async def update_tag(tag_id: int, payload: TagIn, db: AsyncSession = Depends(get_db)) -> TagOut:
    """
    Обновление тега.
    """

    service = ProductService(db)
    tag = await service.update_tag(tag_id, payload.name)
    if not tag:
        raise HTTPException(status_code=404, detail="Тег не найден")
    return TagOut.model_validate(tag, from_attributes=True)


@router.delete("/tags/{tag_id}", response_model=dict)
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    """
    Удаление тега.
    """

    service = ProductService(db)
    ok = await service.delete_tag(tag_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Тег не найден")
    return {"ok": True}


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