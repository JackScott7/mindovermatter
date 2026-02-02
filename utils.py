from enum import Enum


class TaskStatus(Enum):
    COMPLETED = "COMPLETED"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"


class TaskReadType(Enum):
    PLAIN = "PLAIN"
    JSON = "JSON"
