import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from repository import PostgresTaskRepository
from service import TaskService

load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL is not configured.")

repository = PostgresTaskRepository(database_url)
service = TaskService(repository)

app = FastAPI(
    title="Task API",
    description="A PostgreSQL-backed CRUD API for managing tasks.",
    version="2.0",
)


@app.get(
    "/",
    summary="View API information",
    description="Returns the API name, version, and main endpoint.",
)
def root():
    return {
        "name": "Task API",
        "version": "2.0",
        "endpoints": ["/tasks"],
    }


@app.get(
    "/health",
    summary="Check API health",
    description="Checks whether the Task API server is running.",
)
def health():
    return {"status": "ok"}


@app.get(
    "/tasks",
    summary="List all tasks",
    description="Returns every task currently stored in PostgreSQL.",
)
def get_tasks():
    return service.get_all_tasks()


@app.get(
    "/tasks/{task_id}",
    summary="Get one task",
    description="Returns a single task using its numeric ID.",
)
def get_task(task_id: int):
    task = service.get_task(task_id)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"},
        )

    return task


@app.post(
    "/tasks",
    status_code=201,
    summary="Create a task",
    description="Creates a new task with the supplied title.",
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
        return JSONResponse(
            status_code=400,
            content={"error": "Request body must contain valid JSON"},
        )

    if not isinstance(body, dict):
        return JSONResponse(
            status_code=400,
            content={"error": "Request body must be a JSON object"},
        )

    title = body.get("title")

    if not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"},
        )

    return service.create_task(title.strip())


@app.put(
    "/tasks/{task_id}",
    summary="Update a task",
    description="Updates the title, completion status, or both.",
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
    existing_task = service.get_task(task_id)

    if existing_task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"},
        )

    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body must contain valid JSON"},
        )

    if not isinstance(body, dict) or not body:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Request body must contain a title or done value"
            },
        )

    if "title" not in body and "done" not in body:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Request body must contain a title or done value"
            },
        )

    title = None
    done = None

    if "title" in body:
        title = body["title"]

        if not isinstance(title, str) or not title.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"},
            )

        title = title.strip()

    if "done" in body:
        done = body["done"]

        if not isinstance(done, bool):
            return JSONResponse(
                status_code=400,
                content={"error": "Done must be true or false"},
            )

    updated_task = service.update_task(
        task_id=task_id,
        title=title,
        done=done,
    )

    if updated_task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"},
        )

    return updated_task


@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    summary="Delete a task",
    description="Permanently removes a task using its numeric ID.",
)
def delete_task(task_id: int):
    deleted = service.delete_task(task_id)

    if not deleted:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"},
        )

    return Response(status_code=204)