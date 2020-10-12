from collections.abc import MutableMapping

from typer import clear

from ee_cli.utils import pretty_delta

class _State:
    times = []

    def reset_times(self):
        clear()
        self.times = []

    def add_time(self, time):
        self.times.append(time)

    @property
    def no_times_set(self):
        return len(self.times) == 0


# should be a store
class UserInputStore(MutableMapping):
    """Provides all user-facing data."""
    def __str__(self):
        """Returns a list formatted to display the transformation (or potentially lack
        thereof) requested by the user"""
        return pre





state = _State()
