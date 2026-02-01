"""
a simple CLI todo app
- add
    positional required content: ""
    -t --title
    --id
    -t --tags
"""
import uuid
import typer
import sqlite3
from typing import Optional

app = typer.Typer(name="MindOverMatter", add_completion=True, pretty_exceptions_enable=True)


@app.command()
def add(content: str,
        title: str,
        shorthand_title: str = None,
        task_id: Optional[uuid.UUID] = uuid.uuid4(),
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
    ...


@app.command()
def update(content: str, task_id: uuid.UUID) -> None:
    ...


@app.command()
def read(task_id: uuid.UUID) -> None:
    ...


@app.command()
def delete(task_id: uuid.UUID) -> None:
    ...


def __setup_requirements():
    pass


if __name__ == '__main__':
    __setup_requirements()
    app()
