"""
Permission service for checking user permissions within tenants.

This module provides utilities to check if users have specific permissions
within tenants by combining role-based and direct permissions.
"""
from typing import Set, Dict, List, Optional
from sqlalchemy.orm import Session

from .models import User, Tenant, UserTenantRole, UserTenantPermission, RolePermission
from .enum.erole import ERole
from .enum.epermission import EPermission


class PermissionService:
    """Service for checking and managing user permissions within tenants."""
    
    def __init__(self, db: Session):
        self.db = db
        self._role_permissions_cache: Optional[Dict[ERole, Set[EPermission]]] = None
    
    def _get_role_permissions_cache(self) -> Dict[ERole, Set[EPermission]]:
        """Get cached role permissions or load them from database."""
        if self._role_permissions_cache is None:
            self._role_permissions_cache = {}
            role_perms = self.db.query(RolePermission).all()
            
            for role_perm in role_perms:
                if role_perm.role not in self._role_permissions_cache:
                    self._role_permissions_cache[role_perm.role] = set()
                self._role_permissions_cache[role_perm.role].add(role_perm.permission)
        
        return self._role_permissions_cache
    
    def get_user_role_in_tenant(self, user_id: str, tenant_id: str) -> Optional[ERole]:
        """Get the user's role within a specific tenant."""
        user_role = self.db.query(UserTenantRole).filter(
            UserTenantRole.user_id == user_id,
            UserTenantRole.tenant_id == tenant_id
        ).first()
        
        return user_role.role if user_role else None
    
    def get_role_permissions(self, role: ERole) -> Set[EPermission]:
        """Get all permissions that a role has by default."""
        cache = self._get_role_permissions_cache()
        return cache.get(role, set())
    
    def get_user_direct_permissions(self, user_id: str, tenant_id: str) -> Set[EPermission]:
        """Get permissions directly assigned to a user within a tenant."""
        user_permissions = self.db.query(UserTenantPermission).filter(
            UserTenantPermission.user_id == user_id,
            UserTenantPermission.tenant_id == tenant_id
        ).all()
        
        return {up.permission for up in user_permissions}
    
    def get_user_effective_permissions(self, user_id: str, tenant_id: str) -> Set[EPermission]:
        """Get all effective permissions for a user within a tenant (role + direct permissions)."""
        permissions = set()
        
        # Get permissions from role
        user_role = self.get_user_role_in_tenant(user_id, tenant_id)
        if user_role:
            permissions.update(self.get_role_permissions(user_role))
        
        # Get direct permissions
        permissions.update(self.get_user_direct_permissions(user_id, tenant_id))
        
        return permissions
    
    def user_has_permission(self, user_id: str, tenant_id: str, permission: EPermission) -> bool:
        """Check if a user has a specific permission within a tenant."""
        effective_permissions = self.get_user_effective_permissions(user_id, tenant_id)
        return permission in effective_permissions
    
    def user_has_role(self, user_id: str, tenant_id: str, role: ERole) -> bool:
        """Check if a user has a specific role within a tenant."""
        user_role = self.get_user_role_in_tenant(user_id, tenant_id)
        return user_role == role
    
    def user_is_owner(self, user_id: str, tenant_id: str) -> bool:
        """Check if a user is an owner of a tenant."""
        return self.user_has_role(user_id, tenant_id, ERole.OWNER)
    
    def user_is_admin_or_owner(self, user_id: str, tenant_id: str) -> bool:
        """Check if a user is an admin or owner of a tenant."""
        user_role = self.get_user_role_in_tenant(user_id, tenant_id)
        return user_role in [ERole.ADMIN, ERole.OWNER]
    
    def user_can_access_tenant(self, user_id: str, tenant_id: str) -> bool:
        """Check if a user has any access to a tenant."""
        return self.get_user_role_in_tenant(user_id, tenant_id) is not None
    
    def get_user_accessible_tenants(self, user_id: str) -> List[str]:
        """Get all tenant IDs that a user has access to."""
        user_roles = self.db.query(UserTenantRole).filter(
            UserTenantRole.user_id == user_id
        ).all()
        
        return [ur.tenant_id for ur in user_roles]

    def get_tenant_id_for_resource(self, resource_id: str) -> Optional[str]:
        """Find the tenant_id for a given resource ID by checking all resource tables."""
        from .models import Person, Record, Task, Calendar, Tag

        resource_tables = [Person, Record, Task, Calendar, Tag]

        for table in resource_tables:
            resource = self.db.query(table).filter(table.id == resource_id).first()
            if resource and hasattr(resource, 'tenant_id'):
                return resource.tenant_id
        
        return None
    
    def assign_user_role(self, user_id: str, tenant_id: str, role: ERole) -> UserTenantRole:
        """Assign a role to a user within a tenant."""
        # Check if role assignment already exists
        existing_role = self.db.query(UserTenantRole).filter(
            UserTenantRole.user_id == user_id,
            UserTenantRole.tenant_id == tenant_id
        ).first()
        
        if existing_role:
            existing_role.role = role
            self.db.commit()
            return existing_role
        else:
            new_role = UserTenantRole(
                user_id=user_id,
                tenant_id=tenant_id,
                role=role
            )
            self.db.add(new_role)
            self.db.commit()
            return new_role
    
    def assign_user_permission(self, user_id: str, tenant_id: str, permission: EPermission) -> UserTenantPermission:
        """Assign a direct permission to a user within a tenant."""
        # Check if permission already exists
        existing_permission = self.db.query(UserTenantPermission).filter(
            UserTenantPermission.user_id == user_id,
            UserTenantPermission.tenant_id == tenant_id,
            UserTenantPermission.permission == permission
        ).first()
        
        if not existing_permission:
            new_permission = UserTenantPermission(
                user_id=user_id,
                tenant_id=tenant_id,
                permission=permission
            )
            self.db.add(new_permission)
            self.db.commit()
            return new_permission
        
        return existing_permission
    
    def remove_user_permission(self, user_id: str, tenant_id: str, permission: EPermission) -> bool:
        """Remove a direct permission from a user within a tenant."""
        permission_record = self.db.query(UserTenantPermission).filter(
            UserTenantPermission.user_id == user_id,
            UserTenantPermission.tenant_id == tenant_id,
            UserTenantPermission.permission == permission
        ).first()
        
        if permission_record:
            self.db.delete(permission_record)
            self.db.commit()
            return True
        
        return False
    
    def remove_user_from_tenant(self, user_id: str, tenant_id: str) -> bool:
        """Remove a user completely from a tenant (role and all permissions)."""
        # Remove role
        role_record = self.db.query(UserTenantRole).filter(
            UserTenantRole.user_id == user_id,
            UserTenantRole.tenant_id == tenant_id
        ).first()
        
        if role_record:
            self.db.delete(role_record)
        
        # Remove all permissions
        permission_records = self.db.query(UserTenantPermission).filter(
            UserTenantPermission.user_id == user_id,
            UserTenantPermission.tenant_id == tenant_id
        ).all()
        
        for permission_record in permission_records:
            self.db.delete(permission_record)
        
        self.db.commit()
        return role_record is not None


def get_permission_service(db: Session) -> PermissionService:
    """Get a PermissionService instance."""
    return PermissionService(db)
