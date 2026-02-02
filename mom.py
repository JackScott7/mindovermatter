import os
import uuid
from typing import LiteralString, Literal

import typer
from db import Database
from utils import TaskStatus, TaskReadType

app = typer.Typer(name="MindOverMatter", add_completion=True, pretty_exceptions_enable=True)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = os.getenv("MOM_DATABASE_URL", os.path.join(BASE_DIR, "mom.db"))
db = Database(DATABASE_URL)


@app.command()
def add(content: str,
        title: str,
        shorthand_title: str = None,
        task_id: uuid.UUID = uuid.uuid4(),
        tags: list[str] = None) -> None:
    """
    Add a new task

    :param content: task content

    :param title: title of your liking

    :param shorthand_title: pass in shorthand title of your liking to this task,
        you can open this task later with this shorthand instead of the taskID

    :param task_id: pass in a UUID, or let the CLI generate one for you

    :param tags: command separated string of tags for this task

    :return: A Task object
    """
    db.add_task(content, title, shorthand_title, task_id, tags)


@app.command()
def update(content: str, task_id: uuid.UUID, shorthand_title: str = None) -> None:
    """
    Update a task using its ID

    if :param shorthand_title: is passed, task lookup priority will be based on shorthand title,
    lookup will be done using task_id otherwise


    :param content: task content
    :param task_id: task ID
    :param shorthand_title: pass in shorthand title
    :return:
    """
    ...


@app.command()
def read(task_id: uuid.UUID, output: TaskReadType = TaskReadType.PLAIN) -> None:
    """
    Read a task, return its content and metadata

    :param task_id: The task ID

    :param output: PLAIN or JSON, defaults to PLAIN

    :return: the task's content
    """
    ...


@app.command()
def delete(task_id: uuid.UUID) -> None:
    """
    Delete a task using its ID
    """
    ...

@app.command()
def search(query: str) -> None:
    """
    Your query can be on of these arguments: content, title

    :param query: Search query

    :return: the best first match based on query, including metadata of the task
    """
    ...


if __name__ == '__main__':
    app()
