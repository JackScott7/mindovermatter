import sqlite3
from lib.utils import ActionStatus, Task, TaskStatus, SearchResult, is_valid_uuid4


class Database:
    def __init__(self, db_url: str):
        """
            Initializes a SQlite3 database based on the given DB URL.

            Exposes the following methods:
            add, read, update, delete, search
            :param db_url: DATABASE_URL
        """
        if not db_url:
            raise ValueError("Database URL is required. ensure the MOM_DATABASE_URL environment variable is set")

        self.db_url = db_url
        self.__connection = sqlite3.connect(self.db_url)
        self.__connection.row_factory = sqlite3.Row
        self.__cursor = self.__connection.cursor()

        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks
            (
                task_id         TEXT PRIMARY KEY,
                title           TEXT NOT NULL,
                shorthand_title TEXT UNIQUE,
                content         TEXT NOT NULL,
                tags            TEXT,
                
                status          TEXT NOT NULL CHECK (status IN ('active', 'completed', 'pending')),
                created_at      TEXT NOT NULL DEFAULT (datetime('now')),
                updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)
        self.__connection.commit()

    def add_task(self, content, title, shorthand_title, task_id, tags) -> ActionStatus:
        """
        Adds a new task to the database.

        All the parameter checks (empty, incorrect, invalid) values should be checked before calling this method.
        :return: the task id
        """
        try:
            self.__cursor.execute(
                """INSERT INTO tasks (task_id, title, shorthand_title, content, tags, status) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                (task_id, title, shorthand_title, content, tags, TaskStatus.PENDING.value)
            )

            if self.__cursor.rowcount == 0:
                return ActionStatus.FAILURE

            self.__connection.commit()
            return ActionStatus.SUCCESS
        except sqlite3.IntegrityError:
            self.__connection.rollback()
            return ActionStatus.INTEGRITY_ERROR

    def read_task(self, task_id) -> tuple[Task | None, ActionStatus]:
        """
        Reads a task from the database.

        :param task_id: task id

        :return: (task, status)
        """
        try:
            self.__cursor.execute('SELECT task_id, title, shorthand_title, content, '
                                        'tags, status, created_at, updated_at FROM tasks WHERE task_id = ?',
                                (task_id,))

            row = self.__cursor.fetchone()

            if not row:
                return None, ActionStatus.FAILURE

            task = Task(
                task_id=row["task_id"],
                title=row["title"],
                shorthand_title=row["shorthand_title"],
                content=row["content"],
                tags=row["tags"],
                status=row["status"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )

            return task, ActionStatus.SUCCESS
        except sqlite3.Error:
            return None, ActionStatus.FAILURE

    def update_task(self, content, task_id, shorthand_title) -> None:
        ...

    def delete_task(self, task_id)  -> ActionStatus:
        """
        Deletes a task from the database.

        :param task_id: task id

        :return: (task, status)
        """
        try:
            self.__cursor.execute('DELETE FROM tasks WHERE task_id = ?', (task_id,))
            if self.__cursor.rowcount == 0:
                return ActionStatus.NOT_FOUND

            self.__connection.commit()
            return ActionStatus.SUCCESS
        except sqlite3.Error:
            self.__connection.rollback()
            return ActionStatus.FAILURE

    def search_task(self, query: str) -> tuple[list[SearchResult], ActionStatus]:
        self.__cursor.execute(
            "SELECT task_id, title, tags, updated_at FROM tasks "
            f"WHERE content like '%{query}%' "
            f"OR shorthand_title like '%{query}%' "
            f"OR title like '{query}'"
        )
        rows = self.__cursor.fetchall()
        if not rows:
            return [], ActionStatus.NOT_FOUND
        return [SearchResult(**x) for x in rows], ActionStatus.SUCCESS

    def list_tasks(self, status, limit) -> tuple[list[Task], ActionStatus]:
        """
        Lists all tasks from the database.

        :param status: task status

        :param limit: number of tasks to list

        :return: (tasks, status)
        """
        try:
            self.__cursor.execute(
                'SELECT * FROM tasks WHERE status = ? ORDER BY updated_at DESC limit ?',
                (status,limit)
            )
            tasks = self.__cursor.fetchall()
            if not tasks:
                return [], ActionStatus.NOT_FOUND

            return [Task(**x) for x in tasks], ActionStatus.SUCCESS
        except sqlite3.Error:
            return [], ActionStatus.FAILURE

    def mark_task(self, task: Task, status: TaskStatus) -> ActionStatus:
        self.__cursor.execute(
            """UPDATE tasks 
            SET status = ?,
            updated_at = CURRENT_TIMESTAMP
            WHERE task_id = ?""",
            (status.value, task.task_id)
        )
        updated = self.__cursor.rowcount
        if updated == 0:
            print(updated)
            return ActionStatus.NOT_FOUND
        if updated == 1:
            self.__connection.commit()
            return ActionStatus.SUCCESS
        return ActionStatus.FAILURE

    def get_task(self, query: str) -> tuple[Task | None, ActionStatus]:
        self.__cursor.execute(
            "SELECT * FROM tasks WHERE shorthand_title = ? OR task_id = ?",
            (query, query)
        )
        row = self.__cursor.fetchone()
        if not row:
            return None, ActionStatus.NOT_FOUND
        return Task(**row), ActionStatus.SUCCESS
