from abc import ABC, abstractmethod

from app.domain import Ad
from app.repositories.ad_repository import AdRepositoryContract
from app.repositories.category_repository import CategoryRepositoryContract
from app.services.exceptions import CategoryNotFoundError
from app.services.models import AdsPage


class AdServiceContract(ABC):
    @abstractmethod
    async def get_ad(self, id: int) -> Ad | None: ...

    @abstractmethod
    async def list_ads(self, limit: int, offset: int) -> AdsPage: ...

    @abstractmethod
    async def create_ad(
        self,
        *,
        title: str,
        description: str,
        price_minor: int,
        category_id: int,
        owner_id: int,
    ) -> int: ...


class AdService(AdServiceContract):
    def __init__(
        self,
        ad_repo: AdRepositoryContract,
        category_repo: CategoryRepositoryContract,
    ) -> None:
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
        owner_id: int,
    ) -> int:
        category = await self._category_repo.get_category_by_id(category_id)

        if category is None:
            raise CategoryNotFoundError

        return await self._ad_repo.create_ad(
            title=title,
            description=description,
            price_minor=price_minor,
            category_id=category_id,
            owner_id=owner_id,
        )
