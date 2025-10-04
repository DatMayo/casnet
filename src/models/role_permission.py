"""
RolePermission model for defining default permissions that each role has.
"""
from sqlalchemy import Column, Enum
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, UUIDMixin
from ..enum.erole import ERole
from ..enum.epermission import EPermission


class RolePermission(Base, UUIDMixin, TimestampMixin):
    """Defines which permissions each role has by default."""
    
    __tablename__ = 'role_permissions'
    
    role: Mapped[ERole] = mapped_column(Enum(ERole), nullable=False)
    permission: Mapped[EPermission] = mapped_column(Enum(EPermission), nullable=False)
    
    def __repr__(self) -> str:
        return f"<RolePermission(role={self.role.value}, permission={self.permission.value})>"
