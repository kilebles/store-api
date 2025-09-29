from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from collections.abc import AsyncGenerator

from src.core.settings import Settings

settings = Settings()


class Base(DeclarativeBase):
    """
    Базовый класс для моделей.
    """


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
)

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Зависимость для работы с БД в ручках FastAPI.
    """
    
    async with async_session_maker() as session:
        yield session