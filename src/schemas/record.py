"""
Pydantic schemas for record data validation and response formatting.
"""
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class RecordBase(BaseModel):
    """Base schema for record data."""
    title: str = Field(description="Title of the record")
    description: Optional[str] = Field(None, description="Detailed description of the record")
    record_type: str = Field(description="Type of the record (e.g., incident, case)")
    category: Optional[str] = Field(None, description="Category of the record")
    status: int = Field(1, description="Status of the record (e.g., 1 for open)")
    priority: int = Field(2, description="Priority of the record (e.g., 2 for medium)")
    incident_date: Optional[datetime] = Field(None, description="Date of the incident")
    location: Optional[str] = Field(None, description="Location of the incident")
    reporter: Optional[str] = Field(None, description="Person who reported the incident")
    assigned_officer: Optional[str] = Field(None, description="Officer assigned to the record")
    evidence: Optional[str] = Field(None, description="Evidence related to the record")
    notes: Optional[str] = Field(None, description="Additional notes about the record")

class RecordCreate(RecordBase):
    """Schema for creating a new record."""
    pass

class RecordUpdate(BaseModel):
    """Schema for updating an existing record. All fields are optional."""
    title: Optional[str] = Field(None, description="Updated title")
    description: Optional[str] = Field(None, description="Updated description")
    record_type: Optional[str] = Field(None, description="Updated record type")
    category: Optional[str] = Field(None, description="Updated category")
    status: Optional[int] = Field(None, description="Updated status")
    priority: Optional[int] = Field(None, description="Updated priority")
    incident_date: Optional[datetime] = Field(None, description="Updated incident date")
    location: Optional[str] = Field(None, description="Updated location")
    reporter: Optional[str] = Field(None, description="Updated reporter")
    assigned_officer: Optional[str] = Field(None, description="Updated assigned officer")
    evidence: Optional[str] = Field(None, description="Updated evidence")
    notes: Optional[str] = Field(None, description="Updated notes")

class RecordResponse(RecordBase):
    """Schema for returning record data in API responses."""
    id: str = Field(description="Unique identifier for the record")
    tenant_id: str = Field(description="ID of the tenant this record belongs to")
    created_at: datetime = Field(description="Timestamp of record creation")
    updated_at: datetime = Field(description="Timestamp of last record update")
    closed_at: Optional[datetime] = Field(None, description="Timestamp when the record was closed")
    is_open: bool = Field(description="Indicates if the record is open")
    is_closed: bool = Field(description="Indicates if the record is closed")
    days_open: int = Field(description="Number of days the record has been open")

    class Config:
        from_attributes = True
