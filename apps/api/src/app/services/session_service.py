from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe

from app.domain import Session
from app.repositories.session_repository import SessionRepositoryContract
from app.security.session_token_hasher import SessionTokenHasher


class SessionServiceContract(ABC):
    @abstractmethod
    async def create_for_user(self, user_id: int) -> str: ...

    @abstractmethod
    async def get_active_session(self, raw_token: str) -> Session | None: ...

    @abstractmethod
    async def get_active_user_id(self, raw_token: str) -> int | None: ...

    @abstractmethod
    async def revoke_by_token(self, raw_token: str) -> None: ...


class SessionService(SessionServiceContract):
    def __init__(
        self,
        session_repo: SessionRepositoryContract,
        token_hasher: SessionTokenHasher | None = None,
        *,
        session_ttl: timedelta = timedelta(days=30),
    ) -> None:
        self._session_repo = session_repo
        self._token_hasher = token_hasher or SessionTokenHasher()
        self._session_ttl = session_ttl

    async def create_for_user(self, user_id: int) -> str:
        raw_token = token_urlsafe(32)
        expires_at = self._now() + self._session_ttl

        await self._session_repo.create_session(
            user_id=user_id,
            token_hash=self._token_hasher.hash(raw_token),
            expires_at=expires_at,
        )

        return raw_token

    async def get_active_session(self, raw_token: str) -> Session | None:
        session = await self._session_repo.get_session_by_token_hash(
            self._token_hasher.hash(raw_token)
        )

        if not self._is_active_session(session):
            return None

        return session

    async def get_active_user_id(self, raw_token: str) -> int | None:
        session = await self.get_active_session(raw_token)

        if session is None:
            return None

        return session.user_id

    async def revoke_by_token(self, raw_token: str) -> None:
        session = await self._session_repo.get_session_by_token_hash(
            self._token_hasher.hash(raw_token)
        )

        if session is None or session.revoked_at is not None:
            return

        await self._session_repo.revoke_session(session.id, self._now())

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def _is_active_session(self, session: Session | None) -> bool:
        if session is None:
            return False

        if session.revoked_at is not None:
            return False

        return self._normalize_datetime(session.expires_at) > self._now()

    def _normalize_datetime(self, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)
