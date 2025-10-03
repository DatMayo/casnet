"""
Pydantic schemas for calendar event data validation and response formatting.
"""
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class CalendarBase(BaseModel):
    """Base schema for calendar event data."""
    title: str = Field(description="Title of the calendar event")
    description: Optional[str] = Field(None, description="Detailed description of the event")
    location: Optional[str] = Field(None, description="Location of the event")
    start_date: datetime = Field(description="Start date and time of the event")
    end_date: datetime = Field(description="End date and time of the event")
    all_day: bool = Field(False, description="Indicates if the event is an all-day event")
    is_recurring: bool = Field(False, description="Indicates if the event is recurring")
    recurrence_rule: Optional[str] = Field(None, description="Recurrence rule (e.g., RRULE format)")
    organizer: Optional[str] = Field(None, description="Organizer of the event")
    attendees: Optional[str] = Field(None, description="Attendees of the event")
    status: int = Field(1, description="Status of the event (e.g., 1 for scheduled)")

class CalendarCreate(CalendarBase):
    """Schema for creating a new calendar event."""
    pass

class CalendarUpdate(BaseModel):
    """Schema for updating an existing calendar event. All fields are optional."""
    title: Optional[str] = Field(None, description="Updated title")
    description: Optional[str] = Field(None, description="Updated description")
    location: Optional[str] = Field(None, description="Updated location")
    start_date: Optional[datetime] = Field(None, description="Updated start date")
    end_date: Optional[datetime] = Field(None, description="Updated end date")
    all_day: Optional[bool] = Field(None, description="Updated all-day status")
    is_recurring: Optional[bool] = Field(None, description="Updated recurring status")
    recurrence_rule: Optional[str] = Field(None, description="Updated recurrence rule")
    organizer: Optional[str] = Field(None, description="Updated organizer")
    attendees: Optional[str] = Field(None, description="Updated attendees")
    status: Optional[int] = Field(None, description="Updated status")

class CalendarResponse(CalendarBase):
    """Schema for returning calendar event data in API responses."""
    id: str = Field(description="Unique identifier for the calendar event")
    tenant_id: str = Field(description="ID of the tenant this event belongs to")
    created_at: datetime = Field(description="Timestamp of event creation")
    updated_at: datetime = Field(description="Timestamp of last event update")
    duration_hours: float = Field(description="Duration of the event in hours")
    is_past: bool = Field(description="Indicates if the event is in the past")
    is_ongoing: bool = Field(description="Indicates if the event is currently ongoing")

    class Config:
        from_attributes = True
