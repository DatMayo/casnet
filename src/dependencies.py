"""
FastAPI dependencies for permission and role checking.

This module provides dependency functions that can be used to protect routes
with specific permission or role requirements.
"""
from typing import Callable, Optional
from functools import wraps
from fastapi import Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session

from .database import get_db
from .models import User
from .security import get_current_user
from .permissions import get_permission_service, PermissionService
from .enum.epermission import EPermission
from .enum.erole import ERole


def get_permission_checker(permission: EPermission) -> Callable:
    """Factory for creating a permission checking dependency."""
    def _check_permission(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
        tenant_id: str = Query(..., description="ID of the tenant")
    ) -> User:
        permission_service = get_permission_service(db)
        if not permission_service.user_has_permission(current_user.id, tenant_id, permission):
            raise HTTPException(
                status_code=403,
                detail=f"Access denied: You don't have permission '{permission.value}' in this tenant"
            )
        return current_user
    return _check_permission

def get_role_checker(role: ERole) -> Callable:
    """Factory for creating a role checking dependency."""
    def _check_role(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
        tenant_id: str = Query(..., description="ID of the tenant")
    ) -> User:
        permission_service = get_permission_service(db)
        if not permission_service.user_has_role(current_user.id, tenant_id, role):
            raise HTTPException(
                status_code=403,
                detail=f"Access denied: You must be a '{role.value}' to perform this action"
            )
        return current_user
    return _check_role

def get_admin_or_owner_checker() -> Callable:
    """Factory for creating an admin-or-owner checking dependency."""
    def _check_admin_or_owner(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
        tenant_id: str = Query(..., description="ID of the tenant")
    ) -> User:
        permission_service = get_permission_service(db)
        if not permission_service.user_is_admin_or_owner(current_user.id, tenant_id):
            raise HTTPException(
                status_code=403,
                detail="Access denied: You must be an admin or owner to perform this action"
            )
        return current_user
    return _check_admin_or_owner




def requires_permission(permission: EPermission) -> Callable:
    """Dependency to check for a specific permission from a query parameter tenant_id."""
    return get_permission_checker(permission)

def requires_role(role: ERole) -> Callable:
    """Dependency to check for a specific role from a query parameter tenant_id."""
    return get_role_checker(role)

def requires_admin_or_owner() -> Callable:
    """Dependency to check for admin or owner role from a query parameter tenant_id."""
    return get_admin_or_owner_checker()

def requires_owner() -> Callable:
    """Dependency to check for owner role from a query parameter tenant_id."""
    return get_role_checker(ERole.OWNER)



# Dependency to get PermissionService
def requires_permission_for_resource(permission: EPermission) -> Callable:
    """Dependency that checks permission for a resource fetched from the database."""
    def _check_permission(
        resource_id: str = Path(..., description="The ID of the resource to access"),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> User:
        permission_service = get_permission_service(db)
        
        # This is a generic dependency, so we have to make some assumptions.
        # We assume the resource has a 'tenant_id' attribute.
        # A more robust solution might involve a mapping of resource types to table models.
        
        # Find the tenant_id from the resource
        tenant_id = permission_service.get_tenant_id_for_resource(resource_id)
        
        if not tenant_id:
            raise HTTPException(status_code=404, detail="Resource not found or does not belong to a tenant")

        if not permission_service.user_has_permission(current_user.id, tenant_id, permission):
            raise HTTPException(
                status_code=403,
                detail=f"Access denied: You don't have permission '{permission.value}' in this tenant"
            )
        return current_user
    return _check_permission

# --- Path-based Checkers ---

def get_permission_checker_from_path(permission: EPermission) -> Callable:
    """Factory for creating a permission checker that reads tenant_id from the path."""
    def _check_permission(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
        tenant_id: str = Path(..., description="ID of the tenant")
    ) -> User:
        permission_service = get_permission_service(db)
        if not permission_service.user_has_permission(current_user.id, tenant_id, permission):
            raise HTTPException(
                status_code=403,
                detail=f"Access denied: You don't have permission '{permission.value}' in this tenant"
            )
        return current_user
    return _check_permission

def get_role_checker_from_path(role: ERole) -> Callable:
    """Factory for creating a role checker that reads tenant_id from the path."""
    def _check_role(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
        tenant_id: str = Path(..., description="ID of the tenant")
    ) -> User:
        permission_service = get_permission_service(db)
        if not permission_service.user_has_role(current_user.id, tenant_id, role):
            raise HTTPException(
                status_code=403,
                detail=f"Access denied: You must be a '{role.value}' to perform this action"
            )
        return current_user
    return _check_role

def get_admin_or_owner_checker_from_path() -> Callable:
    """Factory for creating an admin-or-owner checker that reads tenant_id from the path."""
    def _check_admin_or_owner(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
        tenant_id: str = Path(..., description="ID of the tenant")
    ) -> User:
        permission_service = get_permission_service(db)
        if not permission_service.user_is_admin_or_owner(current_user.id, tenant_id):
            raise HTTPException(
                status_code=403,
                detail="Access denied: You must be an admin or owner to perform this action"
            )
        return current_user
    return _check_admin_or_owner


def get_permission_service_dep(db: Session = Depends(get_db)) -> PermissionService:
    """Dependency to get PermissionService instance."""
    return get_permission_service(db)
