from enum import Enum
from dataclasses import dataclass


class TaskStatus(Enum):
    COMPLETED = "completed"
    ACTIVE = "active"
    PENDING = "pending"


class OutputType(Enum):
    PLAIN = "plain"
    JSON = "json"


class ActionStatus(Enum):
    INTEGRITY_ERROR = "DUPLICATE_ERROR"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    NOT_FOUND = "NOT_FOUND"


@dataclass
class Task:
    task_id: str
    title: str
    shorthand_title: str | None
    content: str
    tags: str
    status: TaskStatus
    created_at: str
    updated_at: str

    @property
    def json(self) -> dict:
        """
        :return: Retrieves the JSON representation of the task
        """
        return {
            "task_id": self.task_id,
            "title": self.title,
            "shorthand_title": self.shorthand_title,
            "content": self.content,
            "tags": self.tags,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @property
    def plain(self) -> str:
        """
        :return: Returns the plain text representation of the task
        """
        return (f"ID: {self.task_id}\nTitle: {self.title}\nTags: {",".join(x.title() for x in self.tags.split(','))}\n"
                f"Created At: {self.created_at}\nUpdated At: {self.updated_at}\nContent: \n{self.content}")