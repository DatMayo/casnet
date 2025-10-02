"""
API endpoints for record management.

This module contains routes for creating, reading, updating, and deleting records.
"""
import uuid
from typing import List
from fastapi import APIRouter, HTTPException
from ..database import record_list, Record
from ..util import get_timestamp, find_item_by_id, find_tenant_by_id

router = APIRouter()


@router.get("/record/{tenant_id}", response_model=List[Record], tags=["records"])
async def get_records(tenant_id: str, limit: int = 100, offset: int = 0):
    """Retrieve a list of records with optional pagination."""
    find_tenant_by_id(tenant_id)
    return [r for r in record_list if r.tenant and r.tenant.id == tenant_id][offset:offset + limit]


@router.post("/record/{tenant_id}", response_model=Record, tags=["records"], status_code=201)
async def create_record(tenant_id: str, record: Record):
    """Create a new record."""
    tenant = find_tenant_by_id(tenant_id)
    if any(r.id == record.id for r in record_list):
        raise HTTPException(status_code=400, detail="A record with that ID already exists")

    record.tenant = tenant
    record_list.append(record)
    return record


@router.get("/record/{tenant_id}/{record_id}", response_model=Record, tags=["records"])
async def get_record(tenant_id: str, record_id: str):
    """Retrieve a single record by its ID."""
    return find_item_by_id(record_id, record_list, "Record", tenant_id)


@router.put("/record/{tenant_id}/{record_id}", response_model=Record, tags=["records"])
async def update_record(tenant_id: str, record_id: str, title: str, description: str):
    """Update a record's details."""
    record = find_item_by_id(record_id, record_list, "Record", tenant_id)
    record.title = title
    record.description = description
    record.updatedAt = get_timestamp()
    return record


@router.delete("/record/{tenant_id}/{record_id}", response_model=Record, tags=["records"])
async def delete_record(tenant_id: str, record_id: str):
    """Delete a record by its ID and return the deleted object."""
    record = find_item_by_id(record_id, record_list, "Record", tenant_id)
    record_list.remove(record)
    return record
