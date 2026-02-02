import typer
import os
import string
import uuid
from time import sleep
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print, json
from lib.db import Database
from lib.utils import OutputType, ActionStatus, TaskStatus

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
            TextColumn("[progress.description]{task.description}"), transient=True
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
def read(task_id: uuid.UUID, output: OutputType = OutputType.PLAIN) -> None:
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

    if output == OutputType.PLAIN:
        print(task.plain)
        return

    print(json.dumps(task.json, indent=4))


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

@app.command()
def mark(status: TaskStatus, query: str) -> None:
    """
    Mark a task using its ID or Shorthand Title

    :param status: Task status

    :param query: can be either TaskID or Shorthand Title if set
    """
    ...


@app.command(name='list')
def list_tasks(status: TaskStatus = TaskStatus.ACTIVE, limit: int = 5, output: OutputType = OutputType.PLAIN) -> None:
    """
    List all tasks, filtered by status and limit

    :param status: Task status

    :param output: output format

    :param limit: number of tasks to list
    """
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"), transient=True
    ) as progress:
        pid = progress.add_task(f"Fetching ...", total=None)
        sleep(0.4)
        tasks, _ = db.list_tasks(status.value, limit)
        if not tasks:
            progress.update(pid, description="No results")
            print(f"[yellow]There are no tasks with status[/yellow]: [red]{status.value}[/red]")
            raise typer.Exit(1)

        progress.update(pid, description="Found results")

    if output == OutputType.PLAIN:
        _ = [print(x.plain, "\n") for x in tasks]
        return

    print(json.dumps([x.json for x in tasks], indent=4))


if __name__ == '__main__':
    app()
