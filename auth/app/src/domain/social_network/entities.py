"""Module with Social Network class."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from pathlib import Path

from src.domain.base import Base
from src.domain.social_network.dto import SocialNetworkDTO


class SocialNetwork(Base):
    """Class which represent a Social Network.

    Args:
        Base (class): Base representing class.
    """

    def __init__(self, entity: SocialNetworkDTO) -> None:
        """Init method.

        Args:
            entity (SocialNetworkDTO): Data Transfer Object of Social Network.
        """
        self.id = entity.id

        self._picture = entity.picture
        self._name = entity.name
        self._created_at = entity.created_at
        self._updated_at = entity.updated_at

    @classmethod
    def create(cls, picture_file_path: Path, name: str) -> SocialNetwork:
        """Create Social Network class which represent a social network.

        Args:
            picture_file_path (Path): File path to social network icon.
            name (str): Social Network name.

        Returns:
            SocialNetwork (class): Return created class.
        """
        return cls(
            entity=SocialNetworkDTO(
                id=uuid.uuid4(),
                picture=picture_file_path,
                name=name,
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
            ),
        )

    def change_picture(self, picture_file_path: Path) -> None:
        """Change social network icon.

        Args:
            picture_file_path (Path): File path to new social network icon.
        """
        self._picture = picture_file_path
