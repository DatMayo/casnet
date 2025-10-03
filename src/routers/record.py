"""
API endpoints for record management.

This module contains routes for creating, reading, updating, and deleting records.
"""
import uuid
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from ..database import record_list, Record
from ..util import get_timestamp, find_item_by_id, find_tenant_by_id, validate_user_tenant_access
from ..security import get_current_user
from ..model.user import UserAccount

router = APIRouter()


@router.get("/record/{tenant_id}", response_model=List[Record], tags=["records"])
async def get_records(tenant_id: str, limit: int = 100, offset: int = 0, current_user: UserAccount = Depends(get_current_user)):
    """Retrieve a list of records with optional pagination."""
    validate_user_tenant_access(tenant_id, current_user)
    return [r for r in record_list if r.tenant and r.tenant.id == tenant_id][offset:offset + limit]


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
async def update_record(tenant_id: str, record_id: str, title: str, description: str, current_user: UserAccount = Depends(get_current_user)):
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
