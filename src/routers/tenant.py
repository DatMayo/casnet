"""
API endpoints for tenant management.

This module contains routes for creating, reading, updating, and deleting tenants.
"""
import uuid
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Tenant, User
from ..security import get_current_user
from ..schemas.pagination import PaginatedResponse
from ..schemas.tenant import TenantCreate, TenantUpdate, TenantResponse
from ..validation import validate_name, sanitize_input

router = APIRouter()


@router.get(
    "/tenant",
    response_model=PaginatedResponse[TenantResponse],
    tags=["tenants"],
    summary="Lists all tenants assigned to the current user"
)
async def get_tenants(
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a paginated list of tenants the current user is assigned to.
    """
    user_tenants_query = db.query(Tenant).join(Tenant.users).filter(User.id == current_user.id)
    
    total_count = user_tenants_query.count()
    
    offset = (page - 1) * page_size
    tenants = user_tenants_query.offset(offset).limit(page_size).all()
    
    total_pages = (total_count + page_size - 1) // page_size
    return PaginatedResponse(
        data=tenants,
        meta={
            "total_items": total_count,
            "total_pages": total_pages,
            "current_page": page,
            "page_size": page_size,
            "has_next": page < total_pages,
            "has_previous": page > 1,
            "next_page": page + 1 if page < total_pages else None,
            "previous_page": page - 1 if page > 1 else None
        }
    )


@router.get(
    "/tenant/{tenant_id}",
    response_model=TenantResponse,
    tags=["tenants"],
    summary="Shows a specific tenant"
)
async def get_tenant(
    tenant_id: str = Path(description="ID of the tenant to retrieve"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a single tenant by its ID (only if user is assigned to it).
    """
    from ..exceptions import TenantAccessError
    user_tenant_ids = {t.id for t in current_user.tenants}
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, list(user_tenant_ids))

    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail=f"Tenant with ID {tenant_id} not found")
    return tenant


@router.post(
    "/tenant",
    response_model=TenantResponse,
    tags=["tenants"],
    status_code=201,
    summary="Create a new tenant and assign it to the current user",
)
async def create_tenant(
    tenant_data: TenantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Creates a new tenant and automatically assigns the current user to it.
    """
    from ..exceptions import DuplicateResourceError
    validated_name = validate_name(sanitize_input(tenant_data.name), "tenant_name")

    existing_tenant = db.query(Tenant).filter(Tenant.name == validated_name).first()
    if existing_tenant:
        raise DuplicateResourceError("Tenant", validated_name)

    new_tenant = Tenant(
        name=validated_name,
        description=sanitize_input(tenant_data.description) if tenant_data.description else None
    )
    
    # Add the current user to the new tenant's user list
    new_tenant.users.append(current_user)
    
    db.add(new_tenant)
    db.commit()
    db.refresh(new_tenant)
    return new_tenant


@router.put(
    "/tenant/{tenant_id}",
    response_model=TenantResponse,
    tags=["tenants"],
    summary="Update an existing tenant's information",
)
async def update_tenant(
    tenant_data: TenantUpdate,
    tenant_id: str = Path(description="ID of the tenant to update"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing tenant's information (only if user is assigned to it)."""
    from ..exceptions import TenantAccessError, DuplicateResourceError
    user_tenant_ids = {t.id for t in current_user.tenants}
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, list(user_tenant_ids))

    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail=f"Tenant with ID {tenant_id} not found")

    if tenant_data.name:
        validated_name = validate_name(sanitize_input(tenant_data.name), "tenant_name")
        existing_tenant = db.query(Tenant).filter(Tenant.name == validated_name, Tenant.id != tenant_id).first()
        if existing_tenant:
            raise DuplicateResourceError("Tenant", validated_name)
        tenant.name = validated_name

    if tenant_data.description is not None:
        tenant.description = sanitize_input(tenant_data.description)
        
    if tenant_data.status is not None:
        tenant.status = tenant_data.status.value  # Convert enum to integer

    db.commit()
    db.refresh(tenant)
    return tenant


@router.delete(
    "/tenant/{tenant_id}",
    response_model=TenantResponse,
    tags=["tenants"],
    summary="Deletes a tenant by its ID"
)
async def delete_tenant(
    tenant_id: str = Path(description="ID of the tenant to delete"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deletes a tenant by its ID (only if user is assigned to it)."""
    from ..exceptions import TenantAccessError
    user_tenant_ids = {t.id for t in current_user.tenants}
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, list(user_tenant_ids))

    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail=f"Tenant with ID {tenant_id} not found")

    db.delete(tenant)
    db.commit()
    return tenant
