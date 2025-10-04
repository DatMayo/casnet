"""
User management router for managing users, roles, and permissions within tenants.

This module provides endpoints for tenant administrators to manage users,
assign roles, and grant/revoke permissions.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, Tenant, UserTenantRole, UserTenantPermission
from ..dependencies import get_permission_service_dep, get_admin_or_owner_checker_from_path, get_role_checker_from_path
from ..permissions import PermissionService
from ..enum.erole import ERole
from ..enum.epermission import EPermission
from ..schemas.role import UserRoleAssignment, UserRoleUpdate, UserRoleResponse, UserWithRoleResponse, TenantRoleSummary
from ..schemas.permission import UserEffectivePermissions, UserPermissionAssignment, UserPermissionResponse

router = APIRouter()


@router.get("/tenants/{tenant_id}/users", response_model=List[UserWithRoleResponse], tags=["user-management"])
async def get_tenant_users(
    tenant_id: str = Path(description="ID of the tenant"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_or_owner_checker_from_path())
):
    """Get all users and their roles within a tenant (admin/owner only)."""
    user_roles = db.query(UserTenantRole).filter(UserTenantRole.tenant_id == tenant_id).all()
    return user_roles


@router.post("/tenants/{tenant_id}/users", response_model=UserRoleResponse, tags=["user-management"])
async def add_user_to_tenant(
    assignment: UserRoleAssignment,
    tenant_id: str = Path(description="ID of the tenant"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_or_owner_checker_from_path()),
    permission_service: PermissionService = Depends(get_permission_service_dep)
):
    """Add a user to a tenant with a specific role (admin/owner only)."""
    user_role = permission_service.assign_user_role(assignment.user_id, tenant_id, assignment.role)
    return user_role


@router.put("/tenants/{tenant_id}/users/{user_id}/role", response_model=UserRoleResponse, tags=["user-management"])
async def update_user_role(
    role_update: UserRoleUpdate,
    tenant_id: str = Path(description="ID of the tenant"),
    user_id: str = Path(description="ID of the user"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_or_owner_checker_from_path()),
    permission_service: PermissionService = Depends(get_permission_service_dep)
):
    """Update a user's role within a tenant (admin/owner only)."""
    user_role = permission_service.assign_user_role(user_id, tenant_id, role_update.role)
    return user_role


@router.delete("/tenants/{tenant_id}/users/{user_id}", tags=["user-management"])
async def remove_user_from_tenant(
    tenant_id: str = Path(description="ID of the tenant"),
    user_id: str = Path(description="ID of the user to remove"),
    current_user: User = Depends(get_role_checker_from_path(ERole.OWNER)),
    permission_service: PermissionService = Depends(get_permission_service_dep)
):
    """Remove a user from a tenant completely (owner only)."""
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot remove yourself from the tenant")
    
    removed = permission_service.remove_user_from_tenant(user_id, tenant_id)
    if not removed:
        raise HTTPException(status_code=404, detail="User not found in this tenant")
    
    return {"message": "User successfully removed from tenant"}


@router.get("/tenants/{tenant_id}/users/{user_id}/permissions", response_model=UserEffectivePermissions, tags=["user-management"])
async def get_user_permissions(
    tenant_id: str = Path(description="ID of the tenant"),
    user_id: str = Path(description="ID of the user"),
    current_user: User = Depends(get_admin_or_owner_checker_from_path()),
    permission_service: PermissionService = Depends(get_permission_service_dep)
):
    """Get a user's effective permissions within a tenant (admin/owner only)."""
    user_role = permission_service.get_user_role_in_tenant(user_id, tenant_id)
    if not user_role:
        raise HTTPException(status_code=404, detail="User not found in this tenant")
    
    role_permissions = list(permission_service.get_role_permissions(user_role))
    direct_permissions = list(permission_service.get_user_direct_permissions(user_id, tenant_id))
    effective_permissions = list(permission_service.get_user_effective_permissions(user_id, tenant_id))
    
    return UserEffectivePermissions(
        user_id=user_id,
        tenant_id=tenant_id,
        role=user_role,
        role_permissions=role_permissions,
        direct_permissions=direct_permissions,
        effective_permissions=effective_permissions
    )


@router.post("/tenants/{tenant_id}/users/{user_id}/permissions", response_model=UserPermissionResponse, tags=["user-management"])
async def assign_user_permission(
    permission_data: UserPermissionAssignment,
    tenant_id: str = Path(description="ID of the tenant"),
    user_id: str = Path(description="ID of the user"),
    current_user: User = Depends(get_admin_or_owner_checker_from_path()),
    permission_service: PermissionService = Depends(get_permission_service_dep)
):
    """Assign a direct permission to a user within a tenant (admin/owner only)."""
    if not permission_service.user_can_access_tenant(user_id, tenant_id):
        raise HTTPException(status_code=404, detail="User not found in this tenant")
    
    user_permission = permission_service.assign_user_permission(user_id, tenant_id, permission_data.permission)
    
    return UserPermissionResponse(
        id=user_permission.id,
        user_id=user_permission.user_id,
        tenant_id=user_permission.tenant_id,
        permission=user_permission.permission,
        created_at=user_permission.created_at,
        updated_at=user_permission.updated_at
    )


@router.delete("/tenants/{tenant_id}/users/{user_id}/permissions/{permission}", tags=["user-management"])
async def revoke_user_permission(
    tenant_id: str = Path(description="ID of the tenant"),
    user_id: str = Path(description="ID of the user"),
    permission: EPermission = Path(description="Permission to revoke"),
    current_user: User = Depends(get_admin_or_owner_checker_from_path()),
    permission_service: PermissionService = Depends(get_permission_service_dep)
):
    """Revoke a direct permission from a user within a tenant (admin/owner only)."""
    removed = permission_service.remove_user_permission(user_id, tenant_id, permission)
    if not removed:
        raise HTTPException(status_code=404, detail="Permission not found for this user in this tenant")
    
    return {"message": f"Permission '{permission.value}' revoked from user"}


@router.get("/tenants/{tenant_id}/role-summary", response_model=TenantRoleSummary, tags=["user-management"])
async def get_tenant_role_summary(
    tenant_id: str = Path(description="ID of the tenant"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_or_owner_checker_from_path()),
    permission_service: PermissionService = Depends(get_permission_service_dep)
):
    """Get a summary of roles within a tenant (admin/owner only)."""
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    user_roles = db.query(UserTenantRole).filter(UserTenantRole.tenant_id == tenant_id).all()
    
    total_users = len(user_roles)
    owners_count = sum(1 for ur in user_roles if ur.role == ERole.OWNER)
    admins_count = sum(1 for ur in user_roles if ur.role == ERole.ADMIN)
    users_count = sum(1 for ur in user_roles if ur.role == ERole.USER)
    
    return TenantRoleSummary(
        tenant_id=tenant_id,
        tenant_name=tenant.name,
        total_users=total_users,
        owners_count=owners_count,
        admins_count=admins_count,
        users_count=users_count
    )
