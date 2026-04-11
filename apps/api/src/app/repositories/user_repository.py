from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain import User, UserRole
from app.services.exceptions import UserAlreadyExistsError


class UserRepositoryContract(ABC):
    @abstractmethod
    async def get_user_by_id(self, id: int) -> User | None: ...

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def create_user(
        self,
        *,
        email: str,
        display_name: str,
        password_hash: str,
        role: UserRole = UserRole.USER,
    ) -> User: ...


class UserRepository(UserRepositoryContract):
    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    async def get_user_by_id(self, id: int) -> User | None:
        stmt = select(User).where(User.id == id)
        result = await self._db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self._db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(
        self,
        *,
        email: str,
        display_name: str,
        password_hash: str,
        role: UserRole = UserRole.USER,
    ) -> User:
        user = User(
            email=email,
            display_name=display_name,
            password_hash=password_hash,
            role=role,
        )
        self._db_session.add(user)
        try:
            await self._db_session.flush()
        except IntegrityError as error:
            raise UserAlreadyExistsError() from error

        return user
