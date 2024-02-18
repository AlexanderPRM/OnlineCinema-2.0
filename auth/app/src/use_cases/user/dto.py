"""Module with DTO's for User Use cases."""

from typing import Annotated

import pydantic as pd


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
