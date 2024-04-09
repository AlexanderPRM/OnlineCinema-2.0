"""Module with Key schema for Redis."""

import uuid
from typing import Optional

from src.use_cases.interfaces.tokens.entities import IToken

DEFAULT_KEY_PREFIX = 'auth:jwt-tokens'


def prefixed_key(func):
    """Add prefix to key.

    Args:
        func: Function which return key.

    Returns:
        wrapper: Result key.
    """
    def wrapper(self, *args, **kwargs):
        key = func(self, *args, **kwargs)
        return '{prefix}:{key}'.format(prefix=self.prefix, key=key)

    return wrapper


class KeySchema:  # noqa: WPS306 (Without Base class.)
    """Methods to generate key names for Redis."""

    def __init__(self, prefix: Optional[str] = DEFAULT_KEY_PREFIX):
        """Init method.

        Args:
            prefix (str, optional):
            Some prefix. Defaults to DEFAULT_KEY_PREFIX.
        """
        self.prefix = prefix

    @prefixed_key
    def user_access_token(self, uid: uuid.UUID, access_token: IToken):
        """Get key for user access token.

        Args:
            uid (uuid.UUID): User UUID.
            access_token (IToken): Access Json Web Token.

        Returns:
            str: Result key.
        """
        return '{0}:{1}:{2}'.format(
            'access-token', str(uid), access_token.get_encoded_token(),
        )

    @prefixed_key
    def user_refresh_token(self, uid: uuid.UUID, refresh_token: IToken):
        """Get key for user refresh token.

        Args:
            uid (uuid.UUID): User UUID.
            refresh_token (IToken): Refresh Json Web Token.

        Returns:
            str: Result key.
        """
        return '{0}:{1}:{2}'.format(
            'refresh-token', str(uid), refresh_token.get_encoded_token(),
        )
