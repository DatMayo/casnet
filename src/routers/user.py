"""
User router for creating, reading, updating, and deleting user accounts.

This module provides CRUD operations for user management with SQLAlchemy.
"""
import uuid
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..models import User, Tenant
from ..util import get_timestamp, find_item_by_id
from ..security import get_current_user, get_password_hash
from ..model.pagination import PaginatedResponse, paginate_data
from ..validation import validate_name, sanitize_input

router = APIRouter()


@router.get("/user", response_model=PaginatedResponse[dict], tags=["users"])
async def get_users(
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a paginated list of users that share tenants with the current user.
    
    Returns only users who share at least one tenant with the requesting user,
    with pagination metadata for building frontend pagination controls.
    """
    # Get current user's tenant IDs
    user_tenant_ids = [t.id for t in current_user.tenants] if current_user.tenants else []
    
    if not user_tenant_ids:
        # If user has no tenants, return empty result
        return PaginatedResponse(
            data=[],
            meta={"total_items": 0, "total_pages": 0, "current_page": page, "page_size": page_size, 
                  "has_next": False, "has_previous": False, "next_page": None, "previous_page": None}
        )
    
    # Query users that share at least one tenant with current user
    # Using subquery to find users with shared tenants
    shared_users_query = db.query(User).join(User.tenants).filter(
        Tenant.id.in_(user_tenant_ids)
    ).distinct()
    
    # Get total count for pagination
    total_count = shared_users_query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    users = shared_users_query.offset(offset).limit(page_size).all()
    
    # Convert to dict format for response (avoiding Pydantic model issues for now)
    user_data = []
    for user in users:
        user_dict = {
            "id": user.id,
            "name": user.name,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat(),
            "tenants": [{"id": t.id, "name": t.name} for t in user.tenants]
        }
        user_data.append(user_dict)
    
    # Calculate pagination metadata
    total_pages = (total_count + page_size - 1) // page_size
    pagination_meta = {
        "total_items": total_count,
        "total_pages": total_pages,
        "current_page": page,
        "page_size": page_size,
        "has_next": page < total_pages,
        "has_previous": page > 1,
        "next_page": page + 1 if page < total_pages else None,
        "previous_page": page - 1 if page > 1 else None
    }
    
    return PaginatedResponse(
        data=user_data,
        meta=pagination_meta
    )


@router.post("/user", response_model=dict, tags=["users"], status_code=201)
async def create_user(
    user_name: str = Query(description="Username for the new user account"),
    password: str = Query(description="Password for the new user account"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new user account with input validation."""
    from ..exceptions import DuplicateResourceError
    
    # Validate and sanitize input
    validated_name = validate_name(sanitize_input(user_name), "user_name")
    validated_password = sanitize_input(password)
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.name == validated_name).first()
    if existing_user:
        raise DuplicateResourceError("User", validated_name)

    # Create new user
    new_user = User(
        name=validated_name,
        hashed_password=get_password_hash(validated_password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Return user data
    return {
        "id": new_user.id,
        "name": new_user.name,
        "created_at": new_user.created_at.isoformat(),
        "updated_at": new_user.updated_at.isoformat(),
        "tenants": []  # New users start with no tenants
    }


@router.get("/user/{user_id}", response_model=dict, tags=["users"])
async def get_user(
    user_id: str = Path(description="ID of the user to retrieve"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve a single user by their ID (only if they share a tenant with current user)."""
    # Find the user by ID
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    # Check if the requested user shares any tenant with current user
    from ..exceptions import AuthorizationError
    
    current_user_tenant_ids = [t.id for t in current_user.tenants] if current_user.tenants else []
    target_user_tenant_ids = [t.id for t in user.tenants] if user.tenants else []
    
    has_shared_tenant = any(tid in current_user_tenant_ids for tid in target_user_tenant_ids)
    if not has_shared_tenant:
        raise AuthorizationError("Access denied: User does not share any tenants with you")
    
    return {
        "id": user.id,
        "name": user.name,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
        "tenants": [{"id": t.id, "name": t.name} for t in user.tenants]
    }


@router.put("/user/{user_id}", response_model=dict, tags=["users"])
async def update_user(
    user_id: str = Path(description="ID of the user to update"),
    user_name: str = Query(description="Updated username"),
    password: str = Query(default=None, description="Optional new password (leave empty to keep current password)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing user's name and password (only if they share a tenant)."""
    # Find the user by ID
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    # Check if the target user shares any tenant with current user
    from ..exceptions import AuthorizationError
    
    current_user_tenant_ids = [t.id for t in current_user.tenants] if current_user.tenants else []
    target_user_tenant_ids = [t.id for t in user.tenants] if user.tenants else []
    
    has_shared_tenant = any(tid in current_user_tenant_ids for tid in target_user_tenant_ids)
    if not has_shared_tenant:
        raise AuthorizationError("Access denied: User does not share any tenants with you")
    
    # Validate and sanitize input
    validated_name = validate_name(sanitize_input(user_name), "user_name")
    
    # Check if new name conflicts with existing user
    existing_user = db.query(User).filter(User.name == validated_name, User.id != user_id).first()
    if existing_user:
        from ..exceptions import DuplicateResourceError
        raise DuplicateResourceError("User", validated_name)
    
    # Update user fields
    user.name = validated_name
    if password:
        validated_password = sanitize_input(password)
        user.hashed_password = get_password_hash(validated_password)
    
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "name": user.name,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
        "tenants": [{"id": t.id, "name": t.name} for t in user.tenants]
    }


@router.delete("/user/{user_id}", response_model=dict, tags=["users"])
async def delete_user(
    user_id: str = Path(description="ID of the user to delete"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a user by their ID (only if they share a tenant with current user)."""
    # Find the user by ID
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    # Check if the target user shares any tenant with current user
    from ..exceptions import AuthorizationError
    
    current_user_tenant_ids = [t.id for t in current_user.tenants] if current_user.tenants else []
    target_user_tenant_ids = [t.id for t in user.tenants] if user.tenants else []
    
    has_shared_tenant = any(tid in current_user_tenant_ids for tid in target_user_tenant_ids)
    if not has_shared_tenant:
        raise AuthorizationError("Access denied: User does not share any tenants with you")
    
    # Store user data for response
    user_data = {
        "id": user.id,
        "name": user.name,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
        "tenants": [{"id": t.id, "name": t.name} for t in user.tenants]
    }
    
    # Delete the user (this will cascade delete related records due to our model setup)
    db.delete(user)
    db.commit()
    
    return user_data
