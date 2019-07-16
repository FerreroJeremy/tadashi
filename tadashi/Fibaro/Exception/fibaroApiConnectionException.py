from .fibaroException import FibaroException


class FibaroApiConnectionException(FibaroException):
    def __init__(self, reason=''):
        self.reason = reason

    def __str__(self):
        return self.reason
