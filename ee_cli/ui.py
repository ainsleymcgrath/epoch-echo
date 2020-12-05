"""Stateful objects for displaying in repl UI.
Dispatcher-cerator for building ways to alter them."""
from collections.abc import MutableSequence, Sized
from textwrap import indent
from typing import Any, Callable, Dict, Set, Tuple

from ee_cli.settings import Settings
from ee_cli.utils import flip_time_format

settings = Settings()


class EchoList(MutableSequence):
    """Access transformed/formatted versions of the items passed into __init__.
    When accessing an item via index or when iterating on an instance, the members are
    formatted with `flip_time_format` when returned."""

    def __init__(self, *items: str):
        self._items = list(items)
        self.show_index: bool = settings.show_indexes_always

    def __str__(self):
        """Arrange the items in a list and indent to look nice in the prompt."""
        linewise_list = "\n".join(self)
        return indent(f"\n{linewise_list}\n ", "   ")

    def __getitem__(self, idx):
        """Return the formatted self._list element at the given index."""
        original = self._items[int(idx)]
        flipped = flip_time_format(original)
        maybe_index = f"{idx} : " if self.show_index else ""
        return f"{maybe_index}{original} => {flipped}"

    def __setitem__(self, idx, value):
        """Do it the regular way."""
        self._items[int(idx)] = value

    def __delitem__(self, idx):
        """Delete an item, but be apathetic about nonexistent indices.
        Since this is used only by main._repl, idx is a string."""
        try:
            del self._items[int(idx)]
        except IndexError:
            pass

    def __iter__(self):
        """Give back all the elements, formatted.
        __getitem__ knows how to format list items, so use indexes."""
        return (self[i] for i, _ in enumerate(self._items))

    def __len__(self):
        """Do it the regular way."""
        return len(self._items)

    def insert(self, idx: int, value):
        """Set the original and working list so the former can be used for history."""
        self._items.insert(idx, value)

    def plain_str(self) -> str:
        """Provide transformed values as a printable list without formatting.
        Use ._items since iterating on self gives formatted strings."""
        return "\n".join(flip_time_format(s) for s in self._items)


def make_dispatcher(
    *args: Tuple[Set[str], Callable], default=None
) -> Callable[[str], None]:
    """Return a function that takes a string. Put *args in a closure for it to use.

    Any member of a set of strings in any of *args will trigger the invocation of the
    corresponding callable. If a default fn is passed, it will be called with any
    input passed to the dispatcher that is not in the closure, unaltered."""
    switch: Dict[str, Callable] = {
        action: fn for actions, fn in args for action in actions
    }

    def _dispatcher(action: str) -> None:
        """Affect external state, presumably. Do what you want I guess.
        The first word of the string is potentially an action named in one of the
        lists passed into the closure. The remaining words are passed to the action
        callable as arguments if they are present."""
        try:
            key, *args = action.split(" ")
        except AttributeError:
            # when it's not a string or adequately string-ish, it's MEANINGLESS TO US
            return

        if key in switch:
            switch[key](*args)
            return

        if default is not None:
            default(action)

    return _dispatcher


class OptionallyLatentString(Sized):
    """A string-ish object that is 'latent' on initialization.
    When self.latent == True, then str(self) == "".
    """

    latent: bool

    def __init__(self, _content: str, latent=True):
        self._content = _content
        self.latent = latent

    def __str__(self) -> str:
        return self._content if not self.latent else ""

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: Any) -> bool:
        return str(self) == str(other)

    def __len__(self) -> int:
        return len(str(self))
