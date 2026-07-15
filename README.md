# Capstone — Backend AI Engineering

Capstone project for the FlyRank AI Internship, Backend AI Engineering track.

## About
This repository documents my work building AI-assisted frontend applications, combining modern frontend engineering practices with AI tooling (Claude Code / Cursor) for faster, higher-quality development.

## Tech Stack
TypeScript, React (Vite or Next.js), Tailwind CSS, and ESLint with Prettier for linting and formatting. See CLAUDE.md for full conventions.

## Status
Project setup in progress.

## Getting Started
Instructions for installing dependencies and running the project locally will be added as the project develops.

## Conventions
See CLAUDE.md for the stack and contribution conventions used in this repo.

## License
This project is licensed under the MIT License — see the LICENSE file for details.
# Task API

A simple CRUD REST API built with Python and FastAPI.

The API stores tasks in an in-memory Python list and supports creating, reading, updating, and deleting tasks. FastAPI also provides automatically generated interactive API documentation through Swagger UI.

## Features

* View API information
* Check server health
* List all tasks
* Retrieve one task by ID
* Create a new task
* Update a task
* Delete a task
* Input validation with JSON error responses
* Correct HTTP status codes
* Interactive Swagger UI documentation

## Technologies

* Python
* FastAPI
* Uvicorn
* Git and GitHub

## Project Structure

```text
Capstone/
├── main.py
├── requirements.txt
├── README.md
└── screenshots/
    └── swagger-ui.png
```

## Installation and Setup

Clone the repository:

```bash
git clone https://github.com/Rafiaa01/Capstone.git
cd Capstone
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the API

Use this command from the project folder:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger UI will be available at:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint           | Description                                        | Success status   |
| ------ | ------------------ | -------------------------------------------------- | ---------------- |
| GET    | `/`                | Returns API information                            | `200 OK`         |
| GET    | `/health`          | Checks whether the server is running               | `200 OK`         |
| GET    | `/tasks`           | Returns all tasks                                  | `200 OK`         |
| GET    | `/tasks/{task_id}` | Returns one task by ID                             | `200 OK`         |
| POST   | `/tasks`           | Creates a new task                                 | `201 Created`    |
| PUT    | `/tasks/{task_id}` | Updates a task's title, completion status, or both | `200 OK`         |
| DELETE | `/tasks/{task_id}` | Deletes a task                                     | `204 No Content` |

Unknown task IDs return:

```text
404 Not Found
```

Invalid request bodies return:

```text
400 Bad Request
```

## Task Format

Each task contains:

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "done": false
}
```

## Create a Task

Example request:

```bash
curl -i -X POST http://127.0.0.1:8000/tasks \
-H "Content-Type: application/json" \
-d "{\"title\":\"Buy milk\"}"
```

Example response:

```text
HTTP/1.1 201 Created
date: Wed, 15 Jul 2026 00:00:00 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

The exact `date` and `content-length` headers may differ depending on when the command is run and the returned data.

## Validation Example

Sending an empty object:

```bash
curl -i -X POST http://127.0.0.1:8000/tasks \
-H "Content-Type: application/json" \
-d "{}"
```

Returns:

```json
{
  "error": "Title is required and cannot be empty"
}
```

with the status:

```text
400 Bad Request
```

## Swagger UI

The full API can be tested without using curl at:

```text
http://127.0.0.1:8000/docs
```

![Task API Swagger UI](screenshots/swagger-ui.png)

Swagger UI supports the complete CRUD workflow:

1. Create a task using `POST /tasks`
2. View it using `GET /tasks`
3. Update it using `PUT /tasks/{task_id}`
4. Delete it using `DELETE /tasks/{task_id}`
5. Confirm deletion using `GET /tasks/{task_id}`

## Important Note

The tasks are stored in memory. Any tasks created or updated while the API is running will be lost when the server restarts.

## Development Stages

The project was developed through the following stages:

1. Hello server
2. Root and health endpoints
3. Read endpoints with 404 handling
4. Create endpoint with validation
5. Full CRUD functionality
6. Swagger UI documentation
7. GitHub publication and project documentation

