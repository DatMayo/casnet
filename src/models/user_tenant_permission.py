"""
UserTenantPermission model for tracking specific permissions granted to users within tenants.
"""
from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin
from ..enum.epermission import EPermission


class UserTenantPermission(Base, UUIDMixin, TimestampMixin):
    """Grants specific permissions to users within specific tenants."""
    
    __tablename__ = 'user_tenant_permissions'
    
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey('users.id'), nullable=False)
    tenant_id: Mapped[str] = mapped_column(String(36), ForeignKey('tenants.id'), nullable=False)
    permission: Mapped[EPermission] = mapped_column(Enum(EPermission), nullable=False)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="tenant_permissions")
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="user_permissions")
    
    def __repr__(self) -> str:
        return f"<UserTenantPermission(user_id={self.user_id}, tenant_id={self.tenant_id}, permission={self.permission.value})>"
