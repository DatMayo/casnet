"""
API endpoints for user management.

This module contains routes for creating, reading, updating, and deleting user accounts.
"""
import uuid
from typing import List
from fastapi import APIRouter, HTTPException
from ..database import UserAccount, user_list
from ..model.tenant import Tenant
from ..util import get_timestamp

router = APIRouter()


@router.get("/user", response_model=List[UserAccount], tags=["users"])
async def get_users(limit: int = 100, offset: int = 0):
    """Retrieve a list of users with optional pagination."""
    return user_list[offset:offset + limit]


@router.post("/user", response_model=UserAccount, tags=["users"], status_code=201)
async def create_user(user_name: str, user_tenant: List[Tenant]):
    """Create a new user account."""
    if any(user.name == user_name for user in user_list):
        raise HTTPException(status_code=400, detail="A user with that name already exists")

    user = UserAccount(
        id=str(uuid.uuid4()),
        name=user_name,
        tenant=user_tenant,
    )
    user_list.append(user)
    return user


@router.get("/user/{user_id}", response_model=UserAccount, tags=["users"])
async def get_user(user_id: str):
    """Retrieve a single user by their ID."""
    for user in user_list:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@router.put("/user/{user_id}", response_model=UserAccount, tags=["users"])
async def update_user(user_id: str, user_name: str, user_tenant: List[Tenant]):
    """Update an existing user's name and tenant associations."""
    for index, user in enumerate(user_list):
        if user.id == user_id:
            user.name = user_name
            user.tenant = user_tenant
            user_list[index] = user
            return user
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/user/{user_id}", response_model=UserAccount, tags=["users"])
async def delete_user(user_id: str):
    """Delete a user by their ID and return the deleted user."""
    for index, user in enumerate(user_list):
        if user.id == user_id:
            return user_list.pop(index)
    raise HTTPException(status_code=404, detail="User not found")
