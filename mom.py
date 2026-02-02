import os
import string
import sys
import uuid
from time import sleep

import typer
from db import Database
from utils import TaskStatus, TaskReadType, ActionStatus
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print, json


app = typer.Typer(name="MindOverMatter", add_completion=True, pretty_exceptions_enable=True)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = os.getenv("MOM_DATABASE_URL", os.path.join(BASE_DIR, "mom.db"))
db = Database(DATABASE_URL)


@app.command()
def add(content: str,
        title: str,
        shorthand_title: str = None,
        task_id: uuid.UUID = uuid.uuid4(),
        tags: str = None) -> None:
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
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        pid = progress.add_task(f"Creating {shorthand_title or title}", total=None)
        task = db.add_task(content, title, shorthand_title, str(task_id), ",".join(tags.split(',')))
        sleep(0.4)

        if task != ActionStatus.SUCCESS:
            print(f"Your submitted task:\n"
                    f"\tContent: <{content[:10].strip(string.whitespace)}>\n"
                    f"\tTitle: <{title}>\n"
                    f"\tID: <{task_id}>\n"
                    "Is a duplicate, if you want the duplicate content, you should set new shorthand title")
            raise typer.Exit(1)

        progress.update(pid, description="Finished")

    print(f"You task has been created ✨\nID: <{task_id}>")
    print(f"\nOpen your task by running:\n./mom.py read {task_id}")


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
    task, status = db.read_task(str(task_id))
    if status != ActionStatus.SUCCESS:
        print("There was an error reading the task, check your input and try again")
        typer.Exit(1)

    if output == TaskReadType.PLAIN:
        print(f"ID: {task.task_id}\nTitle: {task.title}\nTags: {task.tags}\nContent: \n{task.content}")
        return

    print(json.dumps(task.__dict__, indent=4))


@app.command()
def delete(task_id: uuid.UUID) -> None:
    """
    Delete a task using its ID
    """
    typer.confirm("Are you sure you want to delete this task?", abort=True)
    status = db.delete_task(str(task_id))
    if status == ActionStatus.SUCCESS:
        print(f"✨ Task <{task_id}> deleted successfully")
        return

    if status == ActionStatus.NOT_FOUND:
        print("[red]Task not found, please check your input and try again[/red]")
        raise typer.Exit(1)


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
