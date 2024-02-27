"""Module with Role DTO."""

import uuid
from datetime import date, datetime
from typing import Annotated, Optional

import pydantic as pd
from domain.base import BaseDTO


class UserDTO(BaseDTO):
    """Model which describe User object.

    Args:
        BaseDTO (class): Parent class with common fields for DTO models.
    """

    email: pd.EmailStr
    login: Annotated[
        str, pd.StringConstraints(max_length=60, strip_whitespace=True),
    ]
    password: Annotated[
        str, pd.StringConstraints(max_length=100, strip_whitespace=True),
    ]
    user_service_id: uuid.UUID
    full_name: Optional[
        Annotated[
            str, pd.StringConstraints(max_length=60, strip_whitespace=True),
        ]
    ] = None
    profile_picture: Optional[pd.FilePath] = None
    birthday: Optional[date] = None
    phone_number: Optional[
        Annotated[
            str, pd.StringConstraints(max_length=24, strip_whitespace=True),
        ]
    ] = None
    bio: Optional[Annotated[str, pd.StringConstraints(max_length=1000)]] = None
    created_at: datetime
    updated_at: datetime
