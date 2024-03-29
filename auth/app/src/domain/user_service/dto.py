"""Module with Role DTO."""

import uuid
from datetime import datetime

from src.domain.base import BaseDTO


class UserServiceDTO(BaseDTO):
    """Model which describe User Service object.

    Args:
        BaseDTO (class): Parent class with common fields for DTO models.
    """

    role_id: uuid.UUID
    active: bool
    verified: bool
    created_at: datetime
    updated_at: datetime
