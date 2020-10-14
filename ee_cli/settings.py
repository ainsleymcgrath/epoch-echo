"""Wrap up environment variable based configuration and set defaults."""
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Specification of env variables that allow user customization."""

    default_timezone: str = "America/Chicago"
    custom_datetime_output_format: str = ""
    extra_datetime_input_formats: List[str] = []
    show_indexes_always: bool = False
