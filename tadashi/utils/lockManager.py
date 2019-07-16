import time
from enum import Enum


class LockState(Enum):
    REJECTED = 0
    GOT = 1
    ALREADY_OWN = 2


class LockManager:

    def __init__(self, seconds):
        self.lock_life_duration = seconds
        self._last_attribution = 0
        self._owner = None

    def has_lock(self, applicant):
        if self.is_expired():
            self._last_attribution = time.time()
            self._owner = applicant
            return LockState.GOT
        else:
            if self._owner == applicant:
                return LockState.ALREADY_OWN
            else:
                return LockState.REJECTED

    def is_expired(self):
        if time.time() >= self._last_attribution + self.lock_life_duration:
            return True
        else:
            return False
