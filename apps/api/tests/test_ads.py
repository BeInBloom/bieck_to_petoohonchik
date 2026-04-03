import asyncio
from datetime import datetime, timezone

from litestar.testing import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain import Ad, Category


def test_get_ad_returns_ad(
    client: TestClient,
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def seed_ad() -> None:
        async with db_session_factory() as session:
            category = Category(name="Dogs", slug="dogs")
            session.add(category)
            await session.flush()

            session.add(
                Ad(
                    title="Puppy",
                    description="Healthy puppy",
                    price_minor=150_000,
                    category_id=category.id,
                )
            )
            await session.commit()

    asyncio.run(seed_ad())

    response = client.get("/ads/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Puppy"
    assert response.json()["description"] == "Healthy puppy"
    assert response.json()["price_minor"] == 150_000
    assert response.json()["category_id"] == 1
    assert response.json()["published_at"] is None
    assert response.json()["deleted_at"] is None
    assert response.json()["created_at"] is not None
    assert response.json()["updated_at"] is not None


def test_get_ad_returns_404_when_ad_not_found(client: TestClient) -> None:
    response = client.get("/ads/999")

    assert response.status_code == 404


def test_get_ad_returns_404_when_ad_is_soft_deleted(
    client: TestClient,
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def seed_deleted_ad() -> None:
        async with db_session_factory() as session:
            category = Category(name="Dogs", slug="dogs")
            session.add(category)
            await session.flush()

            session.add(
                Ad(
                    title="Hidden puppy",
                    description="Should not be visible",
                    price_minor=90_000,
                    category_id=category.id,
                    deleted_at=datetime.now(timezone.utc),
                )
            )
            await session.commit()

    asyncio.run(seed_deleted_ad())

    response = client.get("/ads/1")

    assert response.status_code == 404


def test_list_ads_returns_paginated_items(
    client: TestClient,
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def seed_ads() -> None:
        async with db_session_factory() as session:
            category = Category(name="Dogs", slug="dogs")
            session.add(category)
            await session.flush()

            session.add_all(
                [
                    Ad(
                        title="First ad",
                        description="First description",
                        price_minor=100_000,
                        category_id=category.id,
                    ),
                    Ad(
                        title="Second ad",
                        description="Second description",
                        price_minor=200_000,
                        category_id=category.id,
                    ),
                    Ad(
                        title="Deleted ad",
                        description="Should not be listed",
                        price_minor=300_000,
                        category_id=category.id,
                        deleted_at=datetime.now(timezone.utc),
                    ),
                ]
            )
            await session.commit()

    asyncio.run(seed_ads())

    response = client.get("/ads?limit=1&offset=0")

    assert response.status_code == 200
    assert response.json()["total"] == 2
    assert response.json()["limit"] == 1
    assert response.json()["offset"] == 0
    assert [item["title"] for item in response.json()["items"]] == ["Second ad"]


def test_list_ads_respects_offset(
    client: TestClient,
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def seed_ads() -> None:
        async with db_session_factory() as session:
            category = Category(name="Dogs", slug="dogs")
            session.add(category)
            await session.flush()

            session.add_all(
                [
                    Ad(
                        title="First ad",
                        description="First description",
                        price_minor=100_000,
                        category_id=category.id,
                    ),
                    Ad(
                        title="Second ad",
                        description="Second description",
                        price_minor=200_000,
                        category_id=category.id,
                    ),
                ]
            )
            await session.commit()

    asyncio.run(seed_ads())

    response = client.get("/ads?limit=1&offset=1")

    assert response.status_code == 200
    assert response.json()["total"] == 2
    assert response.json()["limit"] == 1
    assert response.json()["offset"] == 1
    assert [item["title"] for item in response.json()["items"]] == ["First ad"]


def test_post_ad_creates_ad(
    client: TestClient,
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def seed_category() -> None:
        async with db_session_factory() as session:
            session.add(Category(name="Dogs", slug="dogs"))
            await session.commit()

    asyncio.run(seed_category())

    response = client.post(
        "/ads",
        json={
            "title": "Puppy",
            "description": "Healthy puppy",
            "price_minor": 150_000,
            "category_id": 1,
        },
    )

    assert response.status_code == 201
    assert response.json() == {"status": "ok", "id": 1}

    get_response = client.get("/ads/1")

    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Puppy"
    assert get_response.json()["description"] == "Healthy puppy"
    assert get_response.json()["price_minor"] == 150_000
    assert get_response.json()["category_id"] == 1


def test_post_ad_returns_404_when_category_not_found(client: TestClient) -> None:
    response = client.post(
        "/ads",
        json={
            "title": "Puppy",
            "description": "Healthy puppy",
            "price_minor": 150_000,
            "category_id": 999,
        },
    )

    assert response.status_code == 404
