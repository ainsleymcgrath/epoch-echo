"""UI state management."""
from collections.abc import MutableSequence
from textwrap import indent
from typing import Callable, List, Tuple

from ee_cli.utils import flip_time_format


class UserInputTransformationStore(MutableSequence):
    """Provides all user-facing data."""

    def __init__(self, *items):
        """Make 2 identical lists. Original is for history, working is for display."""
        self._original_list = list(items)
        self._working_list = list(items)

    def __str__(self):
        """Arrange the items in a list and indent to look nice in the prompt."""
        linewise_list = "\n".join(i for i in self._working_list)
        return indent(f"\n{linewise_list}\n ", "   ")

    def __getitem__(self, idx):
        # noqa: D208, D400
        """Return the formatted self._list element at the given index."""
        original = self._working_list[int(idx)]
        flipped = flip_time_format(original)
        return f"{original} => {flipped}"

    def __setitem__(self, idx, value):
        """Do it the regular way."""
        self._working_list[int(idx)] = value

    def __delitem__(self, idx):
        """Delete an item from the self.working_list only.
        self._full_list isn't touched so we can preserve input history."""
        try:
            del self._working_list[int(idx)]
        except IndexError:
            pass

    def __iter__(self):
        """Give back all the elements of self.working_list, formatted.
        __getitem__ already knows how to format list items."""
        return (self.__getitem__(i) for i, _ in enumerate(self._working_list))

    def __len__(self):
        """Do it the regular way."""
        return len(self._working_list)

    def insert(self, idx, value):
        """Set the original and working list so the former can be used for history."""
        for list in [self._original_list, self._working_list]:
            list.insert(idx, value)  # no str() bc caller uses this like a normal list


def make_dispatcher(*args: Tuple[List[str], Callable], default=None):
    """Return a function that takes a string. Put *args in a closure for it to use.

    Any member of a list of strings in any of *args will trigger the invocation of the
    corresponding callable. If a default fn is passed, it will be called with any
    input passed to the dispatcher that is not in the closure, unaltered."""
    switch = {action: fn for actions, fn in args for action in actions}

    def _dispatcher(action: str):
        """Affect external state, presumably. Do what you want I guess.
        The first word of the string is potentially an action named in one of the
        lists passed into the closure. The remaining words are passed to the action
        callable if they are present."""
        key, *args = action.split(" ")

        if key in switch:
            switch[key](*args)
            return

        if default is not None:
            default(action)

    return _dispatcher
