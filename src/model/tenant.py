"""
Defines the Pydantic model for a Tenant, which represents a distinct
customer or organization in a multi-tenant system.
"""
from src.enum.estatus import EStatus
from pydantic import BaseModel, Field

from src.util import get_timestamp


class Tenant(BaseModel):
    """Represents a tenant in the system."""
    id: str
    name: str
    description: str = None
    status: EStatus = EStatus.Active
    createdAt: int = Field(default_factory=get_timestamp)
    updatedAt: int = Field(default_factory=get_timestamp)
