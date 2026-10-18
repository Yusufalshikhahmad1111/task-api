# Task API

A simple CRUD API for managing a to-do list, built with **FastAPI** as part of the FlyRank Backend AI Engineering program (Week 3).

## Features

- Full CRUD operations on tasks (Create, Read, Update, Delete)
- **Persistent storage using SQLite** (data survives server restarts)
- Input validation with proper HTTP status codes
- Interactive API docs via Swagger UI

## Requirements

- Python 3.10+

## How to run

```bash
# 1. Clone the repo
git clone https://github.com/Yusufalshikhahmad1111/task-api.git
cd task-api

# 2. Create and activate a virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install fastapi uvicorn

# 4. Start the server
uvicorn main:app --reload
```

Then open:
- API root: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

## Database (SQLite)

This API stores tasks in a **SQLite** database (`tasks.db`).

- **Why SQLite?** It requires no separate server, stores data in a single file, and is ideal for learning persistence.
- **Where is the file?** `tasks.db` in the project root. It is created automatically on first run.
- **Persistence:** Data survives server restarts.

### Database Schema

| Column | Type    | Notes                         |
|--------|---------|-------------------------------|
| id     | INTEGER | Primary key, auto-increment   |
| title  | TEXT    | Task title (required)         |
| done   | BOOLEAN | 0 = open, 1 = completed       |

### Example SQL query

```sql
SELECT * FROM tasks WHERE done = 1;
```

![Database screenshot](database.png)

## Endpoints

| Method | Path             | Description       | Status Codes     |
|--------|------------------|-------------------|------------------|
| GET    | `/`              | API information   | 200              |
| GET    | `/health`        | Health check      | 200              |
| GET    | `/tasks`         | List all tasks    | 200              |
| GET    | `/tasks/{id}`    | Get one task      | 200, 404         |
| POST   | `/tasks`         | Create a task     | 201, 400         |
| PUT    | `/tasks/{id}`    | Update a task     | 200, 400, 404    |
| DELETE | `/tasks/{id}`    | Delete a task     | 204, 404         |

## Example: creating a task

```bash
curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk"}'
```

Example response:

```
HTTP/1.1 201 Created
date: Sun, 13 Sep 2026 15:30:00 GMT
server: uvicorn
content-length: 47
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Example: 404 on unknown task

```bash
curl -i http://localhost:8000/tasks/99
```

```
HTTP/1.1 404 Not Found
content-type: application/json

{"detail":"Task 99 not found"}
```

## Swagger UI

![Swagger UI screenshot](swagger1.png)

## Project structure

```
task-api/
├── main.py          # FastAPI application
├── database.png     # SQLite database screenshot
├── swagger1.png     # Swagger UI screenshot
├── README.md        # This file
├── .gitignore       # Git ignore rules
└── tasks.db         # SQLite database (auto-generated, not tracked)
```

## Notes

- Data is stored in SQLite and persists across server restarts.
- This project was built stage by stage (Stages 0–5 of Week 3), with one commit per stage.
