"""
API endpoints for task management.

This module contains routes for creating and reading tasks.
"""
from typing import List
from fastapi import APIRouter, HTTPException
from ..database import task_list, Task, Person
from ..util import get_timestamp

router = APIRouter()


@router.get("/task", response_model=List[Task], tags=["tasks"])
async def get_tasks(limit: int = 100, offset: int = 0):
    """Retrieve a list of tasks with optional pagination."""
    return task_list[offset:offset + limit]


@router.post("/task", response_model=Task, tags=["tasks"])
async def create_task(task: Task):
    """Create a new task."""
    if any(t.id == task.id for t in task_list):
        raise HTTPException(status_code=400, detail="A task with that ID already exists")

    task_list.append(task)
    return task


@router.get("/task/{task_id}", response_model=Task, tags=["tasks"])
async def get_task(task_id: str):
    """Retrieve a single task by its ID."""
    for task in task_list:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@router.put("/task/{task_id}", response_model=Task, tags=["tasks"])
async def update_task(task_id: str, title: str, created_for: Person):
    """Update a task's details."""
    for index, task in enumerate(task_list):
        if task.id == task_id:
            task.title = title
            task.created_for = created_for
            task.updatedAt = get_timestamp()
            task_list[index] = task
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/task/{task_id}", status_code=204, tags=["tasks"])
async def delete_task(task_id: str):
    """Delete a task by its ID."""
    for index, task in enumerate(task_list):
        if task.id == task_id:
            task_list.pop(index)
            return task
    raise HTTPException(status_code=404, detail="Task not found")
