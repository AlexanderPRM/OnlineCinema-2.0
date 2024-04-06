"""Module with DTO's for User Use cases."""

from __future__ import annotations

from typing import Annotated

import pydantic as pd
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserSignUpDTO(pd.BaseModel):
    """User sign up DTO.

    Args:
        BaseModel (class): Base Pydantic model for.
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
