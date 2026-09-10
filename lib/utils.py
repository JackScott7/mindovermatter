from enum import Enum
from dataclasses import dataclass
from uuid import UUID


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
        return (
            f"ID: {self.task_id}"
            f"\nStatus: {self.status}"
            f"\nTitle: {self.title}\nTags: {",".join(x.title() for x in self.tags.split(','))}"
            f"\nCreated At: {self.created_at}"
            f"\nUpdated At: {self.updated_at}"
            f"\nContent: "
            f"\n{self.content}"
        )


@dataclass
class SearchResult:
    task_id: str
    title: str
    tags: str
    updated_at: str


def is_valid_uuid4(string: str) -> bool:
    try:
        parsed = UUID(string, version=4)
        return True if parsed.version == 4 else False
    except ValueError:
        return False
