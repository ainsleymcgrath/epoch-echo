"""Globally shared test resources."""

import pendulum
import pytest
from ee_cli.settings import Settings


@pytest.fixture(autouse=True)
def today_is_my_birthday():
    """In every test, it's my birthday. For real."""
    settings = Settings()
    my_birthday = pendulum.datetime(1995, 1, 19, tz=settings.default_timezone)
    pendulum.set_test_now(my_birthday)
