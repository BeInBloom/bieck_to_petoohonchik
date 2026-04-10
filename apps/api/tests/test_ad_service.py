from unittest.mock import AsyncMock

import pytest
from sqlalchemy.exc import IntegrityError

from app.domain import Category
from app.services.ad_service import AdService
from app.services.exceptions import CategoryNotFoundError


@pytest.mark.asyncio
async def test_create_ad_passes_owner_id_to_repository() -> None:
    ad_repository = AsyncMock()
    ad_repository.create_ad.return_value = 17
    category_repository = AsyncMock()
    category_repository.get_category_by_id.return_value = Category(
        id=5,
        name="Dogs",
        slug="dogs",
    )
    service = AdService(ad_repository, category_repository)

    created_id = await service.create_ad(
        title="Puppy",
        description="Healthy puppy",
        price_minor=150_000,
        category_id=5,
        owner_id=23,
    )

    assert created_id == 17
    category_repository.get_category_by_id.assert_awaited_once_with(5)
    ad_repository.create_ad.assert_awaited_once_with(
        title="Puppy",
        description="Healthy puppy",
        price_minor=150_000,
        category_id=5,
        owner_id=23,
    )


@pytest.mark.asyncio
async def test_create_ad_raises_when_category_missing_and_does_not_create_ad() -> None:
    ad_repository = AsyncMock()
    category_repository = AsyncMock()
    category_repository.get_category_by_id.return_value = None
    service = AdService(ad_repository, category_repository)

    with pytest.raises(CategoryNotFoundError):
        await service.create_ad(
            title="Puppy",
            description="Healthy puppy",
            price_minor=150_000,
            category_id=999,
            owner_id=23,
        )

    category_repository.get_category_by_id.assert_awaited_once_with(999)
    ad_repository.create_ad.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_ad_raises_when_insert_hits_integrity_error() -> None:
    ad_repository = AsyncMock()
    ad_repository.create_ad.side_effect = IntegrityError(
        "INSERT INTO ad (...) VALUES (...)",
        {"category_id": 5},
        Exception("foreign key constraint failed"),
    )
    category_repository = AsyncMock()
    category_repository.get_category_by_id.return_value = Category(
        id=5,
        name="Dogs",
        slug="dogs",
    )
    service = AdService(ad_repository, category_repository)

    with pytest.raises(CategoryNotFoundError):
        await service.create_ad(
            title="Puppy",
            description="Healthy puppy",
            price_minor=150_000,
            category_id=5,
            owner_id=23,
        )

    category_repository.get_category_by_id.assert_awaited_once_with(5)
    ad_repository.create_ad.assert_awaited_once_with(
        title="Puppy",
        description="Healthy puppy",
        price_minor=150_000,
        category_id=5,
        owner_id=23,
    )
