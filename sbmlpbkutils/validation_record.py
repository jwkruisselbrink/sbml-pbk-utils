from enum import Enum

class StatusLevel(Enum):
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

class ErrorCode(Enum):
    UNDEFINED = -1
    COMPARTMENT_MISSING_BQM_TERM = 10
    COMPARTMENT_MISSING_PBPKO_BQM_TERM = 11
    COMPARTMENT_MULTIPLE_PBPKO_BQM_TERMS = 12
    COMPARTMENT_INVALID_PBPKO_BQM_TERM = 13
    PARAMETER_MISSING_BQM_TERM = 20
    PARAMETER_MISSING_PBPKO_BQM_TERM = 21
    PARAMETER_MULTIPLE_PBPKO_BQM_TERMS = 22
    PARAMETER_INVALID_PBPKO_BQM_TERM = 23
    SPECIES_MISSING_BQM_TERM = 30
    SPECIES_MISSING_PBPKO_BQM_TERM = 31
    SPECIES_MULTIPLE_PBPKO_BQM_TERMS = 32
    SPECIES_INVALID_PBPKO_BQM_TERM = 33

class ValidationRecord(object):
    def __init__(
        self,
        level: StatusLevel,
        code: ErrorCode,
        message: str
    ):
        self.level = level
        self.message = message
        self.code = code
