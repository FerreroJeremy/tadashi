from .dataConversionException import DataConversionException


class BadArgumentTypeException(DataConversionException):
    def __init__(self, reason=''):
        self.reason = reason

    def __str__(self):
        return self.reason
