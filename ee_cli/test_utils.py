import pytest
from ee_cli.utils import flip_time_format, pretty_delta


@pytest.fixture
def expected_formatted_list() -> str:
    THREE_SPACES = " " * 3
    return f"\n{THREE_SPACES}foo\n{THREE_SPACES}bar\n{THREE_SPACES}baz\n "


def test_pretty_delta_with_list(expected_formatted_list):
    actual = pretty_delta(["foo", "bar", "baz"])
    assert actual == expected_formatted_list


def test_pretty_delta_empty_list():
    actual = pretty_delta([])
    assert actual == ""


def test_pretty_delta_with_predicate():
    actual = pretty_delta(
        ["fizz!", "buzz"], lambda x: "buzz" not in x
    )
    assert actual == ""


@pytest.mark.parametrize(
    "input, expected",
    [
        ("1602216652", "Thu, Oct 8 2020 23:10:52"),
        ("2020-10-09", "1602201600"),
        # ("now", ""),
        # ("tomorrow", ""),
        # ("yesterday", ""),
    ],
)
def test_flip_format(input, expected):
    actual = flip_time_format(input)
    assert expected == actual
