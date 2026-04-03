from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.ad_repository import AdRepository
from app.repositories.category_repository import CategoryRepository
from app.services.ad_service import AdService
from app.services.category_service import CategoryService


async def provide_category_repository(
    db_session: AsyncSession,
) -> CategoryRepository:
    return CategoryRepository(db_session)


async def provide_category_service(
    category_repository: CategoryRepository,
) -> CategoryService:
    return CategoryService(category_repository)


async def provide_ad_repository(db_session: AsyncSession) -> AdRepository:
    return AdRepository(db_session)


async def provide_ad_service(
    ad_repository: AdRepository,
    category_repository: CategoryRepository,
) -> AdService:
    return AdService(ad_repository, category_repository)
