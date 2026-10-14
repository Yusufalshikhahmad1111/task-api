from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple CRUD API for managing a to-do list, backed by SQLite.",
)

DB_PATH = "tasks.db"


# ---------- Database setup ----------
def init_db():
    """Create the tasks table (if missing) and seed it once."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Learn FastAPI", 0),
                ("Build CRUD API", 0),
                ("Push to GitHub", 0),
            ],
        )

    conn.commit()
    conn.close()


init_db()


# ---------- Pydantic models ----------
class Task(BaseModel):
    id: int
    title: str
    done: bool = False



@app.get("/", tags=["Info"], summary="API information")
def read_root():
    """Returns basic information about this API."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }



@app.get("/health", tags=["Info"], summary="Health check")
def health_check():
    """Returns `ok` if the server is alive."""
    return {"status": "ok"}



@app.get("/tasks", response_model=List[Task], tags=["Tasks"], summary="List all tasks")
def list_tasks():
    """Returns the full list of tasks from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    return [Task(id=r[0], title=r[1], done=bool(r[2])) for r in rows]





@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"], summary="Get one task")
def get_task(task_id: int):
    """Returns a single task by its ID. Returns 404 if not found."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    return Task(id=row[0], title=row[1], done=bool(row[2]))


    


class TaskCreate(BaseModel):
    title: Optional[str] = None


@app.post("/tasks", response_model=Task, status_code=201, tags=["Tasks"], summary="Create a task")
def create_task(payload: TaskCreate):
    """Creates a new task. Returns 400 if title is missing or empty."""
    if not payload.title or not payload.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title is required and cannot be empty"
        )
    new_id = max([t.id for t in tasks_db], default=0) + 1
    new_task = Task(id=new_id, title=payload.title, done=False)
    tasks_db.append(new_task)
    return new_task



class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


@app.put("/tasks/{task_id}", response_model=Task, tags=["Tasks"], summary="Update a task")
def update_task(task_id: int, payload: TaskUpdate):
    """Updates a task's title and/or done. Returns 404 if not found, 400 if title is empty."""
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            if payload.title is not None:
                if not payload.title.strip():
                    raise HTTPException(status_code=400, detail="Title cannot be empty")
                task.title = payload.title
            if payload.done is not None:
                task.done = payload.done
            tasks_db[i] = task
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")



@app.delete("/tasks/{task_id}", status_code=204, tags=["Tasks"], summary="Delete a task")
def delete_task(task_id: int):
    """Deletes a task by ID. Returns 404 if not found."""
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            del tasks_db[i]
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")