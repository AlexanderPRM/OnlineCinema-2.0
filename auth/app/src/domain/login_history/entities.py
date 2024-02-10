"""Module with Login History class."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Optional

from domain.base import Base
from domain.login_history.dto import LoginHistoryDTO


class LoginHistory(Base):
    """Class which represent a Login History.

    Args:
        Base (class): Base representing class.
    """

    def __init__(self, entity: LoginHistoryDTO) -> None:
        """Init method.

        Args:
            entity (LoginHistoryDTO):  Data Transfer Object of Login History.
        """
        self._id = entity.id
        self._user_agent = entity.user_agent
        self._provider_id = entity.provider_id
        self._login_date = entity.login_date

    @classmethod
    def create(
        cls, user_agent: str, provider_id: Optional[uuid.UUID] = None,
    ) -> LoginHistory:
        """Create Login History class which represent a login history object.

        Args:
            user_agent (str): HTTP Header intended to identify User.
            provider_id (UUID): Third-party service that user used to login.

        Returns:
            Role (class): Return created class.
        """
        return cls(
            entity=LoginHistoryDTO(
                id=uuid.uuid4(),
                user_agent=user_agent,
                provider_id=provider_id,
                login_date=datetime.now(UTC),
            ),
        )
