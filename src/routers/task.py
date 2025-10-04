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
from ..dependencies import get_permission_checker, requires_permission_for_resource
from ..enum.epermission import EPermission
from ..schemas.pagination import PaginatedResponse
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()


@router.get("/tasks", response_model=PaginatedResponse[TaskResponse], tags=["tasks"])
async def get_tasks(
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Number of items per page"),
    tenant_id: str = Query(description="ID of the tenant to filter tasks by"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_permission_checker(EPermission.VIEW_TASKS))
):
    """Retrieve all tasks accessible to the current user with pagination."""
    # Get all tenant IDs the user has access to
    user_tenant_ids = [t.id for t in current_user.tenants]
    
    if not user_tenant_ids:
        return PaginatedResponse(
            items=[],
            page=page,
            page_size=page_size,
            total_count=0,
            total_pages=0
        )

    offset = (page - 1) * page_size
    
    # Query tasks from all user's tenants
    tasks_query = db.query(Task).filter(Task.tenant_id.in_(user_tenant_ids))
    total_count = tasks_query.count()
    tasks = tasks_query.offset(offset).limit(page_size).all()
    
    return PaginatedResponse(
        items=tasks,
        page=page,
        page_size=page_size,
        total_count=total_count,
        total_pages=(total_count + page_size - 1) // page_size
    )


@router.post("/tasks", response_model=TaskResponse, tags=["tasks"], status_code=201)
async def create_task(
    task_data: TaskCreate,
    tenant_id: str = Query(description="ID of the tenant to create the task in"), 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_permission_checker(EPermission.CREATE_TASKS))
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


@router.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
async def get_task(
    task_id: str = Path(..., alias="resource_id", description="ID of the task to retrieve"),
    db: Session = Depends(get_db),
    current_user: User = Depends(requires_permission_for_resource(EPermission.VIEW_TASKS))
):
    """Retrieve a single task by its ID."""
    # Get all tenant IDs the user has access to
    user_tenant_ids = [t.id for t in current_user.tenants]
    
    # Query task from user's accessible tenants
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.tenant_id.in_(user_tenant_ids)
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found or access denied")
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
async def update_task(
    task_data: TaskUpdate,
    task_id: str = Path(..., alias="resource_id", description="ID of the task to update"),
    db: Session = Depends(get_db),
    current_user: User = Depends(requires_permission_for_resource(EPermission.EDIT_TASKS))
):
    """Update a task's details."""
    # Get all tenant IDs the user has access to
    user_tenant_ids = [t.id for t in current_user.tenants]
    
    # Find task in user's accessible tenants
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.tenant_id.in_(user_tenant_ids)
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found or access denied")

    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    
    db.commit()
    db.refresh(task)
    return task


@router.delete("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
async def delete_task(
    task_id: str = Path(..., alias="resource_id", description="ID of the task to delete"),
    db: Session = Depends(get_db),
    current_user: User = Depends(requires_permission_for_resource(EPermission.DELETE_TASKS))
):
    """Delete a task by its ID."""
    # Get all tenant IDs the user has access to
    user_tenant_ids = [t.id for t in current_user.tenants]
    
    # Find task in user's accessible tenants
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.tenant_id.in_(user_tenant_ids)
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found or access denied")

    db.delete(task)
    db.commit()
    return task
