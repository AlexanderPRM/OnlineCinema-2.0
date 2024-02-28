"""Module with Login History DTO."""

import uuid
from datetime import datetime
from typing import Optional

from src.domain.base import BaseDTO


class LoginHistoryDTO(BaseDTO):
    """Model which describe Login History object.

    Args:
        BaseDTO (class): Parent class with common fields for DTO models.
    """

    user_id: uuid.UUID
    user_agent: str
    social_network_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime
