"""Module with class for work with Database."""

from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Optional, Type

from domain.repositories.login_history.repo import ILoginHistoryRepository
from domain.repositories.role.repo import IRoleRepository
from domain.repositories.social_network.repo import ISocialNetworkRepository
from domain.repositories.user.repo import IUserRepository
from domain.repositories.user_service.repo import IUserServiceRepository
from domain.repositories.user_social_account.repo import (
    IUserSocialAccountRepository,
)


class AbstractUnitOfWork(ABC):
    """Abstract UoW class for work with Repositories.

        Pattern: Unit Of Work.

    Args:
        ABC (class): Used to create an abstract class.
    """

    user: IUserRepository
    user_service: IUserServiceRepository
    role: IRoleRepository
    login_history: ILoginHistoryRepository
    social_network: ISocialNetworkRepository
    user_social_account: IUserSocialAccountRepository

    def __call__(self, autocommit: bool) -> AbstractUnitOfWork:
        """Magic method responsible for the logic when calling class.

        Args:
            autocommit (bool): Do autcommit in session or not.

        Returns:
            AbstractUnitOfWork: Return itself.
        """
        self._autocommit = autocommit
        return self

    async def __aenter__(self) -> AbstractUnitOfWork:
        """To use async context manager.

            This method overriden in child class.

        Returns:
            AbstractUnitOfWork: Return itself.
        """
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        """To use async context manager.

        Args:
            exc_type (Optional[Type[BaseException]]): Exception Type
            exc_val (Optional[BaseException]): Instance of Exception
            exc_tb (Optional[TracebackType]): Traceback.

        Returns:
            bool: Has error.
        """
        if any((exc_type, exc_tb, exc_val)):
            await self._rollback()
            return False

        if self._autocommit:
            await self._commit()

        await self._close()
        return True

    @abstractmethod
    async def _commit(self) -> None:
        """Commit Transaction."""

    @abstractmethod
    async def _rollback(self) -> None:
        """Roll backs changes."""

    @abstractmethod
    async def _close(self) -> None:
        """Close Session."""
