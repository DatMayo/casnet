"""
Task model for task management within tenants.
"""
from typing import Optional
from datetime import datetime

from sqlalchemy import String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class Task(Base, UUIDMixin, TimestampMixin):
    """Task model for managing tasks within a tenant."""
    
    __tablename__ = 'tasks'
    
    # Basic task information
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Task status and priority
    status: Mapped[int] = mapped_column(Integer, default=1, nullable=False)  # 1=pending, 2=in_progress, 3=completed
    priority: Mapped[int] = mapped_column(Integer, default=2, nullable=False)  # 1=high, 2=medium, 3=low
    
    # Dates
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Assignment (could be extended to reference Person model in the future)
    assigned_to: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Foreign key to tenant
    tenant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('tenants.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    # Relationship back to tenant
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="tasks")
    
    @property
    def is_completed(self) -> bool:
        """Check if the task is completed."""
        return self.status == 3
    
    @property
    def is_overdue(self) -> bool:
        """Check if the task is overdue."""
        if self.due_date and not self.is_completed:
            return datetime.now() > self.due_date
        return False
    
    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title={self.title}, status={self.status}, tenant_id={self.tenant_id})>"
