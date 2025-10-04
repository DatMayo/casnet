"""
Pydantic schemas for permission management within tenants.
"""
from typing import List, Set, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from ..enum.epermission import EPermission
from ..enum.erole import ERole


class UserPermissionAssignment(BaseModel):
    """Schema for assigning a permission to a user within a tenant."""
    user_id: str = Field(description="ID of the user to assign the permission to")
    permission: EPermission = Field(description="Permission to assign to the user")


class BulkUserPermissionAssignment(BaseModel):
    """Schema for assigning multiple permissions to a user within a tenant."""
    user_id: str = Field(description="ID of the user to assign permissions to")
    permissions: List[EPermission] = Field(description="List of permissions to assign")


class UserPermissionRemoval(BaseModel):
    """Schema for removing a permission from a user within a tenant.""" 
    user_id: str = Field(description="ID of the user to remove the permission from")
    permission: EPermission = Field(description="Permission to remove from the user")


class UserPermissionResponse(BaseModel):
    """Schema for returning user permission information."""
    id: str = Field(description="Unique identifier for the permission assignment")
    user_id: str = Field(description="ID of the user")
    tenant_id: str = Field(description="ID of the tenant")
    permission: EPermission = Field(description="Permission granted to the user")
    created_at: datetime = Field(description="When the permission was granted")
    updated_at: datetime = Field(description="When the permission was last updated")
    
    class Config:
        from_attributes = True


class UserEffectivePermissions(BaseModel):
    """Schema for returning a user's effective permissions within a tenant."""
    user_id: str = Field(description="User ID")
    tenant_id: str = Field(description="Tenant ID")
    role: Optional[ERole] = Field(None, description="User's role in the tenant")
    role_permissions: List[EPermission] = Field(description="Permissions from role")
    direct_permissions: List[EPermission] = Field(description="Directly assigned permissions")
    effective_permissions: List[EPermission] = Field(description="All effective permissions (role + direct)")
    
    class Config:
        from_attributes = True


class UserWithPermissions(BaseModel):
    """Schema for returning user information with their permissions in a tenant."""
    id: str = Field(description="User ID")
    name: str = Field(description="Username")
    role: Optional[ERole] = Field(None, description="User's role in the tenant")
    direct_permissions: List[EPermission] = Field(description="Directly assigned permissions")
    effective_permissions: List[EPermission] = Field(description="All effective permissions")
    
    class Config:
        from_attributes = True


class PermissionCheck(BaseModel):
    """Schema for checking if a user has a specific permission."""
    user_id: str = Field(description="User ID to check")
    tenant_id: str = Field(description="Tenant ID to check in")
    permission: EPermission = Field(description="Permission to check for")


class PermissionCheckResult(BaseModel):
    """Schema for returning permission check results."""
    user_id: str = Field(description="User ID")
    tenant_id: str = Field(description="Tenant ID")
    permission: EPermission = Field(description="Permission checked")
    has_permission: bool = Field(description="Whether the user has the permission")
    source: str = Field(description="Source of permission ('role', 'direct', or 'none')")
    
    class Config:
        from_attributes = True


class TenantPermissionSummary(BaseModel):
    """Schema for summarizing permissions within a tenant."""
    tenant_id: str = Field(description="Tenant ID")
    tenant_name: str = Field(description="Tenant name")
    total_users: int = Field(description="Total number of users")
    permission_assignments: int = Field(description="Total direct permission assignments")
    most_common_permissions: List[EPermission] = Field(description="Most commonly assigned permissions")
    
    class Config:
        from_attributes = True


class PermissionCategory(BaseModel):
    """Schema for grouping permissions by category."""
    category: str = Field(description="Permission category (e.g., 'persons', 'tasks')")
    permissions: List[EPermission] = Field(description="Permissions in this category")
    
    class Config:
        from_attributes = True
