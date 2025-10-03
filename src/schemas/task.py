"""
Pydantic schemas for task data validation and response formatting.
"""
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class TaskBase(BaseModel):
    """Base schema for task data."""
    title: str = Field(description="Title of the task")
    description: Optional[str] = Field(None, description="Detailed description of the task")
    status: int = Field(1, description="Status of the task (e.g., 1 for pending)")
    priority: int = Field(2, description="Priority of the task (e.g., 2 for medium)")
    due_date: Optional[datetime] = Field(None, description="Due date for the task")
    assigned_to: Optional[str] = Field(None, description="Who the task is assigned to")

class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass

class TaskUpdate(BaseModel):
    """Schema for updating an existing task. All fields are optional."""
    title: Optional[str] = Field(None, description="Updated title")
    description: Optional[str] = Field(None, description="Updated description")
    status: Optional[int] = Field(None, description="Updated status")
    priority: Optional[int] = Field(None, description="Updated priority")
    due_date: Optional[datetime] = Field(None, description="Updated due date")
    assigned_to: Optional[str] = Field(None, description="Updated assignee")

class TaskResponse(TaskBase):
    """Schema for returning task data in API responses."""
    id: str = Field(description="Unique identifier for the task")
    tenant_id: str = Field(description="ID of the tenant this task belongs to")
    created_at: datetime = Field(description="Timestamp of task creation")
    updated_at: datetime = Field(description="Timestamp of last task update")
    completed_at: Optional[datetime] = Field(None, description="Timestamp when the task was completed")
    is_completed: bool = Field(description="Indicates if the task is completed")
    is_overdue: bool = Field(description="Indicates if the task is overdue")

    class Config:
        from_attributes = True
