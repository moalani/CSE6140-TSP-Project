import datetime as dt
import os


class NullTracer:
    def next_result(self, value):
        pass


class MultiRunTracer:
    def __init__(self):
        self._runs = []
        self._reset()

    def _reset(self):
        self._event_log = []
        self._current_best = float('inf')


    def next_result(self, value):
        if value < self._current_best:
            self._current_best = value
            self._event_log.append((dt.datetime.now(), value))

    def next_run(self):
        self._runs.append(self._event_log)
        self._reset()


class Tracer:
    def __init__(self, method, instance, seed, cutoff):
        self.cutoff = cutoff
        self.seed = seed
        self.instance = instance
        self.method = method
        self._event_log = []
        self._current_best = float('inf')

    def next_result(self, value):
        if value < self._current_best:
            self._current_best = value
            self._event_log.append((dt.datetime.now(), value))

    def write_to(self, file_path):
        first_time = self._event_log[0][0]
        full_path = os.path.join(file_path, f'{self.instance}_{self.method}_{self.cutoff}_{self.seed}.trace')
        with open(full_path, 'w') as f:
            for time, value in self._event_log:
                seconds_elapsed = round((time - first_time).total_seconds(), 2)
                f.write(f'{seconds_elapsed}, {value}\n')