"""
Record model for case/record management within tenants.
"""
from typing import Optional
from datetime import datetime

from sqlalchemy import String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class Record(Base, UUIDMixin, TimestampMixin):
    """Record model for managing cases/records within a tenant."""
    
    __tablename__ = 'records'
    
    # Basic record information
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Record type and category
    record_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # e.g. "incident", "case", "report"
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    
    # Record status and priority
    status: Mapped[int] = mapped_column(Integer, default=1, nullable=False)  # 1=open, 2=in_progress, 3=closed
    priority: Mapped[int] = mapped_column(Integer, default=2, nullable=False)  # 1=high, 2=medium, 3=low
    
    # Record details
    incident_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # People involved (could be extended to reference Person model)
    reporter: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    assigned_officer: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Additional details
    evidence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string or text
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Dates
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Foreign key to tenant
    tenant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('tenants.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    # Relationship back to tenant
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="records")
    
    @property
    def is_open(self) -> bool:
        """Check if the record is open."""
        return self.status == 1
    
    @property
    def is_closed(self) -> bool:
        """Check if the record is closed."""
        return self.status == 3
    
    @property
    def days_open(self) -> int:
        """Calculate how many days the record has been open."""
        if self.is_closed and self.closed_at:
            return (self.closed_at - self.created_at).days
        else:
            return (datetime.now() - self.created_at).days
    
    def __repr__(self) -> str:
        return f"<Record(id={self.id}, title={self.title}, type={self.record_type}, status={self.status}, tenant_id={self.tenant_id})>"
