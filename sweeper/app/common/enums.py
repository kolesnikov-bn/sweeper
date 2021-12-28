from enum import Enum, IntEnum

STATUSES = {0: "OK", 1: "ERROR"}


class StatusEnum(Enum):
    ok = 0
    error = 1


class Priority(IntEnum):
    low = 1
    normal = 5
    high = 9
