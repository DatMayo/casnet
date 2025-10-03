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
    """Retrieve a list of users that share tenants with the current user."""
    user_tenant_ids = [t.id for t in current_user.tenant] if current_user.tenant else []
    # Find users that share at least one tenant with current user
    shared_users = []
    for user in user_list:
        if user.tenant:
            user_has_shared_tenant = any(t.id in user_tenant_ids for t in user.tenant)
            if user_has_shared_tenant:
                shared_users.append(user)
    return shared_users[offset:offset + limit]


@router.post("/user", response_model=UserAccount, tags=["users"], status_code=201)
async def create_user(user_name: str, password: str, user_tenant: List[Tenant], current_user: UserAccount = Depends(get_current_user)):
    """Create a new user account."""
    from ..exceptions import DuplicateResourceError
    
    if any(user.name == user_name for user in user_list):
        raise DuplicateResourceError("User", user_name)

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
    """Retrieve a single user by their ID (only if they share a tenant with current user)."""
    user = find_item_by_id(user_id, user_list, "User")
    
    # Check if the requested user shares any tenant with current user
    from ..exceptions import AuthorizationError
    
    current_user_tenant_ids = [t.id for t in current_user.tenant] if current_user.tenant else []
    target_user_tenant_ids = [t.id for t in user.tenant] if user.tenant else []
    
    has_shared_tenant = any(tid in current_user_tenant_ids for tid in target_user_tenant_ids)
    if not has_shared_tenant:
        raise AuthorizationError("Access denied: User does not share any tenants with you")
    
    return user


@router.put("/user/{user_id}", response_model=UserAccount, tags=["users"])
async def update_user(user_id: str, user_name: str, user_tenant: List[Tenant], password: str = None, current_user: UserAccount = Depends(get_current_user)):
    """Update an existing user's name and tenant associations (only if they share a tenant)."""
    user = find_item_by_id(user_id, user_list, "User")
    
    # Check if the target user shares any tenant with current user
    from ..exceptions import AuthorizationError
    
    current_user_tenant_ids = [t.id for t in current_user.tenant] if current_user.tenant else []
    target_user_tenant_ids = [t.id for t in user.tenant] if user.tenant else []
    
    has_shared_tenant = any(tid in current_user_tenant_ids for tid in target_user_tenant_ids)
    if not has_shared_tenant:
        raise AuthorizationError("Access denied: User does not share any tenants with you")
    
    user.name = user_name
    user.tenant = user_tenant
    if password:
        user.hashed_password = get_password_hash(password)
    user.updatedAt = get_timestamp()
    return user


@router.delete("/user/{user_id}", response_model=UserAccount, tags=["users"])
async def delete_user(user_id: str, current_user: UserAccount = Depends(get_current_user)):
    """Delete a user by their ID (only if they share a tenant with current user)."""
    user = find_item_by_id(user_id, user_list, "User")
    
    # Check if the target user shares any tenant with current user
    from ..exceptions import AuthorizationError
    
    current_user_tenant_ids = [t.id for t in current_user.tenant] if current_user.tenant else []
    target_user_tenant_ids = [t.id for t in user.tenant] if user.tenant else []
    
    has_shared_tenant = any(tid in current_user_tenant_ids for tid in target_user_tenant_ids)
    if not has_shared_tenant:
        raise AuthorizationError("Access denied: User does not share any tenants with you")
    
    user_list.remove(user)
    return user
