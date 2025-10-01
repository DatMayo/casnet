"""
In-memory database for the application.

This module contains lists of tenants and users that are used for demonstration purposes.
In a production environment, this would be replaced with a proper database connection.
"""
from typing import List

from src.enum.estatus import EStatus
from src.model.tenant import Tenant
from src.model.user import UserAccount


tenant_list: List[Tenant] = [
    Tenant(
        id="c0f6088b-0899-4a1a-8651-d15212eb8dcd",
        name="LSPD",
        description="Los Santos Police Department",
        status=EStatus.Active,
        createdAt=1759303664075,
        updatedAt=1759303664075
    ),
    Tenant(
        id="7cdb1a84-0199-490c-b198-b91e96cda147",
        name="SAFMS",
        description="San Andreas Medical Service",
        status=EStatus.Active,
        createdAt=1759304776289,
        updatedAt=1759304776289
    )
]

user_list: List[UserAccount] = [
    UserAccount(
        id="862dc359-4685-4d1b-b4b9-672f2d445833",
        name="Ignatius Stackley",
        tenant=[tenant_list[0]],
        createdAt=1759303664075,
        updatedAt=1759303664075
    ),
    UserAccount(
        id="7ca7a2d1-c0a8-454b-b17e-870d575dfbe7",
        name="Howard Clifton",
        createdAt=1759308060,
        updatedAt=1759308060
    )
]
