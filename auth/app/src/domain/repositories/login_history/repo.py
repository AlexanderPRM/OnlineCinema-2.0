"""Module with Logins Histories Repository."""

import uuid
from abc import ABC, abstractmethod

from src.domain.login_history.entities import LoginHistory


class ILoginHistoryRepository(ABC):
    """Repository with Login History Repository.

    Args:
        ABC (class): Used to create abstract class.
    """

    @abstractmethod
    async def insert(self, entity: LoginHistory) -> LoginHistory:
        """Add a new entry of login.

        Args:
            entity (LoginHistory): entity of LoginHistory.

        Returns:
            LoginHistory (class):
            LoginHistory class which represent login entry.
        """

    @abstractmethod
    async def retrieve_by_id(
        self,
        login_entry_id: uuid.UUID,
    ) -> LoginHistory | None:
        """Retrieve login entry by id.

        Args:
            login_entry_id (uuid.UUID): Login Entry UUID ID.

        Returns:
            LoginHistory | None: Return Login Entry if exists.
        """

    @abstractmethod
    async def retrieve_by_user_id(self, uid: uuid.UUID) -> list[LoginHistory]:
        """Retrieve login entry by user id.

        Args:
            uid (uuid.UUID): User UUID ID.

        Returns:
            LoginHistory (class):
            LoginHistory classs which represent login entry.
        """
