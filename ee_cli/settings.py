"""Wrap up environment variable based configuration and set defaults."""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Specification of env variables that allow user customization."""

    default_timezone: str = "America/Chicago"
    default_datetime_output_format: str = None
    extra_datetime_input_format: str = None
    show_indexes_always: bool = False
