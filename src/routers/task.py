"""
API endpoints for task management.

This module contains routes for creating, reading, updating, and deleting tasks.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from ..database import task_list, Task, Person
from ..util import get_timestamp, find_item_by_id, validate_user_tenant_access
from ..security import get_current_user
from ..model.user import UserAccount

router = APIRouter()


@router.get("/task/{tenant_id}", response_model=List[Task], tags=["tasks"])
async def get_tasks(tenant_id: str, limit: int = 100, offset: int = 0, current_user: UserAccount = Depends(get_current_user)):
    """Retrieve a list of tasks with optional pagination."""
    validate_user_tenant_access(tenant_id, current_user)
    return [t for t in task_list if t.tenant and t.tenant.id == tenant_id][offset:offset + limit]


@router.post("/task/{tenant_id}", response_model=Task, tags=["tasks"], status_code=201)
async def create_task(tenant_id: str, task: Task, current_user: UserAccount = Depends(get_current_user)):
    """Create a new task."""
    tenant = validate_user_tenant_access(tenant_id, current_user)
    if any(t.id == task.id for t in task_list):
        raise HTTPException(status_code=400, detail="A task with that ID already exists")

    task.tenant = tenant
    task_list.append(task)
    return task


@router.get("/task/{tenant_id}/{task_id}", response_model=Task, tags=["tasks"])
async def get_task(tenant_id: str, task_id: str, current_user: UserAccount = Depends(get_current_user)):
    """Retrieve a single task by its ID."""
    validate_user_tenant_access(tenant_id, current_user)
    return find_item_by_id(task_id, task_list, "Task", tenant_id)


@router.put("/task/{tenant_id}/{task_id}", response_model=Task, tags=["tasks"])
async def update_task(tenant_id: str, task_id: str, title: str, created_for: Person, current_user: UserAccount = Depends(get_current_user)):
    """Update a task's details."""
    validate_user_tenant_access(tenant_id, current_user)
    task = find_item_by_id(task_id, task_list, "Task", tenant_id)
    task.title = title
    task.created_for = created_for
    task.updatedAt = get_timestamp()
    return task


@router.delete("/task/{tenant_id}/{task_id}", response_model=Task, tags=["tasks"])
async def delete_task(tenant_id: str, task_id: str, current_user: UserAccount = Depends(get_current_user)):
    """Delete a task by its ID and return the deleted object."""
    validate_user_tenant_access(tenant_id, current_user)
    task = find_item_by_id(task_id, task_list, "Task", tenant_id)
    task_list.remove(task)
    return task
