"""
API endpoints for task management.

This module contains routes for creating, reading, updating, and deleting tasks.
"""
import uuid
from typing import List
from fastapi import APIRouter, HTTPException
from ..database import task_list, Task, Person
from ..util import get_timestamp, find_item_by_id

router = APIRouter()


@router.get("/task", response_model=List[Task], tags=["tasks"])
async def get_tasks(limit: int = 100, offset: int = 0):
    """Retrieve a list of tasks with optional pagination."""
    return task_list[offset:offset + limit]


@router.post("/task", response_model=Task, tags=["tasks"], status_code=201)
async def create_task(task: Task):
    """Create a new task."""
    if any(t.id == task.id for t in task_list):
        raise HTTPException(status_code=400, detail="A task with that ID already exists")

    task_list.append(task)
    return task


@router.get("/task/{task_id}", response_model=Task, tags=["tasks"])
async def get_task(task_id: str):
    """Retrieve a single task by its ID."""
    return find_item_by_id(task_id, task_list, "Task")


@router.put("/task/{task_id}", response_model=Task, tags=["tasks"])
async def update_task(task_id: str, title: str, created_for: Person):
    """Update a task's details."""
    task = find_item_by_id(task_id, task_list, "Task")
    task.title = title
    task.created_for = created_for
    task.updatedAt = get_timestamp()
    return task


@router.delete("/task/{task_id}", response_model=Task, tags=["tasks"])
async def delete_task(task_id: str):
    """Delete a task by its ID and return the deleted object."""
    task = find_item_by_id(task_id, task_list, "Task")
    task_list.remove(task)
    return task
