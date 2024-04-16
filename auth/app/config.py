"""Module with project configuration."""

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseServiceSettings(BaseSettings):
    """Base meta config for Settings."""

    model_config = SettingsConfigDict(
        env_file=('.env', '.env.prod'),
        extra='ignore',
        case_sensitive=True,
    )


class UserSettings(BaseServiceSettings):
    """User Configuration.

    Args:
        BaseSettings (class): Base Pydantic class for Settings.
    """

    default_user_role: str


class PostgreSQLSettings(BaseServiceSettings):
    """Database Configuration.

    Args:
        BaseSettings (class): Base Pydantic class for Settings.
    """

    db_driver: str
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    db_schema: str


class RedisSettings(BaseServiceSettings):
    """Redis Configuration.

    Args:
        BaseSettings (class): Base Pydantic class for Settings.
    """

    redis_host: str
    redis_port: int
    redis_user: str
    redis_password: str
    max_connections: int


class TokensSettings(BaseServiceSettings):
    """Tokens Configuration.

    Args:
        BaseSettings (class): Base Pydantic class for Settings.
    """

    jwt_secret: str
    encryption_algorithm: str
    access_token_expiration: int
    refresh_token_expiration: int


class ProjectSettings(BaseModel):
    """Project configuration.

    Args:
        BaseModel (class): Base Pydantic class for Models.
    """

    user_settings: UserSettings = UserSettings()
    postgresql_settings: PostgreSQLSettings = PostgreSQLSettings()
    redis_settings: RedisSettings = RedisSettings()
    tokens_settings: TokensSettings = TokensSettings()
