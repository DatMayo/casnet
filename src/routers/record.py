"""
API endpoints for record management.

This module contains routes for creating, reading, updating, and deleting records.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Record, User
from ..dependencies import get_permission_checker, requires_permission_for_resource
from ..enum.epermission import EPermission
from ..schemas.pagination import PaginatedResponse
from ..schemas.record import RecordCreate, RecordUpdate, RecordResponse

router = APIRouter()


@router.get("/records", response_model=PaginatedResponse[RecordResponse], tags=["records"])
async def get_records(
    tenant_id: str = Query(..., description="ID of the tenant to retrieve records from"),
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_permission_checker(EPermission.VIEW_RECORDS))
):
    """Retrieve records from a specific tenant with pagination."""
    records_query = db.query(Record).filter(Record.tenant_id == tenant_id)
    total_count = records_query.count()
    offset = (page - 1) * page_size
    records = records_query.offset(offset).limit(page_size).all()
    total_pages = (total_count + page_size - 1) // page_size
    return PaginatedResponse(
        data=records,
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


@router.post("/records", response_model=RecordResponse, tags=["records"], status_code=201)
async def create_record(
    record_data: RecordCreate,
    tenant_id: str = Query(..., description="ID of the tenant to create the record in"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_permission_checker(EPermission.CREATE_RECORDS))
):
    """Create a new record within a specific tenant."""
    new_record = Record(**record_data.model_dump(), tenant_id=tenant_id)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


@router.get("/records/{record_id}", response_model=RecordResponse, tags=["records"])
async def get_record(
    record_id: str = Path(..., alias="resource_id", description="ID of the record to retrieve"),
    db: Session = Depends(get_db),
    current_user: User = Depends(requires_permission_for_resource(EPermission.VIEW_RECORDS))
):
    """Retrieve a single record by its ID."""
    record = db.query(Record).filter(Record.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"Record with ID {record_id} not found")
    return record


@router.put("/records/{record_id}", response_model=RecordResponse, tags=["records"])
async def update_record(
    record_data: RecordUpdate,
    record_id: str = Path(..., alias="resource_id", description="ID of the record to update"),
    db: Session = Depends(get_db),
    current_user: User = Depends(requires_permission_for_resource(EPermission.EDIT_RECORDS))
):
    """Update a record's details."""
    record = db.query(Record).filter(Record.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"Record with ID {record_id} not found")

    update_data = record_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(record, key, value)
    
    db.commit()
    db.refresh(record)
    return record


@router.delete("/records/{record_id}", response_model=RecordResponse, tags=["records"])
async def delete_record(
    record_id: str = Path(..., alias="resource_id", description="ID of the record to delete"),
    db: Session = Depends(get_db),
    current_user: User = Depends(requires_permission_for_resource(EPermission.DELETE_RECORDS))
):
    """Delete a record by its ID."""
    record = db.query(Record).filter(Record.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"Record with ID {record_id} not found")

    db.delete(record)
    db.commit()
    return record
