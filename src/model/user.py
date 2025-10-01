"""
Defines the Pydantic model for a UserAccount, representing a user's login credentials
and their association with one or more tenants.
"""
from src.enum.estatus import EStatus
from src.model.tenant import Tenant
from pydantic import BaseModel, Field
from typing import List

from src.util import get_timestamp


class UserAccount(BaseModel):
    """Represents a user account in the system."""
    id: str
    name: str
    status: EStatus = EStatus.Active
    tenant: List[Tenant] | None = None
    createdAt: int = Field(default_factory=get_timestamp)
    updatedAt: int = Field(default_factory=get_timestamp)
