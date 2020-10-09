from typer import clear


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


state = _State()
