"""Module with User class."""

from __future__ import annotations

from datetime import UTC, datetime

from src.domain.base import Base
from src.domain.user.dto import UserDTO
from src.domain.user.value_objects import UserAdditionalFields
from src.domain.user_service.entities import UserService


class User(Base):
    """Class which represent a User.

    Args:
        Base (class): Base representing class.
    """

    def __init__(
        self, entity: UserDTO, user_service: UserService,
    ) -> None:
        """Init method.

        Args:
            entity (UserDTO): Data Transfer Object of User.
            user_service (UserService): Entity of User Service.

        """
        self.id = entity.id

        self._email = entity.email
        self._login = entity.login
        self._password = entity.password
        self._user_service_id = entity.user_service_id
        self._full_name = entity.full_name
        self._profile_picture = entity.profile_picture
        self._birthday = entity.birthday
        self._phone_number = entity.phone_number
        self._bio = entity.bio
        self._created_at = entity.created_at
        self._updated_at = entity.updated_at

        self.user_service = user_service

    @classmethod
    def create(
        cls,
        email: str,
        login: str,
        password: str,
        user_service: UserService,
    ) -> User:
        """Create User class which represent a user object.

        Args:
            email (str): User email.
            login (str): User login.
            password (str): User password.
            user_service (UserService): entity of UserService.

        Returns:
            User (class): Return created class.
        """
        return cls(
            entity=UserDTO(
                id=user_service.id,
                email=email,
                login=login,
                password=password,
                user_service_id=user_service.id,
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
            ),
            user_service=user_service,
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

    def as_dto(self) -> UserDTO:
        """Get user info as DTO.

        Returns:
            UserDTO: Instance of User data transfer object.
        """
        return UserDTO(
            id=self.id,
            email=self._email,
            login=self._login,
            password=self._password,
            user_service_id=self._user_service_id,
            full_name=self._full_name,
            profile_picture=self._profile_picture,
            birthday=self._birthday,
            phone_number=self._phone_number,
            bio=self._bio,
            created_at=self._created_at,
            updated_at=self._updated_at,
        )
