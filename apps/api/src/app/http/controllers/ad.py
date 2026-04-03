from typing import Annotated, Protocol

from litestar import Controller, get, post
from litestar.exceptions import NotFoundException
from litestar.params import Dependency, Parameter
from litestar.status_codes import HTTP_201_CREATED

from app.domain import Ad
from app.http.schemas import AdRead, AdsPageRead
from app.http.schemas.ad import AdCreate, AdCreated
from app.services.exceptions import CategoryNotFoundError
from app.services.models import AdsPage


class _AdService(Protocol):
    async def get_ad(self, id: int) -> Ad | None: ...
    async def list_ads(self, limit: int, offset: int) -> AdsPage: ...
    async def create_ad(
        self,
        *,
        title: str,
        description: str,
        price_minor: int,
        category_id: int,
    ) -> int: ...


class AdsController(Controller):
    path = "/ads"

    @get()
    async def list_ads(
        self,
        ad_service: Annotated[_AdService, Dependency(skip_validation=True)],
        limit: Annotated[int, Parameter(ge=1, le=100)] = 20,
        offset: Annotated[int, Parameter(ge=0)] = 0,
    ) -> AdsPageRead:
        pages = await ad_service.list_ads(limit, offset)

        return AdsPageRead(
            items=AdRead.validate_list(pages.items),
            limit=pages.limit,
            offset=pages.offset,
            total=pages.total,
        )

    @get("/{id:int}")
    async def get_ad(
        self,
        id: int,
        ad_service: Annotated[_AdService, Dependency(skip_validation=True)],
    ) -> AdRead:
        ad = await ad_service.get_ad(id)

        if ad is None:
            raise NotFoundException("ad not found")

        return AdRead.validate_value(ad)

    @post(status_code=HTTP_201_CREATED)
    async def post_ad(
        self,
        data: AdCreate,
        ad_service: Annotated[_AdService, Dependency(skip_validation=True)],
    ) -> AdCreated:
        try:
            id = await ad_service.create_ad(
                title=data.title,
                description=data.description,
                price_minor=data.price_minor,
                category_id=data.category_id,
            )
        except CategoryNotFoundError as exc:
            raise NotFoundException("category not found") from exc

        return AdCreated(status="ok", id=id)
