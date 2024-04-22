"""Module with Tokens entities."""

from __future__ import annotations

import time
from uuid import UUID

from jose import jwt
from src.config import TokensSettings
from src.use_cases.interfaces.tokens.entities import IToken, ITokenCreator


class Token(IToken):
    """Representation of a Token entity."""

    def __init__(self, token: str, config: TokensSettings) -> None:
        """Init method.

        Args:
            token (str): Json Web Token.
            config (TokensSettings): Settigns for JWT Tokens.
        """
        self.token = token
        self.config = config

    def get_encoded_token(self) -> str:
        """Get encoded token.

        Returns:
            str: Json Web Token instance.
        """
        return self.token

    def get_decoded_token(self) -> dict:
        """Get decoded token.

        Returns:
            dict: Token Header and Payload.
        """
        return jwt.decode(
            self.token,
            self.config.jwt_secret,
            algorithms=self.config.encryption_algorithm,
        )


class TokenCreator(ITokenCreator):
    """Abstract representation of a Token entity."""

    def __init__(self, config: TokensSettings) -> None:
        """Init method.

        Args:
            config (TokensSettings): Settings for JWT tokens.
        """
        self.config = config

    def create_access_token(self, uid: UUID, *args, **kwargs) -> Token:
        """Encode new JWT access token.

        Args:
            uid (UUID): User UUID.
            args: Optional arguments for specific implementation.
            kwargs: Optional key-value arguments for specific implementation.

        Returns:
            Token: Instance of Token class.
        """
        to_encode = {
            'uid': str(uid),
            'exp': time.time() + self.config.access_token_expiration,
        }
        to_encode.update(kwargs)
        access_token = jwt.encode(
            to_encode,
            self.config.jwt_secret,
            algorithm=self.config.encryption_algorithm,
        )
        return Token(
            access_token, self.config,
        )

    def create_refresh_token(self, uid: UUID, *args, **kwargs) -> Token:
        """Encode new JWT refresh token.

        Args:
            uid (UUID): User UUID.
            args: Optional arguments for specific implementation.
            kwargs: Optional key-value arguments for specific implementation.

        Returns:
            Token: Instance of Token class.
        """
        to_encode = {
            'uid': str(uid),
            'exp': time.time() + self.config.refresh_token_expiration,
        }
        access_token = jwt.encode(
            to_encode,
            self.config.jwt_secret,
            algorithm=self.config.encryption_algorithm,
        )
        return Token(
            access_token, self.config,
        )
