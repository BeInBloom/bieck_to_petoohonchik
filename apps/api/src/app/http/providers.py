from litestar import Request
from litestar.di import Provide
from litestar.exceptions import NotAuthorizedException
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain import User
from app.repositories.ad_repository import AdRepository, AdRepositoryContract
from app.repositories.category_repository import CategoryRepository, CategoryRepositoryContract
from app.repositories.session_repository import SessionRepository, SessionRepositoryContract
from app.repositories.user_repository import UserRepository, UserRepositoryContract
from app.security.password_hasher import PasswordHasher
from app.services.ad_service import AdService, AdServiceContract
from app.services.auth_service import AuthService, AuthServiceContract
from app.services.category_service import CategoryService, CategoryServiceContract
from app.services.session_service import SessionService, SessionServiceContract

SESSION_COOKIE_NAME = "session"


async def provide_category_repository(
    db_session: AsyncSession,
) -> CategoryRepositoryContract:
    return CategoryRepository(db_session)


async def provide_category_service(
    category_repository: CategoryRepositoryContract,
) -> CategoryServiceContract:
    return CategoryService(category_repository)


def get_category_dependencies() -> dict[str, Provide]:
    return {
        "category_repository": Provide(provide_category_repository),
        "category_service": Provide(provide_category_service),
    }


async def provide_ad_repository(db_session: AsyncSession) -> AdRepositoryContract:
    return AdRepository(db_session)


async def provide_ad_service(
    ad_repository: AdRepositoryContract,
    category_repository: CategoryRepositoryContract,
) -> AdServiceContract:
    return AdService(ad_repository, category_repository)


def get_ad_dependencies() -> dict[str, Provide]:
    return {
        "ad_repository": Provide(provide_ad_repository),
        "ad_service": Provide(provide_ad_service),
    }


async def provide_user_repository(db_session: AsyncSession) -> UserRepositoryContract:
    return UserRepository(db_session)


async def provide_session_repository(db_session: AsyncSession) -> SessionRepositoryContract:
    return SessionRepository(db_session)


async def provide_session_service(
    session_repository: SessionRepositoryContract,
) -> SessionServiceContract:
    return SessionService(session_repository)


async def provide_password_hasher() -> PasswordHasher:
    return PasswordHasher()


async def provide_auth_service(
    user_repository: UserRepositoryContract,
    session_service: SessionServiceContract,
    password_hasher: PasswordHasher,
) -> AuthServiceContract:
    return AuthService(user_repository, session_service, password_hasher)


async def provide_current_user(
    request: Request,
    auth_service: AuthServiceContract,
) -> User | None:
    session_token = request.cookies.get(SESSION_COOKIE_NAME)

    if not session_token:
        return None

    return await auth_service.get_current_user(session_token)


async def provide_required_current_user(current_user: User | None) -> User:
    if current_user is None:
        raise NotAuthorizedException("not authenticated")

    return current_user


def get_auth_dependencies() -> dict[str, Provide]:
    return {
        "user_repository": Provide(provide_user_repository),
        "session_repository": Provide(provide_session_repository),
        "session_service": Provide(provide_session_service),
        "password_hasher": Provide(provide_password_hasher),
        "auth_service": Provide(provide_auth_service),
        "current_user": Provide(provide_current_user),
        "required_current_user": Provide(provide_required_current_user),
    }
