"""
API endpoints for person management.

This module contains routes for creating, reading, updating, and deleting persons.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Person, User
from ..security import get_current_user
from ..schemas.pagination import PaginatedResponse
from ..schemas.person import PersonResponse, PersonCreate, PersonUpdate
from ..validation import validate_name, sanitize_input

router = APIRouter()


@router.get("/persons", response_model=PaginatedResponse[PersonResponse], tags=["persons"])
async def get_persons(
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Number of items per page"),
    tenant_id: str = Query(description="ID of the tenant to filter persons by"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve all persons from a specific tenant with pagination."""
    # Verify current user has access to the requested tenant
    user_tenant_ids = [t.id for t in current_user.tenants]
    if tenant_id not in user_tenant_ids:
        from ..exceptions import TenantAccessError
        raise TenantAccessError(tenant_id, user_tenant_ids)

    offset = (page - 1) * page_size
    
    # Query persons only from the specified tenant
    persons_query = db.query(Person).filter(Person.tenant_id == tenant_id)
    total_count = persons_query.count()
    persons = persons_query.offset(offset).limit(page_size).all()
    
    total_pages = (total_count + page_size - 1) // page_size
    return PaginatedResponse(
        data=persons,
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


@router.post("/persons", response_model=PersonResponse, tags=["persons"], status_code=201)
async def create_person(
    person_data: PersonCreate,
    tenant_id: str = Query(description="ID of the tenant to create the person in"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new person within a specific tenant."""
    from ..exceptions import TenantAccessError
    user_tenant_ids = {t.id for t in current_user.tenants}
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, list(user_tenant_ids))

    new_person = Person(
        **person_data.model_dump(),
        tenant_id=tenant_id
    )
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person


@router.get("/persons/{person_id}", response_model=PersonResponse, tags=["persons"])
async def get_person(
    person_id: str = Path(description="ID of the person to retrieve"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve a single person by their ID."""
    # Get all tenant IDs the user has access to
    user_tenant_ids = [t.id for t in current_user.tenants]
    
    # Query person from user's accessible tenants
    person = db.query(Person).filter(
        Person.id == person_id,
        Person.tenant_id.in_(user_tenant_ids)
    ).first()
    
    if not person:
        raise HTTPException(status_code=404, detail=f"Person with ID {person_id} not found or access denied")
    return person


@router.put("/persons/{person_id}", response_model=PersonResponse, tags=["persons"])
async def update_person(
    person_data: PersonUpdate,
    person_id: str = Path(description="ID of the person to update"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a person's details."""
    # Get all tenant IDs the user has access to
    user_tenant_ids = [t.id for t in current_user.tenants]
    
    # Find person in user's accessible tenants
    person = db.query(Person).filter(
        Person.id == person_id,
        Person.tenant_id.in_(user_tenant_ids)
    ).first()
    
    if not person:
        raise HTTPException(status_code=404, detail=f"Person with ID {person_id} not found or access denied")

    update_data = person_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(person, key, value)
    
    db.commit()
    db.refresh(person)
    return person


@router.delete("/persons/{person_id}", response_model=PersonResponse, tags=["persons"])
async def delete_person(
    person_id: str = Path(description="ID of the person to delete"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a person by their ID."""
    # Get all tenant IDs the user has access to
    user_tenant_ids = [t.id for t in current_user.tenants]
    
    # Find person in user's accessible tenants
    person = db.query(Person).filter(
        Person.id == person_id,
        Person.tenant_id.in_(user_tenant_ids)
    ).first()
    
    if not person:
        raise HTTPException(status_code=404, detail=f"Person with ID {person_id} not found or access denied")

    db.delete(person)
    db.commit()
    return person
