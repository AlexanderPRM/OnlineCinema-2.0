"""Module with UserSocialAccount DTO."""

import uuid
from datetime import datetime

from domain.base import BaseDTO


class UserSocialAccountDTO(BaseDTO):
    """Model which describe User Social Account object.

    Args:
        BaseDTO (class): Parent class with common fields for DTO models.
    """

    social_network_id: uuid.UUID
    user_id: uuid.UUID
    social_account_id: str
    created_at: datetime
    updated_at: datetime
