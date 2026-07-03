from uuid import UUID

from fastapi import APIRouter, HTTPException
from typing import List

from ..models.task import Task, StatusEnum

router = APIRouter()

# In-memory list to store tasks
tasks: List[Task] = []


def check_uniqueness(data: List[Task]):
    ids = [task.id for task in data]
    if len(ids) != len(set(ids)):
        return False
    return True


# List all tasks
@router.get("/tasks", response_model=List[Task])
async def list_tasks(status: StatusEnum | None = None):
    if status:
        filtered_tasks_db = [task for task in tasks if task.status == status]
        return filtered_tasks_db
    else:
        return tasks


# Create a task
@router.post("/tasks", response_model=Task)
async def create_task(task: Task):
    if not check_uniqueness(tasks + [task]):
        raise HTTPException(status_code=400, detail="Task id is not unique")
    tasks.append(task)
    return task


# Update a task
@router.patch("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task: Task):
    t = next((task for task in tasks if task.id == UUID(task_id)), None)
    if not t:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

    t.title = task.title
    t.status = task.status
    return t
