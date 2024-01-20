"""Module with Project settings."""

import typing

from pydantic import StringConstraints
from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseSettings):
    """Class with settings for API.

    Args:
        BaseSettings (class): Base pydantic class for settings classes.
    """

    model_config = SettingsConfigDict(
        env_file=('.env.prod', '.env'),
        extra='ignore',
    )
    production: bool
    api_title: str
    api_version: typing.Annotated[str, StringConstraints(
        strip_whitespace=True,
        pattern=r'\d+.\d+.\d+',
        ),
    ]
    api_summary: str
    api_description: str

    relational_db: str


class DatabaseSettings(BaseSettings):
    """Class with Database settings.

    Args:
        BaseSettings (class):  Base pydantic class for settings classes.
    """

    model_config = SettingsConfigDict(
        env_file=('.env.prod', '.env'),
        extra='ignore',
    )
    postgres_user: str
    postgres_password: str
    postgres_host: typing.Annotated[str, StringConstraints(
        strip_whitespace=True,
        max_length=60,
        ),
    ]
    postgres_port: str
    postgres_db: str

    redis_host: typing.Annotated[str, StringConstraints(
        strip_whitespace=True,
        max_length=60,
        ),
    ]
    redis_port: str
    redis_password: str


api_settings = APISettings()
database_settings = DatabaseSettings()
