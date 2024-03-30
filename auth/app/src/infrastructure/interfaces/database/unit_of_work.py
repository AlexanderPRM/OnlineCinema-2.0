"""Module with Database Unit of Work."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.infrastructure.repositories.login_history import (
    LoginHistoryRepository,
)
from src.infrastructure.repositories.role import RoleRepository
from src.infrastructure.repositories.social_network import (
    SocialNetworkRepository,
)
from src.infrastructure.repositories.user import UserRepository
from src.infrastructure.repositories.user_service import UserServiceRepository
from src.infrastructure.repositories.user_social_account import (
    UserSocialAccountRepository,
)
from src.use_cases.interfaces.database.unit_of_work import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    """Class for work with repositories.

    Args:
        AbstractUnitOfWork (class): Abstract Unit of Work class.
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        """Init method.

        Args:
            session_factory (async_sessionmaker[AsyncSession]):
            Factory for create sessions.
        """
        self._session_factory = session_factory

    async def __aenter__(self) -> UnitOfWork:
        """Call when entry in async context manager.

        Returns:
            UnitOfWork: Return themself.
        """
        self._session = self._session_factory()

        self.user = UserRepository(self._session)
        self.user_service = UserServiceRepository(self._session)
        self.role = RoleRepository(self._session)
        self.login_history = LoginHistoryRepository(self._session)
        self.social_network = SocialNetworkRepository(self._session)
        self.user_social_account = UserSocialAccountRepository(self._session)

        return self

    async def _commit(self) -> None:
        await self._session.commit()

    async def _rollback(self) -> None:
        await self._session.rollback()

    async def _close(self) -> None:
        await self._session.close()
