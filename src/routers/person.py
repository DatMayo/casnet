"""
API endpoints for person management.

This module contains routes for creating and reading persons.
"""
from typing import List
from fastapi import APIRouter, HTTPException
from ..database import person_list, Person
from ..util import get_timestamp

router = APIRouter()


@router.get("/person", response_model=List[Person], tags=["persons"])
async def get_persons(limit: int = 100, offset: int = 0):
    """Retrieve a list of persons with optional pagination."""
    return person_list[offset:offset + limit]


@router.post("/person", response_model=Person, tags=["persons"])
async def create_person(person: Person):
    """Create a new person."""
    if any(p.id == person.id for p in person_list):
        raise HTTPException(status_code=400, detail="A person with that ID already exists")

    person_list.append(person)
    return person


@router.get("/person/{person_id}", response_model=Person, tags=["persons"])
async def get_person(person_id: str):
    """Retrieve a single person by their ID."""
    for person in person_list:
        if person.id == person_id:
            return person
    raise HTTPException(status_code=404, detail="Person not found")


@router.put("/person/{person_id}", response_model=Person, tags=["persons"])
async def update_person(person_id: str, first_name: str, last_name: str):
    """Update a person's details."""
    for index, person in enumerate(person_list):
        if person.id == person_id:
            person.first_name = first_name
            person.last_name = last_name
            person.updatedAt = get_timestamp()
            person_list[index] = person
            return person
    raise HTTPException(status_code=404, detail="Person not found")


@router.delete("/person/{person_id}", status_code=204, tags=["persons"])
async def delete_person(person_id: str):
    """Delete a person by their ID."""
    for index, person in enumerate(person_list):
        if person.id == person_id:
            person_list.pop(index)
            return person
    raise HTTPException(status_code=404, detail="Person not found")
