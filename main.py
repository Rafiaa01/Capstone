from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

app = FastAPI()


tasks = [
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


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"],
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"},
    )


@app.post("/tasks", status_code=201)
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

    next_id = max((task["id"] for task in tasks), default=0) + 1

    new_task = {
        "id": next_id,
        "title": title.strip(),
        "done": False,
    }

    tasks.append(new_task)

    return new_task


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, request: Request):
    task = next(
        (task for task in tasks if task["id"] == task_id),
        None,
    )

    if task is None:
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

    allowed_fields = {"title", "done"}

    if not any(field in body for field in allowed_fields):
        return JSONResponse(
            status_code=400,
            content={
                "error": "Request body must contain a title or done value"
            },
        )

    if "title" in body:
        title = body["title"]

        if not isinstance(title, str) or not title.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"},
            )

        task["title"] = title.strip()

    if "done" in body:
        done = body["done"]

        if not isinstance(done, bool):
            return JSONResponse(
                status_code=400,
                content={"error": "Done must be true or false"},
            )

        task["done"] = done

    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return Response(status_code=204)

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"},
    )