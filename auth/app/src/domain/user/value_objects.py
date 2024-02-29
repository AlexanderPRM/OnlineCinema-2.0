"""Module with User value objects."""

from datetime import date
from typing import Annotated, Optional

import pydantic as pd
from src.domain.user.exceptions import ModelFieldsAreNotSpecified


class UserAdditionalFields(pd.BaseModel):
    """Model with additional user profile fields.

    Args:
        pd.BaseModel (class): Base class for pydantic validations models.
    """

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

    @pd.model_validator(mode='after')
    def check_additional_fields_are_specified(self) -> 'UserAdditionalFields':
        """At least one additional field must be filled.

        Raises:
            ModelFieldsAreNotSpecified: Custom Exception.

        Returns:
            UserAdditionalFields: Model class.
        """
        if not self.model_fields_set:
            raise ModelFieldsAreNotSpecified(
                'No one additional user field are specified.',
            )
        return self
