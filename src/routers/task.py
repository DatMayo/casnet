"""
API endpoints for task management.

This module contains routes for creating, reading, updating, and deleting tasks.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Task, User
from ..security import get_current_user
from ..schemas.pagination import PaginatedResponse
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()


@router.get("/task/{tenant_id}", response_model=PaginatedResponse[TaskResponse], tags=["tasks"])
async def get_tasks(
    tenant_id: str = Path(description="ID of the tenant to retrieve tasks from"),
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Number of tasks per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve a paginated list of tasks for a specific tenant."""
    from ..exceptions import TenantAccessError
    user_tenant_ids = {t.id for t in current_user.tenants}
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, list(user_tenant_ids))

    tasks_query = db.query(Task).filter(Task.tenant_id == tenant_id)
    
    total_count = tasks_query.count()
    
    offset = (page - 1) * page_size
    tasks = tasks_query.offset(offset).limit(page_size).all()
    
    total_pages = (total_count + page_size - 1) // page_size
    return PaginatedResponse(
        data=tasks,
        meta={
            "total_items": total_count,
            "total_pages": total_pages,
            "current_page": page,
            "page_size": page_size,
            "has_next": page < total_pages,
            "has_previous": page > 1,
            "next_page": page + 1 if page < total_pages else None,
            "previous_page": page - 1 if page > 1 else None
        }
    )


@router.post("/task/{tenant_id}", response_model=TaskResponse, tags=["tasks"], status_code=201)
async def create_task(
    task_data: TaskCreate,
    tenant_id: str = Path(description="ID of the tenant to create the task in"), 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new task within a specific tenant."""
    from ..exceptions import TenantAccessError
    user_tenant_ids = {t.id for t in current_user.tenants}
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, list(user_tenant_ids))

    new_task = Task(
        **task_data.model_dump(),
        tenant_id=tenant_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/task/{tenant_id}/{task_id}", response_model=TaskResponse, tags=["tasks"])
async def get_task(
    tenant_id: str = Path(description="ID of the tenant that owns the task"),
    task_id: str = Path(description="ID of the task to retrieve"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve a single task by its ID."""
    from ..exceptions import TenantAccessError
    user_tenant_ids = {t.id for t in current_user.tenants}
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, list(user_tenant_ids))

    task = db.query(Task).filter(Task.id == task_id, Task.tenant_id == tenant_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found in this tenant")
    return task


@router.put("/task/{tenant_id}/{task_id}", response_model=TaskResponse, tags=["tasks"])
async def update_task(
    task_data: TaskUpdate,
    tenant_id: str = Path(description="ID of the tenant that owns the task"),
    task_id: str = Path(description="ID of the task to update"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a task's details."""
    from ..exceptions import TenantAccessError
    user_tenant_ids = {t.id for t in current_user.tenants}
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, list(user_tenant_ids))

    task = db.query(Task).filter(Task.id == task_id, Task.tenant_id == tenant_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found in this tenant")

    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    
    db.commit()
    db.refresh(task)
    return task


@router.delete("/task/{tenant_id}/{task_id}", response_model=TaskResponse, tags=["tasks"])
async def delete_task(
    tenant_id: str = Path(description="ID of the tenant that owns the task"),
    task_id: str = Path(description="ID of the task to delete"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a task by its ID."""
    from ..exceptions import TenantAccessError
    user_tenant_ids = {t.id for t in current_user.tenants}
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, list(user_tenant_ids))

    task = db.query(Task).filter(Task.id == task_id, Task.tenant_id == tenant_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found in this tenant")

    db.delete(task)
    db.commit()
    return task
