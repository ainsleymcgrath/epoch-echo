from typing import Callable, List, Tuple
from collections.abc import MutableSequence

from typer import clear

from ee_cli.utils import flip_time_format, mangled_prompt_default


class UserInputTransformationStore(MutableSequence):
    """Provides all user-facing data."""

    def __init__(self, *items):
        # maybe should take format stuff as well
        self._list = list(items)

    def __str__(self):
        """Returns a list formatted to display the transformation (or potentially lack
        thereof) requested by the user"""
        return mangled_prompt_default(self)

    def __getitem__(self, key):
        return f"{self._list[int(key)]} => {flip_time_format(self._list[int(key)])}"

    def __setitem__(self, key, value):
        self._list[int(key)] = value

    def __delitem__(self, key):
        try:
            del self._list[int(key)]  # dispatcher sends a string when user requests drop
        except IndexError:
            pass

    def __iter__(self):
        """__getitem__ already knows how to format list items."""
        return (self.__getitem__(i) for i, _ in enumerate(self._list))

    def __len__(self):
        return len(self._list)

    def insert(self, index, value):
        self._list.insert(index, value)


def make_dispatcher(*args: Tuple[List[str], Callable], default=None):
    """Returns a function that takes a string. If the string is in one of the lists
    that was passed here along with some function, then that function is called.

    If a default is passed, it will be called with the string input passed to the
    dispatcher"""

    switch = {action: fn for actions, fn in args for action in actions}

    def _dispatcher(action: str):
        action, *args = action.split(" ")

        if action in switch:
            switch[action](*args)
            return

        if default is not None:
            default(action)  # treat the action as input for the default fn

    return _dispatcher
