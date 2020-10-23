"""Globally shared test resources."""
from dataclasses import dataclass

import pendulum
import pytest
from ee_cli.settings import Settings


@pytest.fixture(autouse=True)
def today_is_my_birthday():
    """In every test, it's my birthday. For real."""
    settings = Settings()
    my_birthday = pendulum.datetime(1995, 1, 19, tz=settings.default_timezone)
    pendulum.set_test_now(my_birthday)


@pytest.fixture(autouse=True)
def pyperclip_patch(monkeypatch):
    """While pyperclip works ok locally, it freaks out in CircleCI."""

    @dataclass
    class ClipboardStub:
        clipped: str = ""

        def copy(self, text):
            self.clipped = text

        def paste(self):
            return self.clipped

    stub = ClipboardStub()  # share the instance across patches

    monkeypatch.setattr("ee_cli.main.pyperclip", stub)
    monkeypatch.setattr("ee_cli.test_ee.pyperclip", stub)
