"""Module with class for work with Tokens."""

from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Optional, Type

from app.src.use_cases.interfaces.cache.tokens.repo import (
    IAccessTokenRepository,
    IRefreshTokenRepository,
)


class AbstractUnitOfWork(ABC):
    """Abstract UoW class for work with Repositories.

        Pattern: Unit Of Work.

    Args:
        ABC (class): Used to create an abstract class.
    """

    access_token: IAccessTokenRepository
    refresh_token: IRefreshTokenRepository

    def __call__(self, transaction: bool) -> AbstractUnitOfWork:
        """Magic method responsible for the logic when calling class.

        Args:
            transaction (bool): Do command in Transaction or not.

        Returns:
            AbstractUnitOfWork: Return itself.
        """
        self._transaction = transaction
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
        if any((exc_type, exc_val, exc_tb)):
            await self._discard()
            return False
        await self._execute()
        return True

    @abstractmethod
    async def _execute(self) -> None:
        """Send commands to storage."""

    @abstractmethod
    async def _discard(self) -> None:
        """Cancel the transaction."""
