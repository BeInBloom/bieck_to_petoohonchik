from typing import Protocol

from app.domain import Ad, Category
from app.services.exceptions import CategoryNotFoundError
from app.services.models import AdsPage


class _AdRepository(Protocol):
    async def list_ads(self, limit: int, offset: int) -> AdsPage: ...
    async def get_ad(self, id: int) -> Ad | None: ...
    async def create_ad(
        self,
        *,
        title: str,
        description: str,
        price_minor: int,
        category_id: int,
    ) -> int: ...


class _CategoryRepository(Protocol):
    async def get_category_by_id(self, id: int) -> Category | None: ...


class AdService:
    def __init__(self, ad_repo: _AdRepository, category_repo: _CategoryRepository) -> None:
        self._ad_repo = ad_repo
        self._category_repo = category_repo

    async def get_ad(self, id: int) -> Ad | None:
        return await self._ad_repo.get_ad(id)

    async def list_ads(self, limit: int, offset: int) -> AdsPage:
        return await self._ad_repo.list_ads(limit, offset)

    async def create_ad(
        self,
        *,
        title: str,
        description: str,
        price_minor: int,
        category_id: int,
    ) -> int:
        category = await self._category_repo.get_category_by_id(category_id)

        if category is None:
            raise CategoryNotFoundError

        return await self._ad_repo.create_ad(
            title=title,
            description=description,
            price_minor=price_minor,
            category_id=category_id,
        )
