import sqlite3


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
        self.__cursor = self.__connection.cursor()

        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks
                (
                    task_id         TEXT PRIMARY KEY,
                    title           TEXT NOT NULL,
                    shorthand_title TEXT UNIQUE,
                    content         TEXT NOT NULL,
                    tags            TEXT
                )
            """)

    def add_task(self, content, title, shorthand_title, task_id, tags) -> None:
        """
        Adds a new task to the database.

        All the parameter checks (empty, incorrect, invalid) values should be checked before calling this method.
        :return: the task id
        """
        task = self.__cursor.execute(
            "INSERT INTO tasks VALUES (?, ?, ?, ?, ?)",
            (content, title, shorthand_title, task_id, tags)
        )
        self.__connection.commit()

    def read_task(self, task_id) -> None:
        ...

    def update_task(self, content, task_id, shorthand_title) -> None:
        ...

    def delete_task(self, task_id) -> None:
        ...

    def search_task(self, content, title, shorthand_title, task_id, tags) -> None:
        ...
