"""
Pydantic schemas for tag data validation and response formatting.
"""
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class TagBase(BaseModel):
    """Base schema for tag data."""
    name: str = Field(description="Name of the tag")
    description: Optional[str] = Field(None, description="Detailed description of the tag")
    color: Optional[str] = Field(None, description="Hex color code for the tag (e.g., #RRGGBB)")
    category: Optional[str] = Field(None, description="Category of the tag")

class TagCreate(TagBase):
    """Schema for creating a new tag."""
    pass

class TagUpdate(BaseModel):
    """Schema for updating an existing tag. All fields are optional."""
    name: Optional[str] = Field(None, description="Updated name")
    description: Optional[str] = Field(None, description="Updated description")
    color: Optional[str] = Field(None, description="Updated color code")
    category: Optional[str] = Field(None, description="Updated category")
    is_active: Optional[bool] = Field(None, description="Updated active status")

class TagResponse(TagBase):
    """Schema for returning tag data in API responses."""
    id: str = Field(description="Unique identifier for the tag")
    tenant_id: str = Field(description="ID of the tenant this tag belongs to")
    created_at: datetime = Field(description="Timestamp of tag creation")
    updated_at: datetime = Field(description="Timestamp of last tag update")
    usage_count: int = Field(description="How often the tag has been used")
    is_active: bool = Field(description="Indicates if the tag is active")

    class Config:
        from_attributes = True
