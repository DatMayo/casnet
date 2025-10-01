"""
API endpoints for person management.

This module contains routes for creating, reading, updating, and deleting persons.
"""
import uuid
from typing import List
from fastapi import APIRouter, HTTPException
from ..database import person_list, Person
from ..util import get_timestamp, find_item_by_id

router = APIRouter()


@router.get("/person", response_model=List[Person], tags=["persons"])
async def get_persons(limit: int = 100, offset: int = 0):
    """Retrieve a list of persons with optional pagination."""
    return person_list[offset:offset + limit]


@router.post("/person", response_model=Person, tags=["persons"], status_code=201)
async def create_person(person: Person):
    """Create a new person."""
    if any(p.id == person.id for p in person_list):
        raise HTTPException(status_code=400, detail="A person with that ID already exists")

    person_list.append(person)
    return person


@router.get("/person/{person_id}", response_model=Person, tags=["persons"])
async def get_person(person_id: str):
    """Retrieve a single person by their ID."""
    return find_item_by_id(person_id, person_list, "Person")


@router.put("/person/{person_id}", response_model=Person, tags=["persons"])
async def update_person(person_id: str, first_name: str, last_name: str):
    """Update a person's details."""
    person = find_item_by_id(person_id, person_list, "Person")
    person.first_name = first_name
    person.last_name = last_name
    person.updatedAt = get_timestamp()
    return person


@router.delete("/person/{person_id}", response_model=Person, tags=["persons"])
async def delete_person(person_id: str):
    """Delete a person by their ID and return the deleted object."""
    person = find_item_by_id(person_id, person_list, "Person")
    person_list.remove(person)
    return person
