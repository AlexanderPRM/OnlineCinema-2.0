"""Module with project configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class UserSettings(BaseSettings):
    """User Configuration.

    Args:
        BaseSettings (class): Base Pydantic class for Settings.
    """

    model_config = SettingsConfigDict(
        env_file=('.env', '.env.prod'),
        extra='ignore',
    )

    default_user_role: str


class DatabaseSettings(BaseSettings):
    """Database Configuration.

    Args:
        BaseSettings (class): Base Pydantic class for Settings.
    """

    model_config = SettingsConfigDict(
        env_file=('.env', '.env.prod'),
        extra='ignore',
    )

    db_driver: str
    db_host: str
    db_port: str
    db_user: str
    db_password: str
    db_name: str
    db_schema: str


user_config = UserSettings()
database_config = DatabaseSettings()
