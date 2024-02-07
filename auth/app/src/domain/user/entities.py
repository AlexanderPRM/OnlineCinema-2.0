"""Module with User class."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from domain.base import Base
from domain.user.dto import UserDTO
from domain.user.value_objects import UserAdditionalFields


class User(Base):
    """Class which represent a User.

    Args:
        Base (class): Base representing class.
    """

    def __init__(self, entity: UserDTO) -> None:
        """Init method.

        Args:
            entity (UserDTO): Data Transfer Object of User.

        """
        self._id = entity.id
        self._email = entity.email
        self._login = entity.login
        self._password = entity.password
        self._full_name = entity.full_name
        self._profile_picture = entity.profile_picture
        self._birthday = entity.birthday
        self._phone_number = entity.phone_number
        self._bio = entity.bio
        self._updated_at = entity.updated_at

    @classmethod
    def create(
        cls,
        email: str,
        login: str,
        password: str,
        user_service_id: uuid.UUID,
    ) -> User:
        """Create User class which represent a user object.

        Args:
            email (str): User email.
            login (str): User login.
            password (str): User password.
            user_service_id (UUID): UUID identifier to user service.

        Returns:
            User (class): Return created class.
        """
        return cls(
            entity=UserDTO(
                id=uuid.uuid4(),
                email=email,
                login=login,
                password=password,
                user_service_id=user_service_id,
                updated_at=datetime.now(UTC),
            ),
        )

    def change_email(self, email: str) -> None:
        """Change User email.

        Args:
            email (str): New User electronic mail.
        """
        self._email = email

    def change_login(self, login: str) -> None:
        """Change User login.

        Args:
            login (str): New User login.
        """
        self._login = login

    def change_password(self, password: str) -> None:
        """Change User password.

        Args:
            password (str): New User password.
        """
        self._password = password

    def change_additional_info(
        self, additional_fields: UserAdditionalFields,
    ) -> None:
        """Change User additional fields.

            For example, fields like:
                - full name
                - birthday
                - phone number

        Args:
            additional_fields (UserAdditionalFields): Changed new fields.
        """
        fields_in_dict = additional_fields.model_dump()
        fields_set = additional_fields.model_fields_set
        for field in fields_set:
            class_field = '_{0}'.format(field)
            self.__dict__[class_field] = fields_in_dict[field]
