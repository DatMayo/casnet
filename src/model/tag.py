"""
Defines the Pydantic model for a Tag, representing a label or category
that can be associated with records and other entities.
"""
from src.model.entity import Entity
from src.model.person import Person


class Tag(Entity):
    """Represents a tag or label in the system."""
    name: str
    color: str
    created_by: Person
