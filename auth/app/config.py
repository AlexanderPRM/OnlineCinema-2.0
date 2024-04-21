"""Module with project configuration."""

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseServiceSettings(BaseSettings):
    """Base meta config for Settings.

    Args:
        BaseSettings (class): Base Pydantic class for Settings
    """

    model_config = SettingsConfigDict(
        env_file=('.env', '.env.prod'),
        extra='ignore',
        case_sensitive=True,
    )


class LoggingSettings(BaseServiceSettings):
    """Logging configuration."""

    use_sentry: bool
    sentry_dsn: str


class APISettings(BaseServiceSettings):
    """API configuration."""

    production: bool
    api_title: str
    api_version: str


class UserSettings(BaseServiceSettings):
    """User Configuration."""

    default_user_role: str


class PostgreSQLSettings(BaseServiceSettings):
    """Database Configuration."""

    db_driver: str
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    db_schema: str


class RedisSettings(BaseServiceSettings):
    """Redis Configuration."""

    redis_host: str
    redis_port: int
    redis_user: str
    redis_password: str
    max_connections: int


class TokensSettings(BaseServiceSettings):
    """Tokens Configuration."""

    jwt_secret: str
    encryption_algorithm: str
    access_token_expiration: int
    refresh_token_expiration: int


class ProjectSettings(BaseModel):
    """Project configuration."""

    user_settings: UserSettings = UserSettings()
    postgresql_settings: PostgreSQLSettings = PostgreSQLSettings()
    redis_settings: RedisSettings = RedisSettings()
    tokens_settings: TokensSettings = TokensSettings()
