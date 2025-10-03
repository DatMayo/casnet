"""
Defines the Pydantic model for a Record, representing a record or case file
in the system with associated tags and processing information.
"""
from typing import List

from src.model.entity import Entity
from src.model.person import Person
from src.model.tag import Tag


class Record(Entity):
    """Represents a record or case file in the system."""
    title: str
    description: str
    created_by: Person
    processed_by: Person
    tags: List[Tag]
    additional_processors: List[Person]
