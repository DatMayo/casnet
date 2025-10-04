"""
Defines the ERole enum for representing user roles within tenants.
"""
from enum import Enum


class ERole(Enum):
    """Represents the role of a user within a tenant."""
    USER = "user"        # Basic user with limited permissions
    ADMIN = "admin"      # Administrator with management permissions
    OWNER = "owner"      # Owner with full control over the tenant
