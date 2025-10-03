"""
API endpoints for task management.

This module contains routes for creating, reading, updating, and deleting tasks.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from ..database import task_list, Task, Person
from ..util import get_timestamp, find_item_by_id, validate_user_tenant_access
from ..security import get_current_user
from ..model.user import UserAccount
from ..model.pagination import PaginatedResponse, paginate_data

router = APIRouter()


@router.get("/task/{tenant_id}", response_model=PaginatedResponse[Task], tags=["tasks"])
async def get_tasks(
    tenant_id: str = Path(description="ID of the tenant to retrieve tasks from"),
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Number of tasks per page"),
    current_user: UserAccount = Depends(get_current_user)
):
    """Retrieve a paginated list of tasks for a specific tenant."""
    validate_user_tenant_access(tenant_id, current_user)
    
    # Filter tasks by tenant
    tenant_tasks = [t for t in task_list if t.tenant and t.tenant.id == tenant_id]
    
    # Paginate the data
    paginated_tasks, pagination_meta = paginate_data(tenant_tasks, page, page_size)
    
    return PaginatedResponse(
        data=paginated_tasks,
        meta=pagination_meta
    )


@router.post("/task/{tenant_id}", response_model=Task, tags=["tasks"], status_code=201)
async def create_task(
    task: Task,
    tenant_id: str = Path(description="ID of the tenant to create the task in"), 
    current_user: UserAccount = Depends(get_current_user)
):
    """Create a new task."""
    tenant = validate_user_tenant_access(tenant_id, current_user)
    if any(t.id == task.id for t in task_list):
        raise HTTPException(status_code=400, detail="A task with that ID already exists")

    task.tenant = tenant
    task_list.append(task)
    return task


@router.get("/task/{tenant_id}/{task_id}", response_model=Task, tags=["tasks"])
async def get_task(
    tenant_id: str = Path(description="ID of the tenant that owns the task"),
    task_id: str = Path(description="ID of the task to retrieve"),
    current_user: UserAccount = Depends(get_current_user)
):
    """Retrieve a single task by its ID."""
    validate_user_tenant_access(tenant_id, current_user)
    return find_item_by_id(task_id, task_list, "Task", tenant_id)


@router.put("/task/{tenant_id}/{task_id}", response_model=Task, tags=["tasks"])
async def update_task(
    created_for: Person,  # Complex types can't use Query()
    tenant_id: str = Path(description="ID of the tenant that owns the task"),
    task_id: str = Path(description="ID of the task to update"),
    title: str = Query(description="Updated title for the task"),
    current_user: UserAccount = Depends(get_current_user)
):
    """Update a task's details."""
    validate_user_tenant_access(tenant_id, current_user)
    task = find_item_by_id(task_id, task_list, "Task", tenant_id)
    task.title = title
    task.created_for = created_for
    task.updatedAt = get_timestamp()
    return task


@router.delete("/task/{tenant_id}/{task_id}", response_model=Task, tags=["tasks"])
async def delete_task(
    tenant_id: str = Path(description="ID of the tenant that owns the task"),
    task_id: str = Path(description="ID of the task to delete"),
    current_user: UserAccount = Depends(get_current_user)
):
    """Delete a task by its ID and return the deleted object."""
    validate_user_tenant_access(tenant_id, current_user)
    task = find_item_by_id(task_id, task_list, "Task", tenant_id)
    task_list.remove(task)
    return task
