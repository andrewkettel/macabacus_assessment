from uuid import UUID

from fastapi import APIRouter, HTTPException
from typing import List

from ..models.task import Task

router = APIRouter()

# In-memory list to store tasks
tasks: List[Task] = []


# List all tasks
@router.get("/tasks")
async def list_tasks():
    return [task for task in tasks]


# Create a task
@router.post("/tasks", response_model=Task)
async def create_task(task: Task):
    tasks.append(task)
    return task


# Update a task
@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task: Task):
    t = next((task for task in tasks if task.id == UUID(task_id)), None)
    if not t:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

    t.title = task.title
    t.status = task.status
    return t
