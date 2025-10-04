"""
Pydantic schemas for user data validation and response formatting.
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

from .tenant import TenantResponse
from ..enum.erole import ERole
from ..enum.epermission import EPermission

class UserBase(BaseModel):
    """Base schema for user data."""
    name: str = Field(description="Username for the user account")

class UserCreate(BaseModel):
    """Schema for creating a new user."""
    name: str = Field(description="Username for the new user account")
    password: str = Field(description="Password for the new user account")

class UserUpdate(BaseModel):
    """Schema for updating an existing user. All fields are optional."""
    name: Optional[str] = Field(None, description="Updated username")
    password: Optional[str] = Field(None, description="Optional new password")

class UserTenantInfo(BaseModel):
    """Schema for user's tenant access information."""
    tenant: TenantResponse = Field(description="Tenant information")
    role: ERole = Field(description="User's role in this tenant")
    effective_permissions: List[EPermission] = Field(description="User's effective permissions in this tenant")
    
    class Config:
        from_attributes = True


class UserResponse(UserBase):
    """Schema for returning user data in API responses."""
    id: str = Field(description="Unique identifier for the user")
    created_at: datetime = Field(description="Timestamp of user creation")
    updated_at: datetime = Field(description="Timestamp of last user update")
    tenants: List[TenantResponse] = Field([], description="List of tenants the user is assigned to")

    class Config:
        from_attributes = True


class UserDetailedResponse(UserBase):
    """Schema for returning detailed user data with role and permission information."""
    id: str = Field(description="Unique identifier for the user")
    created_at: datetime = Field(description="Timestamp of user creation")
    updated_at: datetime = Field(description="Timestamp of last user update")
    tenant_access: List[UserTenantInfo] = Field([], description="Detailed tenant access with roles and permissions")

    class Config:
        from_attributes = True
