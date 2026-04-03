from typing import Protocol

from app.domain import Category


class _CategoryRepository(Protocol):
    async def list_categories(self) -> list[Category]: ...
    async def get_category(self, slug: str) -> Category | None: ...


class CategoryService:
    def __init__(self, category_repo: _CategoryRepository) -> None:
        self._category_repo = category_repo

    async def list_categories(self) -> list[Category]:
        return await self._category_repo.list_categories()

    async def get_category(self, slug: str) -> Category | None:
        return await self._category_repo.get_category(slug)
