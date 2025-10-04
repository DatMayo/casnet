"""
User model with authentication and tenant relationships.
"""
from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class User(Base, UUIDMixin, TimestampMixin):
    """User model for authentication and authorization."""
    
    __tablename__ = 'users'
    
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Role-based relationship with tenants
    tenant_roles: Mapped[List["UserTenantRole"]] = relationship(
        "UserTenantRole",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    # Permission-based relationship with tenants
    tenant_permissions: Mapped[List["UserTenantPermission"]] = relationship(
        "UserTenantPermission",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    # Convenience property to get tenants (for backward compatibility)
    @property
    def tenants(self) -> List["Tenant"]:
        """Get all tenants this user has access to."""
        return [role.tenant for role in self.tenant_roles]
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name})>"
