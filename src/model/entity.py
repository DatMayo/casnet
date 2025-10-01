"""
Defines the base Pydantic model for all data entities.

This model provides common fields that other data models inherit from, such as ID,
tenant, status, and timestamps.
"""
from src.enum.estatus import EStatus
from src.model.tenant import Tenant
from pydantic import BaseModel, Field

from src.util import get_timestamp


class Entity(BaseModel):
    """Represents a base entity with common fields like ID, tenant, and timestamps."""
    id: str
    tenant: Tenant
    status: EStatus = EStatus.Active
    createdAt: int = Field(default_factory=get_timestamp)
    updatedAt: int = Field(default_factory=get_timestamp)
