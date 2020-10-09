import pytest
from utils import arrange_for_pretty_defaults_abuse


@pytest.fixture
def arranged_list() -> str:
    THREE_SPACES = " " * 3
    return f"\n{THREE_SPACES}foo\n{THREE_SPACES}bar\n{THREE_SPACES}baz\n "


def test_arranging_with_list(arranged_list):
    actual = arrange_for_pretty_defaults_abuse(["foo", "bar", "baz"])
    assert actual == arranged_list


def test_arranging_empty_list():
    actual = arrange_for_pretty_defaults_abuse([])
    assert actual == ""


def test_arranging_with_predicate():
    actual = arrange_for_pretty_defaults_abuse(
        ["fizz!", "buzz"], lambda x: "buzz" not in x
    )
    assert actual == ""


@pytest.mark.parametrize("input, expected, msg", [])
def test_flip_format(input, expected, msg):
    assert 0
