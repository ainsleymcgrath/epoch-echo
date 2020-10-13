# should format when there are inputs
# should show a default when not
# should show indexes when asked
# should show help when asked

import pytest

from ee_cli.ui import UserInputTransformationStore, make_dispatcher


class StatefulObject:
    value = 0

    def five(self):
        self.value = 5

    def double(self, num):
        self.value = int(num) * 2

    def sum(self, *args):
        self.value = sum(map(int, args))

    def set(self, num):
        self.value = num


obj = StatefulObject()


@pytest.fixture
def basic_dispatcher():
    return make_dispatcher(
        [("5", "do-5"), obj.five],
        [("2x",), obj.double],
        [("+",), obj.sum],
        default=obj.set,
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
def test_dispatcher(action, expected_obj_value, basic_dispatcher):
    basic_dispatcher(action)
    assert obj.value == expected_obj_value
