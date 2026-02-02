from enum import Enum


class Task:
    def __init__(self, content, title, shorthand_title, task_id, tags):
        self.content = content
        self.title = title
        self.shorthand_title = shorthand_title
        self.task_id = task_id
        self.tags = tags


class TaskStatus(Enum):
    COMPLETED = "COMPLETED"
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"


class TaskReadType(Enum):
    PLAIN = "PLAIN"
    JSON = "JSON"


class ActionStatus(Enum):
    INTEGRITY_ERROR = "DUPLICATE_ERROR"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    NOT_FOUND = "NOT_FOUND"
