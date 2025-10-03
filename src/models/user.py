"""
User model with authentication and tenant relationships.
"""
from typing import List

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


# Association table for many-to-many relationship between users and tenants
user_tenant_association = Table(
    'user_tenants',
    Base.metadata,
    Column('user_id', String(36), ForeignKey('users.id'), primary_key=True),
    Column('tenant_id', String(36), ForeignKey('tenants.id'), primary_key=True),
)


class User(Base, UUIDMixin, TimestampMixin):
    """User model for authentication and authorization."""
    
    __tablename__ = 'users'
    
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Many-to-many relationship with tenants
    tenants: Mapped[List["Tenant"]] = relationship(
        "Tenant",
        secondary=user_tenant_association,
        back_populates="users",
        lazy="selectin"
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name})>"
