# should format when there are inputs
# should show a default when not
# should show indexes when asked
# should show help when asked

import pytest

from ee_cli.ui import EchoList, OptionallyLatentString, make_dispatcher
from ee_cli.utils import flip_time_format


@pytest.fixture
def stateful_object():
    class StatefulObject:
        """To test the dispatcher against."""

        value = 0

        def five(self):
            self.value = 5

        def double(self, num):
            self.value = int(num) * 2

        def sum(self, *args):
            self.value = sum(map(int, args))

        def set(self, num):
            self.value = num

    return StatefulObject()


@pytest.fixture
def basic_dispatcher(stateful_object):
    return make_dispatcher(
        [("5", "do-5"), stateful_object.five],
        [("2x",), stateful_object.double],
        [("+",), stateful_object.sum],
        default=stateful_object.set,
    )


@pytest.mark.parametrize(
    "action, expected_obj_value",
    [
        ("5", 5),
        ("do-5", 5),
        ("2x 4", 8),
        ("lovely weather today", "lovely weather today"),
        ("+ 1 2 3", 6),
    ],
)
def test_dispatcher(action, expected_obj_value, basic_dispatcher, stateful_object):
    basic_dispatcher(action)
    assert stateful_object.value == expected_obj_value


@pytest.mark.parametrize(
    "latent_str, expected",
    [
        (OptionallyLatentString("Can you see me?"), ""),
        (OptionallyLatentString("What about me?", latent=False), "What about me?"),
    ],
)
def test_latent_string_latent_by_default(latent_str, expected):
    assert (
        latent_str == expected
    ), "String displayes _content as __repr__ based on latent kwarg"


@pytest.fixture
def ui_store():
    return EchoList(1, 2, 3)


def test_delete_items_from_store(ui_store):
    # the item comes out formatted, so we just want the first char,
    # which is the 'unformatted' value
    deleted_item = int(ui_store.pop()[0])

    assert (
        deleted_item not in ui_store
    ), "Deleted items appear not to be in the ui_store"
    try:
        del ui_store[200]
    except IndexError:
        pytest.fail("EchoList doesn't care about its indexes.")


def test_getitem_does_format(ui_store):
    expected = flip_time_format(ui_store._items[0])
    actual = ui_store[0]
    assert expected in actual, "Formatted string included in getitem"
