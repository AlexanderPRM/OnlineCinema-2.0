"""Module with DTO's for User Use cases."""

from __future__ import annotations

from typing import Annotated

import pydantic as pd
from passlib.context import CryptContext
from pydantic_core import PydanticCustomError
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


class UserSignInDTO(pd.BaseModel):
    """User sign in data transfer object.

    Args:
        BaseModel (class): Base pydantic class for models.
    """

    credential: Annotated[
        str, pd.StringConstraints(strip_whitespace=True),
    ]
    password: Annotated[
        str, pd.StringConstraints(strip_whitespace=True),
    ]

    @property
    def credential_is_email(self) -> bool:
        """Check credential is email.

        Returns:
            bool: True if credential is email.
        """
        try:
            pd.validate_email(self.credential)
        except PydanticCustomError:
            return False
        return True


class UserOutDTO(pd.BaseModel):
    """User sign up output data transfer object.

    Args:
        BaseModel (class): Base Pydantic class for models.
    """

    user: UserDTO
    access_token: str
    refresh_token: str
