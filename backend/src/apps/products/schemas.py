from decimal import Decimal
from typing import Annotated
from pydantic import Field, ConfigDict
from pydantic import BaseModel, condecimal

from src.core.utils import to_camel


Price = Annotated[Decimal, condecimal(max_digits=10, decimal_places=2)]


class CamelModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

class ProductImageOut(CamelModel):
    """
    DTO изображения товара.
    """
    
    id: int
    url: str = Field(validation_alias='image_url')


class TagOut(CamelModel):
    """
    DTO тега товара.
    """

    id: int
    name: str


class CategoryOut(CamelModel):
    """
    DTO категории товара.
    """

    id: int
    name: str


class ProductOut(CamelModel):
    """
    DTO для чтения карточки товара.
    """

    id: int
    name: str
    description: str | None
    size: str | None
    price: Price
    discount_price: Price | None
    main_image_url: str | None
    is_active: bool
    stock: int
    category: CategoryOut | None
    images: list[ProductImageOut]
    tags: list[TagOut]


class ProductIn(CamelModel):
    """
    DTO для создания нового товара.
    """

    name: str
    description: str | None = None
    size: str | None = None
    price: Price
    discount_price: Price | None = None
    main_image_url: str | None = None
    is_active: bool = True
    stock: int = 0
    category_id: int | None = None
    tag_ids: list[int] = []
    image_urls: list[str] = []


class ProductUpdate(CamelModel):
    """
    DTO для обновления существующего товара.
    """

    name: str | None = None
    description: str | None = None
    size: str | None = None
    price: Price | None = None
    discount_price: Price | None = None
    main_image_url: str | None = None
    is_active: bool | None = None
    stock: int | None = None
    category_id: int | None = None
    tag_ids: list[int] | None = None
    image_urls: list[str] | None = None