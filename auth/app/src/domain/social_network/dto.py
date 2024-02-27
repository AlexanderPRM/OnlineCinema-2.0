"""Module with social network DTO."""

from datetime import datetime
from typing import Annotated, Optional

import pydantic as pd
from domain.base import BaseDTO


class SocialNetworkDTO(BaseDTO):
    """Model which describe social network object.

    Args:
        BaseDTO (class): Parent class with common fields for DTO models.
    """

    picture: Optional[pd.FilePath] = None
    name: Annotated[
        str, pd.StringConstraints(strip_whitespace=True, max_length=24),
    ]
    created_at: datetime
    updated_at: datetime
