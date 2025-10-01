"""
API endpoints for tenant management.

This module contains routes for creating, reading, updating, and deleting tenants.
"""
from typing import List
from fastapi import APIRouter, HTTPException
from ..database import Tenant, tenant_list
from ..util import get_timestamp

router = APIRouter()


@router.get(
    "/tenant",
    response_model=List[Tenant],
    tags=["tenants"],
    summary="Lists all current existing tenants"
)
async def get_tenants(limit: int = 100, offset: int = 0):
    """Retrieve a list of tenants with optional pagination."""
    return tenant_list[offset:offset + limit]


@router.get(
    "/tenant/{tenant_id}",
    response_model=Tenant,
    tags=["tenants"],
    summary="Shows a specific tenant"
)
async def get_tenant(tenant_id: str):
    """
    Retrieve a single tenant by its ID.

    - **tenant_id** - The tenant ID to retrieve from the database
    """
    for tenant in tenant_list:
        if tenant.id == tenant_id:
            return tenant
    raise HTTPException(status_code=404, detail="Tenant not found")


@router.post(
    "/tenant",
    response_model=Tenant,
    tags=["tenants"],
    summary="Create a new tenant",
    response_description="The newly created tenant object."
)
async def create_tenant(tenant_name: str, tenant_description: str = None):
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
async def update_tenant(tenant_id: str, tenant_name: str, tenant_description: str, tenant_status: int):
    """Update an existing tenant's information."""
    for index, tenant in enumerate(tenant_list):
        if tenant.id == tenant_id:
            tenant.name = tenant_name
            tenant.description = tenant_description
            tenant.status = tenant_status
            tenant.updatedAt = get_timestamp()
            tenant_list[index] = tenant
            return tenant
    raise HTTPException(status_code=404, detail="Tenant not found")


@router.delete(
    "/tenant/{tenant_id}",
    status_code=204,
    tags=["tenants"],
    summary="Deletes a tenant by its ID"
)
async def delete_tenant(tenant_id: str):
    """Deletes a tenant by its ID."""
    for index, tenant in enumerate(tenant_list):
        if tenant.id == tenant_id:
            tenant_list.pop(index)
            return tenant
    raise HTTPException(status_code=404, detail="Tenant not found")
