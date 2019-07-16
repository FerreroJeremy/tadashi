import time


class PeriodicallyProcessor:
    TIME_BETWEEN_TWO_PROCESS = 5  # seconds

    def __init__(self):
        self._last_update = 0

    def process(self, method):
        while True:
            if self.can_it_be_process():
                method(time.time())
                self._last_update = time.time()

    def get_remaining_time_before_reprocess(self):
        return self._last_update + self.TIME_BETWEEN_TWO_PROCESS - time.time()

    def can_it_be_process(self):
        if self.get_remaining_time_before_reprocess() <= 0:
            return True
        else:
            return False
