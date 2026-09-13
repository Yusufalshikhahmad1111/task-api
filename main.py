from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional 



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



class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskUpdate):
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            if payload.title is not None:
                if not payload.title.strip():
                    raise HTTPException(
                        status_code=400,
                        detail="Title cannot be empty"
                    )
                task.title = payload.title
            if payload.done is not None:
                task.done = payload.done
            tasks_db[i] = task
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


# ---- Delete: حذف مهمة ----
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            del tasks_db[i]
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")