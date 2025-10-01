"""
API endpoints for user management.

This module contains routes for creating and reading user accounts.
"""
import uuid
from typing import List
from fastapi import APIRouter, HTTPException
from ..database import UserAccount, user_list
from ..model.tenant import Tenant

router = APIRouter()


@router.get("/user", response_model=List[UserAccount], tags=["users"])
async def get_users(limit: int = 100, offset: int = 0):
    """Retrieve a list of users with optional pagination."""
    return user_list[offset:offset + limit]


@router.post("/user", response_model=UserAccount, tags=["users"])
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
