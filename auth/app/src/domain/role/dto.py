"""Module with Role DTO."""

from datetime import datetime
from typing import Annotated, Optional

import pydantic as pd
from src.domain.base import BaseDTO
from src.domain.role.value_objects import AccessLevel


class RoleDTO(BaseDTO):
    """Model which describe Role object.

    Args:
        BaseDTO (class): Parent class with common fields for DTO models.
    """

    name: Annotated[
        str, pd.StringConstraints(strip_whitespace=True, max_length=24),
    ]
    description: Optional[Annotated[
        str, pd.StringConstraints(strip_whitespace=True, max_length=100),
        ]
    ] = None
    access_level: AccessLevel
    created_at: datetime
    updated_at: datetime
