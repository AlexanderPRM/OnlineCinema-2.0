"""Module with social network DTO."""

from typing import Optional

import pydantic as pd
from domain.base import BaseDTO


class SocialNetworkDTO(BaseDTO):
    """Model which describe social network object.

    Args:
        BaseDTO (class): Parent class with common fields for DTO models.
    """

    picture: Optional[pd.FilePath] = None
    name: str
