"""
Utility functions for the application.

This module contains common helper functions, such as timestamp generation,
that are used across the application.
"""
import datetime
from typing import List, TypeVar, Optional

T = TypeVar('T')


def get_timestamp():
    """Returns the current timestamp in milliseconds."""
    now = datetime.datetime.now()
    return int(now.timestamp() * 1000)


def find_tenant_by_id(tenant_id: str):
    """Find a tenant by its ID or raise a structured error."""
    from src.database import tenant_list
    from src.exceptions import TenantNotFoundError
    
    for tenant in tenant_list:
        if tenant.id == tenant_id:
            return tenant
    raise TenantNotFoundError(tenant_id)


def validate_user_tenant_access(tenant_id: str, current_user):
    """Validate that the current user has access to the specified tenant."""
    from src.exceptions import TenantAccessError
    
    # First check if tenant exists
    tenant = find_tenant_by_id(tenant_id)
    
    # Check if user is assigned to this tenant
    user_tenant_ids = [t.id for t in current_user.tenant] if current_user.tenant else []
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, user_tenant_ids)
    
    return tenant


def find_item_by_id(item_id: str, item_list: List[T], item_name: str, tenant_id: Optional[str] = None) -> T:
    """Find an item in a list by its ID and optional tenant ID, or raise a structured error."""
    from src.exceptions import ResourceNotFoundError
    
    for item in item_list:
        if item.id == item_id:
            if tenant_id is None or (hasattr(item, 'tenant') and item.tenant and item.tenant.id == tenant_id):
                return item
    raise ResourceNotFoundError(item_name, item_id)
