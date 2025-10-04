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
from ..security import get_current_user
from ..hashing import get_password_hash
from ..schemas.pagination import PaginatedResponse
from ..schemas.user import UserCreate, UserUpdate, UserResponse
from ..validation import validate_name, sanitize_input

router = APIRouter()


@router.get("/users", response_model=PaginatedResponse[UserResponse], tags=["users"])
async def get_users(
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a paginated list of users that share tenants with the current user.
    """
    user_tenant_ids = {t.id for t in current_user.tenants}
    
    if not user_tenant_ids:
        return PaginatedResponse(data=[], meta={
            "total_items": 0, "total_pages": 0, "current_page": page, "page_size": page_size, 
            "has_next": False, "has_previous": False, "next_page": None, "previous_page": None
        })
    
    shared_users_query = db.query(User).join(User.tenants).filter(Tenant.id.in_(user_tenant_ids)).distinct()
    
    total_count = shared_users_query.count()
    
    offset = (page - 1) * page_size
    users = shared_users_query.offset(offset).limit(page_size).all()
    
    total_pages = (total_count + page_size - 1) // page_size
    return PaginatedResponse(
        data=users,
        meta={
            "total_items": total_count,
            "total_pages": total_pages,
            "current_page": page,
            "page_size": page_size,
            "has_next": page < total_pages,
            "has_previous": page > 1,
            "next_page": page + 1 if page < total_pages else None,
            "previous_page": page - 1 if page > 1 else None
        }
    )


@router.post("/users", response_model=UserResponse, tags=["users"], status_code=201)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Create a new user account. This is an open endpoint and does not require authentication."""
    from ..exceptions import DuplicateResourceError
    
    validated_name = validate_name(sanitize_input(user_data.name), "user_name")
    
    existing_user = db.query(User).filter(User.name == validated_name).first()
    if existing_user:
        raise DuplicateResourceError("User", validated_name)

    new_user = User(
        name=validated_name,
        hashed_password=get_password_hash(sanitize_input(user_data.password))
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.get("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def get_user(
    user_id: str = Path(description="ID of the user to retrieve"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve a single user by their ID (only if they share a tenant with current user)."""
    from ..exceptions import AuthorizationError

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    current_user_tenant_ids = {t.id for t in current_user.tenants}
    target_user_tenant_ids = {t.id for t in user.tenants}
    
    if not current_user_tenant_ids.intersection(target_user_tenant_ids):
        raise AuthorizationError("Access denied: User does not share any tenants with you")
    
    return user


@router.put("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def update_user(
    user_data: UserUpdate,
    user_id: str = Path(description="ID of the user to update"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing user's name and password (only if they share a tenant)."""
    from ..exceptions import AuthorizationError, DuplicateResourceError

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    current_user_tenant_ids = {t.id for t in current_user.tenants}
    target_user_tenant_ids = {t.id for t in user.tenants}

    if not current_user_tenant_ids.intersection(target_user_tenant_ids):
        raise AuthorizationError("Access denied: User does not share any tenants with you")
    
    update_data = user_data.model_dump(exclude_unset=True)
    
    if 'name' in update_data:
        validated_name = validate_name(sanitize_input(update_data['name']), "user_name")
        existing_user = db.query(User).filter(User.name == validated_name, User.id != user_id).first()
        if existing_user:
            raise DuplicateResourceError("User", validated_name)
        user.name = validated_name

    if 'password' in update_data:
        user.hashed_password = get_password_hash(sanitize_input(update_data['password']))
    
    db.commit()
    db.refresh(user)
    
    return user


@router.delete("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def delete_user(
    user_id: str = Path(description="ID of the user to delete"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a user by their ID (only if they share a tenant with current user)."""
    from ..exceptions import AuthorizationError

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    current_user_tenant_ids = {t.id for t in current_user.tenants}
    target_user_tenant_ids = {t.id for t in user.tenants}

    if not current_user_tenant_ids.intersection(target_user_tenant_ids):
        raise AuthorizationError("Access denied: User does not share any tenants with you")
    
    db.delete(user)
    db.commit()
    
    return user
