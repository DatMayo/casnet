"""
Calendar model for event management within tenants.
"""
from typing import Optional
from datetime import datetime

from sqlalchemy import String, Text, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class Calendar(Base, UUIDMixin, TimestampMixin):
    """Calendar model for managing events within a tenant."""
    
    __tablename__ = 'calendar_events'
    
    # Basic event information
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Event timing
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    all_day: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Event properties
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    recurrence_rule: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # RRULE format
    
    # Organizer and attendees (could be extended to reference Person model)
    organizer: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    attendees: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string or comma-separated
    
    # Event status
    status: Mapped[int] = mapped_column(Integer, default=1, nullable=False)  # 1=scheduled, 2=cancelled, 3=completed
    
    # Foreign key to tenant
    tenant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('tenants.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    # Relationship back to tenant
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="calendar_events")
    
    @property
    def duration_hours(self) -> float:
        """Calculate the duration of the event in hours."""
        if self.end_date and self.start_date:
            delta = self.end_date - self.start_date
            return delta.total_seconds() / 3600
        return 0.0
    
    @property
    def is_past(self) -> bool:
        """Check if the event is in the past."""
        return self.end_date < datetime.now()
    
    @property
    def is_ongoing(self) -> bool:
        """Check if the event is currently ongoing."""
        now = datetime.now()
        return self.start_date <= now <= self.end_date
    
    def __repr__(self) -> str:
        return f"<Calendar(id={self.id}, title={self.title}, start={self.start_date}, tenant_id={self.tenant_id})>"
