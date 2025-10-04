"""
Pydantic schemas for role management within tenants.
"""
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from ..enum.erole import ERole
from ..enum.epermission import EPermission


class UserRoleAssignment(BaseModel):
    """Schema for assigning a role to a user within a tenant."""
    user_id: str = Field(description="ID of the user to assign the role to")
    role: ERole = Field(description="Role to assign to the user")


class UserRoleUpdate(BaseModel):
    """Schema for updating a user's role within a tenant."""
    role: ERole = Field(description="New role for the user")


class UserRoleResponse(BaseModel):
    """Schema for returning user role information."""
    id: str = Field(description="Unique identifier for the role assignment")
    user_id: str = Field(description="ID of the user")
    tenant_id: str = Field(description="ID of the tenant") 
    role: ERole = Field(description="User's role in the tenant")
    created_at: datetime = Field(description="When the role was assigned")
    updated_at: datetime = Field(description="When the role was last updated")
    
    class Config:
        from_attributes = True


class UserWithRoleResponse(BaseModel):
    """Schema for returning user information with their role in a tenant."""
    id: str = Field(description="User ID")
    name: str = Field(description="Username")
    role: ERole = Field(description="User's role in the tenant")
    role_assigned_at: datetime = Field(description="When the role was assigned")
    
    class Config:
        from_attributes = True


class TenantRoleSummary(BaseModel):
    """Schema for summarizing roles within a tenant."""
    tenant_id: str = Field(description="Tenant ID")
    tenant_name: str = Field(description="Tenant name")
    total_users: int = Field(description="Total number of users in tenant")
    owners_count: int = Field(description="Number of owners")
    admins_count: int = Field(description="Number of admins") 
    users_count: int = Field(description="Number of regular users")
    
    class Config:
        from_attributes = True


class RolePermissionMapping(BaseModel):
    """Schema for role-permission default mappings."""
    role: ERole = Field(description="Role")
    permissions: List[EPermission] = Field(description="Default permissions for this role")
    
    class Config:
        from_attributes = True
