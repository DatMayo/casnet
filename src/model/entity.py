"""
Defines the base Pydantic model for a generic Entity.

This model provides common fields that other models can inherit from.
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
