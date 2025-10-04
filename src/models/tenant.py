"""
Tenant model for multi-tenant organization.
"""
from typing import List, Optional

from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class Tenant(Base, UUIDMixin, TimestampMixin):
    """Tenant model representing departments or organizations."""
    
    __tablename__ = 'tenants'
    
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[int] = mapped_column(Integer, default=1, nullable=False)  # 1=active, 0=inactive
    
    # Role-based relationship with users
    user_roles: Mapped[List["UserTenantRole"]] = relationship(
        "UserTenantRole",
        back_populates="tenant",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    # Permission-based relationship with users
    user_permissions: Mapped[List["UserTenantPermission"]] = relationship(
        "UserTenantPermission",
        back_populates="tenant",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    # Convenience property to get users (for backward compatibility)
    @property
    def users(self) -> List["User"]:
        """Get all users that have access to this tenant."""
        return [role.user for role in self.user_roles]
    
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
