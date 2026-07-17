from repository import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def get_all_tasks(self) -> list[dict]:
        return self.repository.get_all()

    def get_task(self, task_id: int) -> dict | None:
        return self.repository.get_by_id(task_id)

    def create_task(self, title: str) -> dict:
        return self.repository.create(title)

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        done: bool | None = None,
    ) -> dict | None:
        return self.repository.update(
            task_id=task_id,
            title=title,
            done=done,
        )

    def delete_task(self, task_id: int) -> bool:
        return self.repository.delete(task_id)