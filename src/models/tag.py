"""
Tag model for categorization and labeling within tenants.
"""
from typing import Optional

from sqlalchemy import String, Text, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class Tag(Base, UUIDMixin, TimestampMixin):
    """Tag model for categorizing and labeling items within a tenant."""
    
    __tablename__ = 'tags'
    
    # Basic tag information
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Tag appearance
    color: Mapped[Optional[str]] = mapped_column(String(7), nullable=True)  # Hex color code (#RRGGBB)
    
    # Tag category and usage
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)  # e.g. "priority", "status", "type"
    usage_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # Track how often used
    
    # Tag status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Foreign key to tenant
    tenant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('tenants.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    # Relationship back to tenant
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="tags")
    
    def increment_usage(self) -> None:
        """Increment the usage count of this tag."""
        self.usage_count += 1
    
    def __repr__(self) -> str:
        return f"<Tag(id={self.id}, name={self.name}, category={self.category}, tenant_id={self.tenant_id})>"
