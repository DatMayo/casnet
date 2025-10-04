"""
API endpoints for record management.

This module contains routes for creating, reading, updating, and deleting records.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Record, User
from ..security import get_current_user
from ..schemas.pagination import PaginatedResponse
from ..schemas.record import RecordCreate, RecordUpdate, RecordResponse

router = APIRouter()


@router.get("/records", response_model=PaginatedResponse[RecordResponse], tags=["records"])
async def get_records(
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve all records accessible to the current user with pagination."""
    # Get all tenant IDs the user has access to
    user_tenant_ids = [t.id for t in current_user.tenants]
    
    if not user_tenant_ids:
        return PaginatedResponse(
            items=[],
            page=page,
            page_size=page_size,
            total_count=0,
            total_pages=0
        )

    offset = (page - 1) * page_size
    
    # Query records from all user's tenants
    records_query = db.query(Record).filter(Record.tenant_id.in_(user_tenant_ids))
    total_count = records_query.count()
    records = records_query.offset(offset).limit(page_size).all()
    
    return PaginatedResponse(
        items=records,
        page=page,
        page_size=page_size,
        total_count=total_count,
        total_pages=(total_count + page_size - 1) // page_size
    )


@router.post("/records", response_model=RecordResponse, tags=["records"], status_code=201)
async def create_record(
    record_data: RecordCreate,
    tenant_id: str = Query(description="ID of the tenant to create the record in"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new record within a specific tenant."""
    from ..exceptions import TenantAccessError
    user_tenant_ids = {t.id for t in current_user.tenants}
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, list(user_tenant_ids))

    new_record = Record(
        **record_data.model_dump(),
        tenant_id=tenant_id
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


@router.get("/records/{record_id}", response_model=RecordResponse, tags=["records"])
async def get_record(
    record_id: str = Path(description="ID of the record to retrieve"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve a single record by its ID."""
    # Get all tenant IDs the user has access to
    user_tenant_ids = [t.id for t in current_user.tenants]
    
    # Query record from user's accessible tenants
    record = db.query(Record).filter(
        Record.id == record_id,
        Record.tenant_id.in_(user_tenant_ids)
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail=f"Record with ID {record_id} not found or access denied")
    return record


@router.put("/records/{record_id}", response_model=RecordResponse, tags=["records"])
async def update_record(
    record_data: RecordUpdate,
    record_id: str = Path(description="ID of the record to update"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a record's details."""
    # Get all tenant IDs the user has access to
    user_tenant_ids = [t.id for t in current_user.tenants]
    
    # Find record in user's accessible tenants
    record = db.query(Record).filter(
        Record.id == record_id,
        Record.tenant_id.in_(user_tenant_ids)
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail=f"Record with ID {record_id} not found or access denied")

    update_data = record_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(record, key, value)
    
    db.commit()
    db.refresh(record)
    return record


@router.delete("/records/{record_id}", response_model=RecordResponse, tags=["records"])
async def delete_record(
    record_id: str = Path(description="ID of the record to delete"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a record by its ID."""
    # Get all tenant IDs the user has access to
    user_tenant_ids = [t.id for t in current_user.tenants]
    
    # Find record in user's accessible tenants
    record = db.query(Record).filter(
        Record.id == record_id,
        Record.tenant_id.in_(user_tenant_ids)
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail=f"Record with ID {record_id} not found or access denied")

    db.delete(record)
    db.commit()
    return record
