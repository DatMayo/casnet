"""
API endpoints for person management.

This module contains routes for creating, reading, updating, and deleting persons.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from ..database import person_list, Person
from ..util import get_timestamp, find_item_by_id, validate_user_tenant_access
from ..security import get_current_user
from ..model.user import UserAccount
from ..model.pagination import PaginatedResponse, paginate_data

router = APIRouter()


@router.get("/person/{tenant_id}", response_model=PaginatedResponse[Person], tags=["persons"])
async def get_persons(
    tenant_id: str, 
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Number of items per page"),
    current_user: UserAccount = Depends(get_current_user)
):
    """
    Retrieve a paginated list of persons for a specific tenant.
    
    Returns paginated person data with metadata including total count,
    page information, and navigation links.
    """
    validate_user_tenant_access(tenant_id, current_user)
    
    # Filter persons by tenant
    tenant_persons = [p for p in person_list if p.tenant and p.tenant.id == tenant_id]
    
    # Paginate the data
    paginated_persons, pagination_meta = paginate_data(tenant_persons, page, page_size)
    
    return PaginatedResponse(
        data=paginated_persons,
        meta=pagination_meta
    )


@router.post("/person/{tenant_id}", response_model=Person, tags=["persons"], status_code=201)
async def create_person(tenant_id: str, person: Person, current_user: UserAccount = Depends(get_current_user)):
    """Create a new person."""
    from ..exceptions import DuplicateResourceError
    
    tenant = validate_user_tenant_access(tenant_id, current_user)
    if any(p.id == person.id for p in person_list):
        raise DuplicateResourceError("Person", person.id)

    person.tenant = tenant
    person_list.append(person)
    return person


@router.get("/person/{tenant_id}/{person_id}", response_model=Person, tags=["persons"])
async def get_person(tenant_id: str, person_id: str, current_user: UserAccount = Depends(get_current_user)):
    """Retrieve a single person by their ID."""
    validate_user_tenant_access(tenant_id, current_user)
    return find_item_by_id(person_id, person_list, "Person", tenant_id)


@router.put("/person/{tenant_id}/{person_id}", response_model=Person, tags=["persons"])
async def update_person(tenant_id: str, person_id: str, first_name: str, last_name: str, current_user: UserAccount = Depends(get_current_user)):
    """Update a person's details."""
    validate_user_tenant_access(tenant_id, current_user)
    person = find_item_by_id(person_id, person_list, "Person", tenant_id)
    person.first_name = first_name
    person.last_name = last_name
    person.updatedAt = get_timestamp()
    return person


@router.delete("/person/{tenant_id}/{person_id}", response_model=Person, tags=["persons"])
async def delete_person(tenant_id: str, person_id: str, current_user: UserAccount = Depends(get_current_user)):
    """Delete a person by their ID and return the deleted object."""
    validate_user_tenant_access(tenant_id, current_user)
    person = find_item_by_id(person_id, person_list, "Person", tenant_id)
    person_list.remove(person)
    return person
