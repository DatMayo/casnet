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


class PermissionDependency:
    """Dependency class for checking user permissions."""
    
    def __init__(self, permission: EPermission, tenant_from: str = "query"):
        """
        Initialize permission dependency.
        
        Args:
            permission: The required permission
            tenant_from: Where to get tenant_id from ("query", "path", or "auto")
        """
        self.permission = permission
        self.tenant_from = tenant_from
    
    def __call__(
        self,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
        tenant_id: Optional[str] = Query(None, description="Tenant ID"),
        tenant_id_path: Optional[str] = Query(None, alias="tenant_id_path")
    ) -> User:
        """Check if current user has the required permission."""
        permission_service = get_permission_service(db)
        
        # Determine tenant_id based on tenant_from parameter
        if self.tenant_from == "query" and tenant_id:
            target_tenant_id = tenant_id
        elif self.tenant_from == "path" and tenant_id_path:
            target_tenant_id = tenant_id_path
        elif self.tenant_from == "auto":
            target_tenant_id = tenant_id or tenant_id_path
        else:
            raise HTTPException(
                status_code=400,
                detail="Tenant ID is required for this operation"
            )
        
        if not target_tenant_id:
            raise HTTPException(
                status_code=400,
                detail="Tenant ID is required for this operation"
            )
        
        # Check if user can access the tenant
        if not permission_service.user_can_access_tenant(current_user.id, target_tenant_id):
            raise HTTPException(
                status_code=403,
                detail=f"Access denied: You don't have access to tenant {target_tenant_id}"
            )
        
        # Check if user has the required permission
        if not permission_service.user_has_permission(current_user.id, target_tenant_id, self.permission):
            raise HTTPException(
                status_code=403,
                detail=f"Access denied: You don't have permission '{self.permission.value}' in this tenant"
            )
        
        return current_user


class RoleDependency:
    """Dependency class for checking user roles."""
    
    def __init__(self, role: ERole, tenant_from: str = "query"):
        """
        Initialize role dependency.
        
        Args:
            role: The required role
            tenant_from: Where to get tenant_id from ("query", "path", or "auto")
        """
        self.role = role
        self.tenant_from = tenant_from
    
    def __call__(
        self,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
        tenant_id: Optional[str] = Query(None, description="Tenant ID"),
        tenant_id_path: Optional[str] = Query(None, alias="tenant_id_path")
    ) -> User:
        """Check if current user has the required role."""
        permission_service = get_permission_service(db)
        
        # Determine tenant_id based on tenant_from parameter
        if self.tenant_from == "query" and tenant_id:
            target_tenant_id = tenant_id
        elif self.tenant_from == "path" and tenant_id_path:
            target_tenant_id = tenant_id_path
        elif self.tenant_from == "auto":
            target_tenant_id = tenant_id or tenant_id_path
        else:
            raise HTTPException(
                status_code=400,
                detail="Tenant ID is required for this operation"
            )
        
        if not target_tenant_id:
            raise HTTPException(
                status_code=400,
                detail="Tenant ID is required for this operation"
            )
        
        # Check if user has the required role
        if not permission_service.user_has_role(current_user.id, target_tenant_id, self.role):
            raise HTTPException(
                status_code=403,
                detail=f"Access denied: You must be a '{self.role.value}' to perform this action"
            )
        
        return current_user


# Convenience functions for common permission checks
def requires_permission(permission: EPermission, tenant_from: str = "query"):
    """Decorator factory for requiring specific permissions."""
    return Depends(PermissionDependency(permission, tenant_from))


def requires_role(role: ERole, tenant_from: str = "query"):
    """Decorator factory for requiring specific roles.""" 
    return Depends(RoleDependency(role, tenant_from))


def requires_owner(tenant_from: str = "query"):
    """Require OWNER role."""
    return requires_role(ERole.OWNER, tenant_from)


def requires_admin_or_owner(tenant_from: str = "query"):
    """Require ADMIN or OWNER role."""
    def check_admin_or_owner(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
        tenant_id: Optional[str] = Query(None, description="Tenant ID"),
        tenant_id_path: Optional[str] = Query(None, alias="tenant_id_path")
    ) -> User:
        permission_service = get_permission_service(db)
        
        # Determine tenant_id
        if tenant_from == "query" and tenant_id:
            target_tenant_id = tenant_id
        elif tenant_from == "path" and tenant_id_path:
            target_tenant_id = tenant_id_path
        elif tenant_from == "auto":
            target_tenant_id = tenant_id or tenant_id_path
        else:
            raise HTTPException(
                status_code=400,
                detail="Tenant ID is required for this operation"
            )
        
        if not target_tenant_id:
            raise HTTPException(
                status_code=400,
                detail="Tenant ID is required for this operation"
            )
        
        # Check if user is admin or owner
        if not permission_service.user_is_admin_or_owner(current_user.id, target_tenant_id):
            raise HTTPException(
                status_code=403,
                detail="Access denied: You must be an admin or owner to perform this action"
            )
        
        return current_user
    
    return check_admin_or_owner


# Dependency to get PermissionService
def get_permission_service_dep(db: Session = Depends(get_db)) -> PermissionService:
    """Dependency to get PermissionService instance."""
    return get_permission_service(db)
