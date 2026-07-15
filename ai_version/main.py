from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

app = FastAPI(
    title="AI Task API",
    description="An AI-generated in-memory CRUD API for managing tasks.",
    version="1.0",
)


INITIAL_TASKS = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False,
    },
    {
        "id": 2,
        "title": "Build a Task API",
        "done": False,
    },
    {
        "id": 3,
        "title": "Push the project to GitHub",
        "done": True,
    },
]

tasks = [task.copy() for task in INITIAL_TASKS]


def find_task(task_id: int) -> dict[str, Any] | None:
    """Find and return a task by ID."""
    return next(
        (task for task in tasks if task["id"] == task_id),
        None,
    )


def error_response(message: str, status_code: int) -> JSONResponse:
    """Return a consistent JSON error response."""
    return JSONResponse(
        status_code=status_code,
        content={"error": message},
    )


@app.get(
    "/",
    summary="View API information",
    description="Returns the API name, version, and available task endpoint.",
)
def root():
    return {
        "name": "AI Task API",
        "version": "1.0",
        "endpoints": ["/tasks"],
    }


@app.get(
    "/health",
    summary="Check API health",
    description="Confirms that the API server is running.",
)
def health():
    return {"status": "ok"}


@app.get(
    "/tasks",
    summary="List all tasks",
    description="Returns every task currently stored in memory.",
)
def get_tasks():
    return tasks


@app.get(
    "/tasks/{task_id}",
    summary="Get one task",
    description="Returns a single task using its numeric ID.",
)
def get_task(task_id: int):
    task = find_task(task_id)

    if task is None:
        return error_response(
            f"Task {task_id} not found",
            404,
        )

    return task


@app.post(
    "/tasks",
    status_code=201,
    summary="Create a task",
    description="Creates a task using a required title.",
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "required": ["title"],
                        "properties": {
                            "title": {
                                "type": "string",
                                "example": "Buy milk",
                            }
                        },
                    }
                }
            },
        }
    },
)
async def create_task(request: Request):
    try:
        body = await request.json()
    except Exception:
        return error_response(
            "Request body must contain valid JSON",
            400,
        )

    if not isinstance(body, dict):
        return error_response(
            "Request body must be a JSON object",
            400,
        )

    title = body.get("title")

    if not isinstance(title, str):
        return error_response(
            "Title is required and must be text",
            400,
        )

    title = title.strip()

    if not title:
        return error_response(
            "Title is required and cannot be empty",
            400,
        )

    next_id = max(
        (task["id"] for task in tasks),
        default=0,
    ) + 1

    new_task = {
        "id": next_id,
        "title": title,
        "done": False,
    }

    tasks.append(new_task)

    return new_task


@app.put(
    "/tasks/{task_id}",
    summary="Update a task",
    description="Updates a task's title, completion status, or both.",
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "example": "Buy milk and bread",
                            },
                            "done": {
                                "type": "boolean",
                                "example": True,
                            },
                        },
                    }
                }
            },
        }
    },
)
async def update_task(task_id: int, request: Request):
    task = find_task(task_id)

    if task is None:
        return error_response(
            f"Task {task_id} not found",
            404,
        )

    try:
        body = await request.json()
    except Exception:
        return error_response(
            "Request body must contain valid JSON",
            400,
        )

    if not isinstance(body, dict):
        return error_response(
            "Request body must be a JSON object",
            400,
        )

    if not body:
        return error_response(
            "Request body must contain a title or done value",
            400,
        )

    if "title" not in body and "done" not in body:
        return error_response(
            "Request body must contain a title or done value",
            400,
        )

    updated_title = task["title"]
    updated_done = task["done"]

    if "title" in body:
        title = body["title"]

        if not isinstance(title, str):
            return error_response(
                "Title must be text",
                400,
            )

        title = title.strip()

        if not title:
            return error_response(
                "Title cannot be empty",
                400,
            )

        updated_title = title

    if "done" in body:
        done = body["done"]

        if not isinstance(done, bool):
            return error_response(
                "Done must be true or false",
                400,
            )

        updated_done = done

    task["title"] = updated_title
    task["done"] = updated_done

    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    summary="Delete a task",
    description="Deletes a task using its numeric ID.",
)
def delete_task(task_id: int):
    task = find_task(task_id)

    if task is None:
        return error_response(
            f"Task {task_id} not found",
            404,
        )

    tasks.remove(task)

    return Response(status_code=204)