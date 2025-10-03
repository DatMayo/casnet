"""
Person model for individual profiles within tenants.
"""
from typing import Optional

from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class Person(Base, UUIDMixin, TimestampMixin):
    """Person model representing individual profiles within a tenant."""
    
    __tablename__ = 'persons'
    
    # Basic information
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Optional fields that can be extended
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Status field (can be used for active/inactive, etc.)
    status: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    
    # Foreign key to tenant
    tenant_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey('tenants.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    # Relationship back to tenant
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="persons")
    
    @property
    def full_name(self) -> str:
        """Get the full name of the person."""
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self) -> str:
        return f"<Person(id={self.id}, name={self.full_name}, tenant_id={self.tenant_id})>"
