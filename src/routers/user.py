"""
API endpoints for user management.

This module contains routes for creating, reading, updating, and deleting user accounts.
"""
import uuid
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from ..database import UserAccount, user_list
from ..model.tenant import Tenant
from ..util import get_timestamp, find_item_by_id
from ..security import get_current_user, get_password_hash

router = APIRouter()


@router.get("/user", response_model=List[UserAccount], tags=["users"])
async def get_users(limit: int = 100, offset: int = 0, current_user: UserAccount = Depends(get_current_user)):
    """Retrieve a list of users with optional pagination."""
    return user_list[offset:offset + limit]


@router.post("/user", response_model=UserAccount, tags=["users"], status_code=201)
async def create_user(user_name: str, password: str, user_tenant: List[Tenant], current_user: UserAccount = Depends(get_current_user)):
    """Create a new user account."""
    if any(user.name == user_name for user in user_list):
        raise HTTPException(status_code=400, detail="A user with that name already exists")

    user = UserAccount(
        id=str(uuid.uuid4()),
        name=user_name,
        hashed_password=get_password_hash(password),
        tenant=user_tenant,
    )
    user_list.append(user)
    return user


@router.get("/user/{user_id}", response_model=UserAccount, tags=["users"])
async def get_user(user_id: str, current_user: UserAccount = Depends(get_current_user)):
    """Retrieve a single user by their ID."""
    return find_item_by_id(user_id, user_list, "User")


@router.put("/user/{user_id}", response_model=UserAccount, tags=["users"])
async def update_user(user_id: str, user_name: str, user_tenant: List[Tenant], password: str = None, current_user: UserAccount = Depends(get_current_user)):
    """Update an existing user's name and tenant associations."""
    user = find_item_by_id(user_id, user_list, "User")
    user.name = user_name
    user.tenant = user_tenant
    if password:
        user.hashed_password = get_password_hash(password)
    user.updatedAt = get_timestamp()
    return user


@router.delete("/user/{user_id}", response_model=UserAccount, tags=["users"])
async def delete_user(user_id: str, current_user: UserAccount = Depends(get_current_user)):
    """Delete a user by their ID and return the deleted user."""
    user = find_item_by_id(user_id, user_list, "User")
    user_list.remove(user)
    return user
