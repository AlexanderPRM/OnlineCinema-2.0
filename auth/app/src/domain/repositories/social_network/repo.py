"""Module with Social Networks Repository."""

import uuid
from abc import ABC, abstractmethod

from domain.social_network.entities import SocialNetwork


class ISocialNetworkRepository(ABC):
    """Repository with Social Network objects.

    Args:
        ABC (class): Used to create abstract class.
    """

    @abstractmethod
    async def insert(self, entity: SocialNetwork) -> SocialNetwork:
        """Add a new social network.

        Args:
            entity (SocialNetwork): entity of Social Network.

        Returns:
            SocialNetwork (class): New Social Network class
            with new info of created object.
        """

    @abstractmethod
    async def retrieve_by_id(
        self, social_network_id: uuid.UUID,
    ) -> SocialNetwork | None:
        """Retrieve social network by id.

        Args:
            social_network_id (uuid.UUID): Social Network UUID ID.

        Returns:
            SocialNetwork | None: Return Social Network if exists.
        """

    @abstractmethod
    async def retrieve_by_name(self, name: str) -> SocialNetwork | None:
        """Retrieve social network by name.

        Args:
            name (str): Name of social network.

        Returns:
            SocialNetwork: Retrieve Social Network if exists.
        """

    @abstractmethod
    async def change_picture(
        self, social_network_id: uuid.UUID, picture_file_path: str,
    ) -> SocialNetwork:
        """Change a picture of social network to new one.

        Args:
            social_network_id (uuid.UUID): Social Network UUID ID.
            picture_file_path (str):
            File path to new picture of social network.

        Returns:
            SocialNetwork (class): Social Network class
            which represent Social Network.
        """
