"""
Defines the Pydantic model for a Person, representing an individual's personal
information. This model can be linked to a UserAccount.
"""
from src.enum.egender import EGender
from src.model.entity import Entity
from src.model.user import UserAccount


class Person(Entity):
    """Represents a person, inheriting from the base Entity model."""
    first_name: str
    last_name: str
    birth_date: int = None
    alias: str = None
    gender: EGender = EGender.Unknown
    email: str = None
    phone: str = None
    notes: str = None
    user: UserAccount = None
