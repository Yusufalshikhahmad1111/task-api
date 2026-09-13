from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from typing import Optional 

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    done: bool = False


tasks_db: List[Task] = [
    Task(id=1, title="Learn FastAPI", done=False),
    Task(id=2, title="Build CRUD API", done=False),
    Task(id=3, title="Push to GitHub", done=False),
]


@app.get("/")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}



@app.get("/tasks", response_model=List[Task])
def list_tasks():
    return tasks_db



@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

#هذه فكرة احترافية: افصل بين ما يستقبله السيرفر وما يرجّعه.


class TaskCreate(BaseModel):
    title: Optional[str] = None


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate):
    if not payload.title or not payload.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title is required and cannot be empty"
        )
    
    new_id = max([t.id for t in tasks_db], default=0) + 1
    new_task = Task(id=new_id, title=payload.title, done=False)
    tasks_db.append(new_task)
    return new_task