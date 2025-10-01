"""
Defines the Pydantic model for a Task, representing a unit of work or an
assignment within the system.
"""
from src.model.entity import Entity
from src.model.person import Person


class Task(Entity):
    """Represents a task assigned to a person."""
    title: str
    created_from: Person
    created_for: Person
