"""
API endpoints for record management.

This module contains routes for creating, reading, updating, and deleting records.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from ..database import record_list, Record
from ..util import get_timestamp, find_item_by_id, validate_user_tenant_access
from ..security import get_current_user
from ..model.user import UserAccount
from ..model.pagination import PaginatedResponse, paginate_data

router = APIRouter()


@router.get("/record/{tenant_id}", response_model=PaginatedResponse[Record], tags=["records"])
async def get_records(
    tenant_id: str,
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Number of records per page"),
    current_user: UserAccount = Depends(get_current_user)
):
    """Retrieve a paginated list of records for a specific tenant."""
    validate_user_tenant_access(tenant_id, current_user)
    
    # Filter records by tenant
    tenant_records = [r for r in record_list if r.tenant and r.tenant.id == tenant_id]
    
    # Paginate the data
    paginated_records, pagination_meta = paginate_data(tenant_records, page, page_size)
    
    return PaginatedResponse(
        data=paginated_records,
        meta=pagination_meta
    )


@router.post("/record/{tenant_id}", response_model=Record, tags=["records"], status_code=201)
async def create_record(tenant_id: str, record: Record, current_user: UserAccount = Depends(get_current_user)):
    """Create a new record."""
    tenant = validate_user_tenant_access(tenant_id, current_user)
    if any(r.id == record.id for r in record_list):
        raise HTTPException(status_code=400, detail="A record with that ID already exists")

    record.tenant = tenant
    record_list.append(record)
    return record


@router.get("/record/{tenant_id}/{record_id}", response_model=Record, tags=["records"])
async def get_record(tenant_id: str, record_id: str, current_user: UserAccount = Depends(get_current_user)):
    """Retrieve a single record by its ID."""
    validate_user_tenant_access(tenant_id, current_user)
    return find_item_by_id(record_id, record_list, "Record", tenant_id)


@router.put("/record/{tenant_id}/{record_id}", response_model=Record, tags=["records"])
async def update_record(
    tenant_id: str,
    record_id: str,
    title: str = Query(description="Updated title for the record"),
    description: str = Query(description="Updated description for the record"),
    current_user: UserAccount = Depends(get_current_user)
):
    """Update a record's details."""
    validate_user_tenant_access(tenant_id, current_user)
    record = find_item_by_id(record_id, record_list, "Record", tenant_id)
    record.title = title
    record.description = description
    record.updatedAt = get_timestamp()
    return record


@router.delete("/record/{tenant_id}/{record_id}", response_model=Record, tags=["records"])
async def delete_record(tenant_id: str, record_id: str, current_user: UserAccount = Depends(get_current_user)):
    """Delete a record by its ID and return the deleted object."""
    validate_user_tenant_access(tenant_id, current_user)
    record = find_item_by_id(record_id, record_list, "Record", tenant_id)
    record_list.remove(record)
    return record
