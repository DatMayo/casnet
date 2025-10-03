"""
Utility functions for the application.

This module contains common helper functions, such as timestamp generation,
that are used across the application.
"""
import datetime
from typing import List, TypeVar, Optional
from fastapi import HTTPException

T = TypeVar('T')


def get_timestamp():
    """Returns the current timestamp in milliseconds."""
    now = datetime.datetime.now()
    return int(now.timestamp() * 1000)


def find_tenant_by_id(tenant_id: str):
    """Find a tenant by its ID or raise a 404 error."""
    from src.database import tenant_list
    for tenant in tenant_list:
        if tenant.id == tenant_id:
            return tenant
    raise HTTPException(status_code=404, detail="Tenant not found")


def validate_user_tenant_access(tenant_id: str, current_user):
    """Validate that the current user has access to the specified tenant."""
    # First check if tenant exists
    tenant = find_tenant_by_id(tenant_id)
    
    # Check if user is assigned to this tenant
    user_tenant_ids = [t.id for t in current_user.tenant] if current_user.tenant else []
    if tenant_id not in user_tenant_ids:
        raise HTTPException(
            status_code=403, 
            detail="Access denied: You are not assigned to this tenant"
        )
    
    return tenant


def find_item_by_id(item_id: str, item_list: List[T], item_name: str, tenant_id: Optional[str] = None) -> T:
    """Find an item in a list by its ID and optional tenant ID, or raise a 404 error."""
    for item in item_list:
        if item.id == item_id:
            if tenant_id is None or (hasattr(item, 'tenant') and item.tenant and item.tenant.id == tenant_id):
                return item
    raise HTTPException(status_code=404, detail=f"{item_name} not found")
