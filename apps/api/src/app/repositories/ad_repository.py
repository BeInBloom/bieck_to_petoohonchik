from abc import ABC, abstractmethod

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain import Ad
from app.services.models import AdsPage


class AdRepositoryContract(ABC):
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


class AdRepository(AdRepositoryContract):
    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    async def get_ad(self, id: int) -> Ad | None:
        stmt = select(Ad).where(Ad.id == id, Ad.deleted_at.is_(None))
        result = await self._db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_ads(self, limit: int, offset: int) -> AdsPage:
        base_stmt = select(Ad).where(Ad.deleted_at.is_(None))

        total_stmt = select(func.count()).select_from(
            select(Ad.id).where(Ad.deleted_at.is_(None)).subquery()
        )
        total_res = await self._db_session.execute(total_stmt)
        total = total_res.scalar_one()

        items_stmt = (
            base_stmt.order_by(Ad.created_at.desc(), Ad.id.desc()).limit(limit).offset(offset)
        )
        items_result = await self._db_session.execute(items_stmt)
        items = list(items_result.scalars().all())

        return AdsPage(
            items=items,
            total=total,
            limit=limit,
            offset=offset,
        )

    async def create_ad(
        self,
        *,
        title: str,
        description: str,
        price_minor: int,
        category_id: int,
        owner_id: int,
    ) -> int:
        ad = Ad(
            title=title,
            description=description,
            price_minor=price_minor,
            category_id=category_id,
            owner_id=owner_id,
        )

        self._db_session.add(ad)
        await self._db_session.flush()

        return ad.id
