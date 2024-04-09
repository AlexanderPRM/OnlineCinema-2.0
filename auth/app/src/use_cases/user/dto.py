"""Module with DTO's for User Use cases."""

from __future__ import annotations

from typing import Annotated

import pydantic as pd
from passlib.context import CryptContext
from src.domain.user.dto import UserDTO

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserSignUpDTO(pd.BaseModel):
    """User sign up data transfer object.

    Args:
        BaseModel (class): Base Pydantic class for models.
    """

    email: pd.EmailStr
    login: Annotated[
        str, pd.StringConstraints(max_length=60, strip_whitespace=True),
    ]
    password: Annotated[
        str, pd.StringConstraints(strip_whitespace=True),
    ]

    @pd.model_validator(mode='after')
    def serialize_model(self) -> UserSignUpDTO:
        """Hash password.

        Returns:
            UserSignUpDTO: Return themself.
        """
        self.password = pwd_context.hash(self.password)
        return self


class UserSignUpOutDTO(pd.BaseModel):
    """User sign up output data transfer object.

    Args:
        BaseModel (class): Base Pydantic class for models.
    """

    created_user: UserDTO
    access_token: str
    refresh_token: str
