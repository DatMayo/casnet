"""
Tenant model for multi-tenant organization.
"""
from typing import List, Optional

from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin
from .user import user_tenant_association


class Tenant(Base, UUIDMixin, TimestampMixin):
    """Tenant model representing departments or organizations."""
    
    __tablename__ = 'tenants'
    
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[int] = mapped_column(Integer, default=1, nullable=False)  # 1=active, 0=inactive
    
    # Many-to-many relationship with users
    users: Mapped[List["User"]] = relationship(
        "User",
        secondary=user_tenant_association,
        back_populates="tenants",
        lazy="selectin"
    )
    
    # One-to-many relationships with other entities
    persons: Mapped[List["Person"]] = relationship(
        "Person", 
        back_populates="tenant",
        cascade="all, delete-orphan",
        lazy="select"
    )
    
    tasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="tenant", 
        cascade="all, delete-orphan",
        lazy="select"
    )
    
    calendar_events: Mapped[List["Calendar"]] = relationship(
        "Calendar",
        back_populates="tenant",
        cascade="all, delete-orphan", 
        lazy="select"
    )
    
    records: Mapped[List["Record"]] = relationship(
        "Record",
        back_populates="tenant",
        cascade="all, delete-orphan",
        lazy="select"
    )
    
    tags: Mapped[List["Tag"]] = relationship(
        "Tag",
        back_populates="tenant",
        cascade="all, delete-orphan",
        lazy="select"
    )
    
    def __repr__(self) -> str:
        return f"<Tenant(id={self.id}, name={self.name}, status={self.status})>"
