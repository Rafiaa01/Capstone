import psycopg
from psycopg.rows import dict_row


class TaskRepository:
    def get_all(self) -> list[dict]:
        raise NotImplementedError

    def get_by_id(self, task_id: int) -> dict | None:
        raise NotImplementedError

    def create(self, title: str) -> dict:
        raise NotImplementedError

    def update(
        self,
        task_id: int,
        title: str | None = None,
        done: bool | None = None,
    ) -> dict | None:
        raise NotImplementedError

    def delete(self, task_id: int) -> bool:
        raise NotImplementedError


class InMemoryTaskRepository(TaskRepository):
    def __init__(self) -> None:
        self.tasks = [
            {"id": 1, "title": "Learn FastAPI", "done": False},
            {"id": 2, "title": "Build a Task API", "done": False},
            {
                "id": 3,
                "title": "Push the project to GitHub",
                "done": True,
            },
        ]

    def get_all(self) -> list[dict]:
        return self.tasks

    def get_by_id(self, task_id: int) -> dict | None:
        return next(
            (task for task in self.tasks if task["id"] == task_id),
            None,
        )

    def create(self, title: str) -> dict:
        next_id = max(
            (task["id"] for task in self.tasks),
            default=0,
        ) + 1

        new_task = {
            "id": next_id,
            "title": title,
            "done": False,
        }

        self.tasks.append(new_task)
        return new_task

    def update(
        self,
        task_id: int,
        title: str | None = None,
        done: bool | None = None,
    ) -> dict | None:
        task = self.get_by_id(task_id)

        if task is None:
            return None

        if title is not None:
            task["title"] = title

        if done is not None:
            task["done"] = done

        return task

    def delete(self, task_id: int) -> bool:
        for index, task in enumerate(self.tasks):
            if task["id"] == task_id:
                self.tasks.pop(index)
                return True

        return False


class PostgresTaskRepository(TaskRepository):
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url

    def get_all(self) -> list[dict]:
        query = """
            SELECT id, title, done
            FROM tasks
            ORDER BY id;
        """

        with psycopg.connect(
            self.database_url,
            row_factory=dict_row,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()

    def get_by_id(self, task_id: int) -> dict | None:
        query = """
            SELECT id, title, done
            FROM tasks
            WHERE id = %s;
        """

        with psycopg.connect(
            self.database_url,
            row_factory=dict_row,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (task_id,))
                return cursor.fetchone()

    def create(self, title: str) -> dict:
        query = """
            INSERT INTO tasks (title, done)
            VALUES (%s, FALSE)
            RETURNING id, title, done;
        """

        with psycopg.connect(
            self.database_url,
            row_factory=dict_row,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (title,))
                task = cursor.fetchone()

        if task is None:
            raise RuntimeError("Task could not be created.")

        return task

    def update(
        self,
        task_id: int,
        title: str | None = None,
        done: bool | None = None,
    ) -> dict | None:
        existing_task = self.get_by_id(task_id)

        if existing_task is None:
            return None

        new_title = (
            title
            if title is not None
            else existing_task["title"]
        )

        new_done = (
            done
            if done is not None
            else existing_task["done"]
        )

        query = """
            UPDATE tasks
            SET title = %s,
                done = %s
            WHERE id = %s
            RETURNING id, title, done;
        """

        with psycopg.connect(
            self.database_url,
            row_factory=dict_row,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (new_title, new_done, task_id),
                )
                return cursor.fetchone()

    def delete(self, task_id: int) -> bool:
        query = """
            DELETE FROM tasks
            WHERE id = %s;
        """

        with psycopg.connect(self.database_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (task_id,))
                return cursor.rowcount > 0