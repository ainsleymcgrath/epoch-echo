import pytest

from ee_cli import utils
from ee_cli.constants import COULD_NOT_PARSE_ERROR_MESSAGE
from ee_cli.settings import Settings
from ee_cli.utils import flip_time_format, try_parse_formats


@pytest.fixture
def expected_formatted_list() -> str:
    THREE_SPACES = " " * 3
    return f"\n{THREE_SPACES}foo\n{THREE_SPACES}bar\n{THREE_SPACES}baz\n "


@pytest.mark.parametrize(
    "input, expected",
    [
        ("1602216652", "2020-10-08 23:10:52"),
        ("2020-10-08", "1602133200"),
        ("now", "790495200"),
        ("tomorrow", "790581600"),
        ("yesterday", "790408800"),
        ("pizza", COULD_NOT_PARSE_ERROR_MESSAGE.format(date="pizza")),
    ],
)
def test_flip_format(input, expected):
    actual = flip_time_format(input)
    assert expected == actual


@pytest.fixture
def customized_date_format_for_flip(monkeypatch):
    monkeypatch.setattr(
        utils, "settings", Settings(extra_datetime_input_formats=["[Q]Q YYYY"])
    )
    return "Q1 2020", "1577858400"


def test_flip_format_extra_inputs_set(customized_date_format_for_flip):
    input, expected = customized_date_format_for_flip
    assert expected == flip_time_format(input)


@pytest.mark.parametrize(
    "date, formats, expected",
    [
        ("Q1 2020", ["[Q]Q YYYY"], "1577858400"),
        ("never", [], None),
        ("3rd of January 1922", ["asdfg", "Do [of] MMMM YYYY"], "-1514570400"),
    ],
)
def test_try_parse_formats(date, formats, expected):
    actual = try_parse_formats(date, *formats)
    assert expected == actual
