"""
Pydantic schemas for tenant data validation and response formatting.
"""
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from ..enum.estatus import EStatus


class TenantBase(BaseModel):
    """Base schema for tenant data."""
    name: str = Field(description="Name of the tenant organization")
    description: Optional[str] = Field(None, description="Optional description of the tenant")


class TenantCreate(TenantBase):
    """Schema for creating a new tenant."""
    pass


class TenantUpdate(BaseModel):
    """Schema for updating an existing tenant. All fields are optional."""
    name: Optional[str] = Field(None, description="Updated name for the tenant")
    description: Optional[str] = Field(None, description="Updated description for the tenant")
    status: Optional[EStatus] = Field(None, description="Updated status for the tenant")


class TenantResponse(TenantBase):
    """Schema for returning tenant data in API responses."""
    id: str = Field(description="Unique identifier for the tenant")
    status: EStatus = Field(description="Current status of the tenant")
    created_at: datetime = Field(description="Timestamp of tenant creation")
    updated_at: datetime = Field(description="Timestamp of last tenant update")

    class Config:
        from_attributes = True
