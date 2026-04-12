from typing import Annotated

from litestar import Controller, get, post
from litestar.exceptions import NotFoundException
from litestar.params import Dependency, Parameter
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED

from app.domain import User
from app.http.schemas import AdRead, AdsPageRead
from app.http.schemas.ad import AdCreate, AdCreated
from app.http.service_exception_mapper import service_exception_mapper
from app.services.ad_service import AdServiceContract
from app.services.exceptions import ServiceError


class AdsController(Controller):
    path = "/ads"

    @get(status_code=HTTP_200_OK)
    async def list_ads(
        self,
        ad_service: Annotated[AdServiceContract, Dependency(skip_validation=True)],
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

    @get("/{id:int}", status_code=HTTP_200_OK)
    async def get_ad(
        self,
        id: int,
        ad_service: Annotated[AdServiceContract, Dependency(skip_validation=True)],
    ) -> AdRead:
        ad = await ad_service.get_ad(id)

        if ad is None:
            raise NotFoundException("ad not found")

        return AdRead.validate_value(ad)

    @post(status_code=HTTP_201_CREATED)
    async def post_ad(
        self,
        data: AdCreate,
        ad_service: Annotated[AdServiceContract, Dependency(skip_validation=True)],
        required_current_user: Annotated[User, Dependency(skip_validation=True)],
    ) -> AdCreated:
        try:
            id = await ad_service.create_ad(
                title=data.title,
                description=data.description,
                price_minor=data.price_minor,
                category_id=data.category_id,
                owner_id=required_current_user.id,
            )
        except ServiceError as error:
            service_exception_mapper.raise_http_exception(error)

        return AdCreated(status="ok", id=id)
