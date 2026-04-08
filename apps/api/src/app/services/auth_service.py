from abc import ABC, abstractmethod

from app.domain import User
from app.repositories.user_repository import UserRepositoryContract
from app.security.password_hasher import PasswordHasher
from app.services.exceptions import (
    InactiveUserError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from app.services.models import AuthResult
from app.services.session_service import SessionServiceContract


class AuthServiceContract(ABC):
    @abstractmethod
    async def register(
        self,
        *,
        email: str,
        display_name: str,
        password: str,
    ) -> AuthResult: ...

    @abstractmethod
    async def login(
        self,
        *,
        email: str,
        password: str,
    ) -> AuthResult: ...

    @abstractmethod
    async def logout(self, raw_session_token: str) -> None: ...

    @abstractmethod
    async def get_current_user(self, raw_session_token: str) -> User | None: ...


class AuthService(AuthServiceContract):
    def __init__(
        self,
        user_repo: UserRepositoryContract,
        session_service: SessionServiceContract,
        password_hasher: PasswordHasher,
    ) -> None:
        self._user_repo = user_repo
        self._session_service = session_service
        self._password_hasher = password_hasher

    async def register(
        self,
        *,
        email: str,
        display_name: str,
        password: str,
    ) -> AuthResult:
        existing_user = await self._user_repo.get_user_by_email(email)

        if existing_user is not None:
            raise UserAlreadyExistsError()

        user = await self._user_repo.create_user(
            email=email,
            display_name=display_name,
            password_hash=self._password_hasher.hash(password),
        )
        session_token = await self._session_service.create_for_user(user.id)

        return AuthResult(user=user, session_token=session_token)

    async def login(
        self,
        *,
        email: str,
        password: str,
    ) -> AuthResult:
        user = await self._user_repo.get_user_by_email(email)
        user = self._ensure_user_can_login(user, password)
        session_token = await self._session_service.create_for_user(user.id)
        return AuthResult(user=user, session_token=session_token)

    async def logout(self, raw_session_token: str) -> None:
        await self._session_service.revoke_by_token(raw_session_token)

    async def get_current_user(self, raw_session_token: str) -> User | None:
        user_id = await self._session_service.get_active_user_id(raw_session_token)

        if user_id is None:
            return None

        return await self._user_repo.get_user_by_id(user_id)

    def _ensure_user_can_login(self, user: User | None, password: str) -> User:
        if user is None:
            raise InvalidCredentialsError()

        if not user.is_active:
            raise InactiveUserError()

        if not self._password_hasher.verify(user.password_hash, password):
            raise InvalidCredentialsError()

        return user
