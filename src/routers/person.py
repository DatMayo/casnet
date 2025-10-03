"""
API endpoints for person management.

This module contains routes for creating, reading, updating, and deleting persons.
"""
import uuid
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from ..database import person_list, Person
from ..util import get_timestamp, find_item_by_id, find_tenant_by_id, validate_user_tenant_access
from ..security import get_current_user
from ..model.user import UserAccount

router = APIRouter()


@router.get("/person/{tenant_id}", response_model=List[Person], tags=["persons"])
async def get_persons(tenant_id: str, limit: int = 100, offset: int = 0, current_user: UserAccount = Depends(get_current_user)):
    """Retrieve a list of persons with optional pagination."""
    validate_user_tenant_access(tenant_id, current_user)
    return [p for p in person_list if p.tenant and p.tenant.id == tenant_id][offset:offset + limit]


@router.post("/person/{tenant_id}", response_model=Person, tags=["persons"], status_code=201)
async def create_person(tenant_id: str, person: Person, current_user: UserAccount = Depends(get_current_user)):
    """Create a new person."""
    tenant = validate_user_tenant_access(tenant_id, current_user)
    if any(p.id == person.id for p in person_list):
        raise HTTPException(status_code=400, detail="A person with that ID already exists")

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
