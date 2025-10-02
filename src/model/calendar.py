"""
Defines the Pydantic model for a Calendar event.
"""
from src.model.entity import Entity
from src.model.person import Person
from src.model.tenant import Tenant


class Calendar(Entity):
    """Represents a calendar event, such as a meeting or appointment."""
    title: str
    description: str = None
    created_from: Person
    date_start: int
    date_end: int = 0
    tenant: Tenant = None
