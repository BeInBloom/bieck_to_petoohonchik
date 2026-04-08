from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain import Category


class CategoryRepositoryContract(ABC):
    @abstractmethod
    async def list_categories(self) -> list[Category]: ...

    @abstractmethod
    async def get_category(self, slug: str) -> Category | None: ...

    @abstractmethod
    async def get_category_by_id(self, id: int) -> Category | None: ...


class CategoryRepository(CategoryRepositoryContract):
    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    async def list_categories(self) -> list[Category]:
        stmt = select(Category).order_by(Category.name)
        result = await self._db_session.execute(stmt)
        return list(result.scalars().all())

    async def get_category(self, slug: str) -> Category | None:
        stmt = select(Category).where(Category.slug == slug)
        result = await self._db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_category_by_id(self, id: int) -> Category | None:
        stmt = select(Category).where(Category.id == id)
        result = await self._db_session.execute(stmt)
        return result.scalar_one_or_none()
