from enum import Enum

class StatusLevel(Enum):
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

class ValidationRecord(object):
    def __init__(self, level: StatusLevel, message: str):
        self.level = level
        self.message = message
