"""Module with Tokens entities."""

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class IToken(ABC):
    """Abstract representation of a Token entity."""

    @abstractmethod
    def get_encoded_token(self) -> str:
        """Get encoded token.

        Returns:
            str: Json Web Token instance.
        """

    @abstractmethod
    def get_decoded_token(self) -> dict:
        """Get decoded token.

        Returns:
            dict: Token Header and Payload.
        """


class ITokenCreator(ABC):
    """Abstract representation of a Token entity."""

    @abstractmethod
    def create_access_token(self, uid: UUID, *args, **kwargs) -> IToken:
        """Encode new JWT access token.

        Args:
            uid (UUID): User UUID.
            args: Optional arguments for specific implementation.
            kwargs: Optional key-value arguments for specific implementation.

        Returns:
            IToken: Instance of IToken class.
        """

    @abstractmethod
    def create_refresh_token(self, uid: UUID, *args, **kwargs) -> IToken:
        """Encode new JWT refresh token.

        Args:
            uid (UUID): User UUID.
            args: Optional arguments for specific implementation.
            kwargs: Optional key-value arguments for specific implementation.

        Returns:
            IToken: Instance of IToken class.
        """
