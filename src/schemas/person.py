"""
Pydantic schemas for person data validation and response formatting.
"""
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class PersonBase(BaseModel):
    """Base schema for person data."""
    first_name: str = Field(description="First name of the person")
    last_name: str = Field(description="Last name of the person")
    email: Optional[str] = Field(None, description="Email address of the person")
    phone: Optional[str] = Field(None, description="Phone number of the person")
    address: Optional[str] = Field(None, description="Physical address of the person")
    notes: Optional[str] = Field(None, description="Additional notes about the person")
    status: int = Field(1, description="Status of the person (e.g., 1 for active)")

class PersonCreate(PersonBase):
    """Schema for creating a new person."""
    pass

class PersonUpdate(BaseModel):
    """Schema for updating an existing person. All fields are optional."""
    first_name: Optional[str] = Field(None, description="Updated first name")
    last_name: Optional[str] = Field(None, description="Updated last name")
    email: Optional[str] = Field(None, description="Updated email address")
    phone: Optional[str] = Field(None, description="Updated phone number")
    address: Optional[str] = Field(None, description="Updated physical address")
    notes: Optional[str] = Field(None, description="Updated notes")
    status: Optional[int] = Field(None, description="Updated status")

class PersonResponse(PersonBase):
    """Schema for returning person data in API responses."""
    id: str = Field(description="Unique identifier for the person")
    tenant_id: str = Field(description="ID of the tenant this person belongs to")
    created_at: datetime = Field(description="Timestamp of person creation")
    updated_at: datetime = Field(description="Timestamp of last person update")
    full_name: str = Field(description="Full name of the person")

    class Config:
        from_attributes = True
