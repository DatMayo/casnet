"""
API endpoints for tenant management.

This module contains routes for creating, reading, updating, and deleting tenants.
"""
import uuid
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from ..database import Tenant, tenant_list
from ..util import get_timestamp, find_tenant_by_id
from ..security import get_current_user
from ..model.user import UserAccount
from ..model.pagination import PaginatedResponse, paginate_data

router = APIRouter()


@router.get(
    "/tenant",
    response_model=PaginatedResponse[Tenant],
    tags=["tenants"],
    summary="Lists all tenants assigned to the current user"
)
async def get_tenants(
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Number of items per page"),
    current_user: UserAccount = Depends(get_current_user)
):
    """
    Retrieve a paginated list of tenants the current user is assigned to.
    
    Returns only tenants where the user has access, with pagination metadata
    for building frontend pagination controls.
    """
    user_tenant_ids = [t.id for t in current_user.tenant] if current_user.tenant else []
    user_tenants = [t for t in tenant_list if t.id in user_tenant_ids]
    
    # Paginate the user's tenants
    paginated_tenants, pagination_meta = paginate_data(user_tenants, page, page_size)
    
    return PaginatedResponse(
        data=paginated_tenants,
        meta=pagination_meta
    )


@router.get(
    "/tenant/{tenant_id}",
    response_model=Tenant,
    tags=["tenants"],
    summary="Shows a specific tenant"
)
async def get_tenant(tenant_id: str, current_user: UserAccount = Depends(get_current_user)):
    """
    Retrieve a single tenant by its ID (only if user is assigned to it).

    - **tenant_id** - The tenant ID to retrieve from the database
    """
    # Validate user has access to this tenant
    from ..exceptions import TenantAccessError
    
    user_tenant_ids = [t.id for t in current_user.tenant] if current_user.tenant else []
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, user_tenant_ids)
    return find_tenant_by_id(tenant_id)


@router.post(
    "/tenant",
    response_model=Tenant,
    tags=["tenants"],
    status_code=201,
    summary="Create a new tenant",
    response_description="The newly created tenant object."
)
async def create_tenant(tenant_name: str, tenant_description: str = None, current_user: UserAccount = Depends(get_current_user)):
    """
    Creates a new tenant in the system.

    This endpoint allows you to create a new tenant by providing a name and an optional description.
    A unique ID and timestamps will be generated automatically upon creation.

    - **tenant_name**: The name of the tenant (required).
    - **tenant_description**: An optional text describing the tenant.
    """
    tenant = Tenant(
        id=str(uuid.uuid4()),
        name=tenant_name,
        description=tenant_description
    )
    tenant_list.append(tenant)
    return tenant


@router.put(
    "/tenant/{tenant_id}",
    response_model=Tenant,
    tags=["tenants"],
    summary="Update an existing tenant's information",
    response_description="The updated tenant object"
)
async def update_tenant(tenant_id: str, tenant_name: str, tenant_description: str, tenant_status: int, current_user: UserAccount = Depends(get_current_user)):
    """Update an existing tenant's information (only if user is assigned to it)."""
    # Validate user has access to this tenant
    from ..exceptions import TenantAccessError
    
    user_tenant_ids = [t.id for t in current_user.tenant] if current_user.tenant else []
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, user_tenant_ids)
    tenant = find_tenant_by_id(tenant_id)
    tenant.name = tenant_name
    tenant.description = tenant_description
    tenant.status = tenant_status
    tenant.updatedAt = get_timestamp()
    return tenant


@router.delete(
    "/tenant/{tenant_id}",
    response_model=Tenant,
    tags=["tenants"],
    summary="Deletes a tenant by its ID"
)
async def delete_tenant(tenant_id: str, current_user: UserAccount = Depends(get_current_user)):
    """Deletes a tenant by its ID (only if user is assigned to it)."""
    # Validate user has access to this tenant
    from ..exceptions import TenantAccessError
    
    user_tenant_ids = [t.id for t in current_user.tenant] if current_user.tenant else []
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, user_tenant_ids)
    tenant = find_tenant_by_id(tenant_id)
    tenant_list.remove(tenant)
    return tenant
