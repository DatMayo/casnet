"""
UserTenantRole model for tracking user roles within specific tenants.
"""
from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin
from ..enum.erole import ERole


class UserTenantRole(Base, UUIDMixin, TimestampMixin):
    """Associates users with tenants and their roles within those tenants."""
    
    __tablename__ = 'user_tenant_roles'
    
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey('users.id'), nullable=False)
    tenant_id: Mapped[str] = mapped_column(String(36), ForeignKey('tenants.id'), nullable=False)
    role: Mapped[ERole] = mapped_column(Enum(ERole), nullable=False, default=ERole.USER)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="tenant_roles")
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="user_roles")
    
    def __repr__(self) -> str:
        return f"<UserTenantRole(user_id={self.user_id}, tenant_id={self.tenant_id}, role={self.role.value})>"
