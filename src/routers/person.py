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
from ..schemas.person import PersonCreate, PersonUpdate, PersonResponse
from ..validation import validate_name, sanitize_input

router = APIRouter()


@router.get("/person/{tenant_id}", response_model=PaginatedResponse[PersonResponse], tags=["persons"])
async def get_persons(
    tenant_id: str = Path(description="ID of the tenant to retrieve persons from"), 
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a paginated list of persons for a specific tenant.
    """
    from ..exceptions import TenantAccessError
    user_tenant_ids = {t.id for t in current_user.tenants}
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, list(user_tenant_ids))

    persons_query = db.query(Person).filter(Person.tenant_id == tenant_id)
    
    total_count = persons_query.count()
    
    offset = (page - 1) * page_size
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


@router.post("/person/{tenant_id}", response_model=PersonResponse, tags=["persons"], status_code=201)
async def create_person(
    person_data: PersonCreate,
    tenant_id: str = Path(description="ID of the tenant to create the person in"),
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


@router.get("/person/{tenant_id}/{person_id}", response_model=PersonResponse, tags=["persons"])
async def get_person(
    tenant_id: str = Path(description="ID of the tenant that owns the person"),
    person_id: str = Path(description="ID of the person to retrieve"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve a single person by their ID."""
    from ..exceptions import TenantAccessError
    user_tenant_ids = {t.id for t in current_user.tenants}
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, list(user_tenant_ids))

    person = db.query(Person).filter(Person.id == person_id, Person.tenant_id == tenant_id).first()
    if not person:
        raise HTTPException(status_code=404, detail=f"Person with ID {person_id} not found in this tenant")
    return person


@router.put("/person/{tenant_id}/{person_id}", response_model=PersonResponse, tags=["persons"])
async def update_person(
    person_data: PersonUpdate,
    tenant_id: str = Path(description="ID of the tenant that owns the person"),
    person_id: str = Path(description="ID of the person to update"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a person's details."""
    from ..exceptions import TenantAccessError
    user_tenant_ids = {t.id for t in current_user.tenants}
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, list(user_tenant_ids))

    person = db.query(Person).filter(Person.id == person_id, Person.tenant_id == tenant_id).first()
    if not person:
        raise HTTPException(status_code=404, detail=f"Person with ID {person_id} not found in this tenant")

    update_data = person_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(person, key, value)
    
    db.commit()
    db.refresh(person)
    return person


@router.delete("/person/{tenant_id}/{person_id}", response_model=PersonResponse, tags=["persons"])
async def delete_person(
    tenant_id: str = Path(description="ID of the tenant that owns the person"),
    person_id: str = Path(description="ID of the person to delete"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a person by their ID."""
    from ..exceptions import TenantAccessError
    user_tenant_ids = {t.id for t in current_user.tenants}
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, list(user_tenant_ids))

    person = db.query(Person).filter(Person.id == person_id, Person.tenant_id == tenant_id).first()
    if not person:
        raise HTTPException(status_code=404, detail=f"Person with ID {person_id} not found in this tenant")

    db.delete(person)
    db.commit()
    return person
