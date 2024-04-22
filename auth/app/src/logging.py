"""Module with logging configuration."""

from src.config import LoggingSettings

config = LoggingSettings()


def get_logging_config() -> dict:
    """Return logging configuration.

    Returns:
        dict: Logging Configuration.
    """
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                'format': '%(name)s - %(asctime)s - %(levelname)s - '
                + '%(filename)s:%(lineno)d:%(funcName)s - %(message)s',
                'datefmt': '%Y-%m-%dT%H:%M:%SZ',
                'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            },
        },
        'handlers': {
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'maxBytes': 5242880,
                'backupCount': 10,
                'level': 'INFO',
                'formatter': 'json',
                'filename': 'logs/application.log',
            },
        },
        'loggers': {
            '': {
                'handlers': ['file'],
                'level': config.logging_level,
                'propagate': False,
            },
        },
    }
