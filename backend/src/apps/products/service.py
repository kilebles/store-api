from typing import Iterable, List

from sqlalchemy import select, delete, true
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.exceptions import AppException
from src.apps.products import models, schemas


class ProductService:
    """
    Сервис для работы с товарами.
    """

    def __init__(self, session: AsyncSession):
        """
        Инициализация сервиса с сессией БД.
        """
        self.session = session

    async def create(self, data: schemas.ProductIn) -> models.Product:
        """
        Создание товара с привязкой тегов и изображений.
        """
        product = models.Product(
            name=data.name,
            description=data.description,
            size=data.size,
            price=data.price,
            discount_price=data.discount_price,
            main_image_url=data.main_image_url,
            is_active=data.is_active,
            stock=data.stock,
            category_id=data.category_id,
        )
        self.session.add(product)
        await self.session.flush()

        if data.image_urls:
            self.session.add_all(
                models.ProductImage(product_id=product.id, image_url=url)
                for url in data.image_urls
            )

        if data.tag_ids:
            tags = await self._load_tags(data.tag_ids)
            product.tags = list(tags)

        await self.session.commit()
        await self.session.refresh(
            product,
            attribute_names=("category", "images", "tags"),
        )
        return product

    async def get(self, product_id: int) -> models.Product | None:
        """
        Получение товара по id.
        """
        result = await self.session.execute(
            select(models.Product)
            .options(
                selectinload(models.Product.category),
                selectinload(models.Product.images),
                selectinload(models.Product.tags),
            )
            .where(models.Product.id == product_id)
        )
        return result.scalar_one_or_none()

    async def list(self, limit: int = 20, offset: int = 0) -> List[models.Product]:
        """
        Получение списка товаров с постраничной выборкой.
        """
        result = await self.session.execute(
            select(models.Product)
            .options(
                selectinload(models.Product.category),
                selectinload(models.Product.images),
                selectinload(models.Product.tags),
            )
            .order_by(models.Product.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def update(self, product_id: int, data: schemas.ProductUpdate) -> models.Product | None:
        """
        Частичное обновление товара с пересборкой связей по необходимости.
        """
        product = await self.get(product_id)
        if product is None:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            if field in {"tag_ids", "image_urls", "category_id"}:
                continue
            setattr(product, field, value)

        if data.category_id is not None:
            product.category_id = data.category_id

        if data.tag_ids is not None:
            tags = await self._load_tags(data.tag_ids)
            product.tags = list(tags)

        if data.image_urls is not None:
            await self.session.execute(
                delete(models.ProductImage).where(models.ProductImage.product_id == product.id)
            )
            if data.image_urls:
                self.session.add_all(
                    models.ProductImage(product_id=product.id, image_url=url)
                    for url in data.image_urls
                )

        await self.session.commit()
        await self.session.refresh(
            product,
            attribute_names=("category", "images", "tags"),
        )
        return product

    async def delete(self, product_id: int) -> bool:
        """
        Удаление товара.
        """
        product = await self.session.get(models.Product, product_id)
        if product is None:
            return False
        await self.session.delete(product)
        await self.session.commit()
        return True

    async def _load_tags(self, tag_ids: Iterable[int]) -> Iterable[models.Tag]:
        """
        Загрузка тегов по идентификаторам.
        """
        if not tag_ids:
            return []
        result = await self.session.execute(
            select(models.Tag).where(models.Tag.id.in_(list(tag_ids)))
        )
        return result.scalars().all()

    async def list_public(self, limit: int = 20, offset: int = 0) -> List[models.Product]:
        """
        Возвращает список активных товаров.
        """
        result = await self.session.execute(
            select(models.Product)
            .options(
                selectinload(models.Product.category),
                selectinload(models.Product.images),
                selectinload(models.Product.tags),
            )
            .where(models.Product.is_active.is_(true()))
            .order_by(models.Product.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def get_public(self, product_id: int) -> models.Product:
        """
        Возвращает один активный товар.
        """
        result = await self.session.execute(
            select(models.Product)
            .options(
                selectinload(models.Product.category),
                selectinload(models.Product.images),
                selectinload(models.Product.tags),
            )
            .where(
                models.Product.id == product_id,
                models.Product.is_active.is_(true()),
            )
        )
        product = result.scalar_one_or_none()
        if not product:
            raise AppException("Товар не найден", status_code=404)
        return product