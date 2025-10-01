"""
Defines the EStatus enum for representing entity statuses.
"""
from enum import Enum


class EStatus(Enum):
    """Represents the status of an entity."""
    Inactive = 0
    Active = 1
    Disabled = 2