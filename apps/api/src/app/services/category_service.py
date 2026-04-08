from abc import ABC, abstractmethod

from app.domain import Category
from app.repositories.category_repository import CategoryRepositoryContract


class CategoryServiceContract(ABC):
    @abstractmethod
    async def list_categories(self) -> list[Category]: ...

    @abstractmethod
    async def get_category(self, slug: str) -> Category | None: ...


class CategoryService(CategoryServiceContract):
    def __init__(self, category_repo: CategoryRepositoryContract) -> None:
        self._category_repo = category_repo

    async def list_categories(self) -> list[Category]:
        return await self._category_repo.list_categories()

    async def get_category(self, slug: str) -> Category | None:
        return await self._category_repo.get_category(slug)
