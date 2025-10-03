"""

This module contains routes for creating, reading, updating, and deleting user accounts.
"""
import uuid
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from ..database import user_list, UserAccount, Tenant
from ..util import get_timestamp, find_item_by_id
from ..security import get_current_user, get_password_hash
from ..model.pagination import PaginatedResponse, paginate_data
from ..validation import validate_name, sanitize_input

router = APIRouter()


@router.get("/user", response_model=PaginatedResponse[UserAccount], tags=["users"])
async def get_users(
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Number of items per page"),
    current_user: UserAccount = Depends(get_current_user)
):
    """
    Retrieve a paginated list of users that share tenants with the current user.
    
    Returns only users who share at least one tenant with the requesting user,
    with pagination metadata for building frontend pagination controls.
    """
    user_tenant_ids = [t.id for t in current_user.tenant] if current_user.tenant else []
    
    # Find users that share at least one tenant with current user
    shared_users = []
    for user in user_list:
        if user.tenant:
            user_has_shared_tenant = any(t.id in user_tenant_ids for t in user.tenant)
            if user_has_shared_tenant:
                shared_users.append(user)
    
    # Paginate the filtered users
    paginated_users, pagination_meta = paginate_data(shared_users, page, page_size)
    
    return PaginatedResponse(
        data=paginated_users,
        meta=pagination_meta
    )


@router.post("/user", response_model=UserAccount, tags=["users"], status_code=201)
async def create_user(
    user_tenant: List[Tenant],  # Complex types can't use Query()
    user_name: str = Query(description="Username for the new user account"),
    password: str = Query(description="Password for the new user account"),
    current_user: UserAccount = Depends(get_current_user)
):
    """Create a new user account with input validation."""
    from ..exceptions import DuplicateResourceError
    
    # Validate and sanitize input
    validated_name = validate_name(sanitize_input(user_name), "user_name")
    validated_password = sanitize_input(password)
    
    if any(user.name == validated_name for user in user_list):
        raise DuplicateResourceError("User", validated_name)

    user = UserAccount(
        id=str(uuid.uuid4()),
        name=validated_name,
        hashed_password=get_password_hash(validated_password),
        tenant=user_tenant,
    )
    user_list.append(user)
    return user


@router.get("/user/{user_id}", response_model=UserAccount, tags=["users"])
async def get_user(
    user_id: str = Path(description="ID of the user to retrieve"),
    current_user: UserAccount = Depends(get_current_user)
):
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
async def update_user(
    user_tenant: List[Tenant],  # Complex types can't use Query()
    user_id: str = Path(description="ID of the user to update"),
    user_name: str = Query(description="Updated username"),
    password: str = Query(default=None, description="Optional new password (leave empty to keep current password)"),
    current_user: UserAccount = Depends(get_current_user)
):
    """Update an existing user's name and tenant associations (only if they share a tenant)."""
    user = find_item_by_id(user_id, user_list, "User")
    
    # Check if the target user shares any tenant with current user
    from ..exceptions import AuthorizationError
    
    current_user_tenant_ids = [t.id for t in current_user.tenant] if current_user.tenant else []
    target_user_tenant_ids = [t.id for t in user.tenant] if user.tenant else []
    
    has_shared_tenant = any(tid in current_user_tenant_ids for tid in target_user_tenant_ids)
    if not has_shared_tenant:
        raise AuthorizationError("Access denied: User does not share any tenants with you")
    
    # Validate and sanitize input
    user.name = validate_name(sanitize_input(user_name), "user_name")
    user.tenant = user_tenant
    if password:
        validated_password = sanitize_input(password)
        user.hashed_password = get_password_hash(validated_password)
    user.updatedAt = get_timestamp()
    return user


@router.delete("/user/{user_id}", response_model=UserAccount, tags=["users"])
async def delete_user(
    user_id: str = Path(description="ID of the user to delete"),
    current_user: UserAccount = Depends(get_current_user)
):
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
