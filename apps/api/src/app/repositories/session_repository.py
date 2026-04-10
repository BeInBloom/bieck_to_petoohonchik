from abc import ABC, abstractmethod
from datetime import datetime

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain import Session


class SessionRepositoryContract(ABC):
    @abstractmethod
    async def create_session(
        self,
        *,
        user_id: int,
        token_hash: str,
        expires_at: datetime,
    ) -> Session: ...

    @abstractmethod
    async def get_session_by_token_hash(self, token_hash: str) -> Session | None: ...

    @abstractmethod
    async def get_active_session_by_token_hash(self, token_hash: str) -> Session | None: ...

    @abstractmethod
    async def delete_session(self, id: int) -> None: ...

    @abstractmethod
    async def delete_user_sessions(self, user_id: int) -> None: ...

    @abstractmethod
    async def revoke_session(self, id: int, revoked_at: datetime) -> None: ...

    @abstractmethod
    async def revoke_session_by_token_hash(self, token_hash: str, revoked_at: datetime) -> None: ...

    @abstractmethod
    async def revoke_user_sessions(self, user_id: int, revoked_at: datetime) -> None: ...


class SessionRepository(SessionRepositoryContract):
    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    async def create_session(
        self,
        *,
        user_id: int,
        token_hash: str,
        expires_at: datetime,
    ) -> Session:
        session = Session(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        self._db_session.add(session)
        await self._db_session.flush()
        return session

    async def get_session_by_token_hash(self, token_hash: str) -> Session | None:
        stmt = select(Session).where(Session.token_hash == token_hash)
        result = await self._db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_session_by_token_hash(self, token_hash: str) -> Session | None:
        stmt = select(Session).where(
            Session.token_hash == token_hash,
            Session.revoked_at.is_(None),
            Session.expires_at > func.now(),
        )
        result = await self._db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_session(self, id: int) -> None:
        stmt = delete(Session).where(Session.id == id)
        await self._db_session.execute(stmt)

    async def delete_user_sessions(self, user_id: int) -> None:
        stmt = delete(Session).where(Session.user_id == user_id)
        await self._db_session.execute(stmt)

    async def revoke_session(self, id: int, revoked_at: datetime) -> None:
        stmt = (
            update(Session)
            .where(Session.id == id, Session.revoked_at.is_(None))
            .values(revoked_at=revoked_at)
        )
        await self._db_session.execute(stmt)

    async def revoke_session_by_token_hash(self, token_hash: str, revoked_at: datetime) -> None:
        stmt = (
            update(Session)
            .where(Session.token_hash == token_hash, Session.revoked_at.is_(None))
            .values(revoked_at=revoked_at)
        )
        await self._db_session.execute(stmt)

    async def revoke_user_sessions(self, user_id: int, revoked_at: datetime) -> None:
        stmt = (
            update(Session)
            .where(Session.user_id == user_id, Session.revoked_at.is_(None))
            .values(revoked_at=revoked_at)
        )
        await self._db_session.execute(stmt)
