from enum import Enum

class LogLevel(Enum):
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

class ValidationRecord(object):
    def __init__(self, message: str, level: LogLevel):
        self.message = message
        self.level = level
