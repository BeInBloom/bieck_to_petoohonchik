from typing import Sequence

from advanced_alchemy.extensions.litestar import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,
)
from litestar import Litestar
from litestar.di import Provide
from litestar.types import ControllerRouterHandler

from app.config import Settings
from app.http.controllers import (
    AdsController,
    AuthController,
    CategoriesController,
    HealthController,
)
from app.http.providers import (
    get_ad_dependencies,
    get_auth_dependencies,
    get_category_dependencies,
)


def get_dependencies() -> dict[str, Provide]:
    return {
        **get_category_dependencies(),
        **get_ad_dependencies(),
        **get_auth_dependencies(),
    }


def get_handlers() -> Sequence[ControllerRouterHandler]:
    return [HealthController, CategoriesController, AdsController, AuthController]


def create_app() -> Litestar:
    settings = Settings()
    settings.data_dir.mkdir(parents=True, exist_ok=True)

    session_config = AsyncSessionConfig(expire_on_commit=False)
    alchemy_config = SQLAlchemyAsyncConfig(
        connection_string=settings.database_url,
        session_config=session_config,
        before_send_handler="autocommit",
        create_all=False,
    )

    alchemy = SQLAlchemyPlugin(config=alchemy_config)

    app = Litestar(
        route_handlers=get_handlers(),
        plugins=[alchemy],
        dependencies=get_dependencies(),
    )

    return app


app = create_app()
