"""
API endpoints for tag management.

This module contains routes for creating, reading, updating, and deleting tags.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Tag, User
from ..security import get_current_user
from ..dependencies import requires_permission
from ..enum.epermission import EPermission
from ..schemas.pagination import PaginatedResponse
from ..schemas.tag import TagCreate, TagUpdate, TagResponse

router = APIRouter()


@router.get("/tags", response_model=PaginatedResponse[TagResponse], tags=["tags"])
async def get_tags(
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Number of items per page"),
    tenant_id: str = Query(description="ID of the tenant to filter tags by"),
    db: Session = Depends(get_db),
    current_user: User = Depends(requires_permission(EPermission.VIEW_TAGS))
):
    """Retrieve all tags accessible to the current user with pagination."""
    # Get all tenant IDs the user has access to
    user_tenant_ids = [t.id for t in current_user.tenants]
    
    if not user_tenant_ids:
        return PaginatedResponse(
            items=[],
            page=page,
            page_size=page_size,
            total_count=0,
            total_pages=0
        )

    offset = (page - 1) * page_size
    
    # Query tags from all user's tenants
    tags_query = db.query(Tag).filter(Tag.tenant_id.in_(user_tenant_ids))
    total_count = tags_query.count()
    tags = tags_query.offset(offset).limit(page_size).all()
    
    return PaginatedResponse(
        items=tags,
        page=page,
        page_size=page_size,
        total_count=total_count,
        total_pages=(total_count + page_size - 1) // page_size
    )


@router.post("/tags", response_model=TagResponse, tags=["tags"], status_code=201)
async def create_tag(
    tag_data: TagCreate,
    tenant_id: str = Query(description="ID of the tenant to create the tag in"),
    db: Session = Depends(get_db),
    current_user: User = Depends(requires_permission(EPermission.CREATE_TAGS))
):
    """Create a new tag within a specific tenant."""
    from ..exceptions import TenantAccessError
    user_tenant_ids = {t.id for t in current_user.tenants}
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, list(user_tenant_ids))

    new_tag = Tag(
        **tag_data.model_dump(),
        tenant_id=tenant_id
    )
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag


@router.get("/tags/{tag_id}", response_model=TagResponse, tags=["tags"])
async def get_tag(
    tag_id: str = Path(description="ID of the tag to retrieve"),
    db: Session = Depends(get_db),
    current_user: User = Depends(requires_permission(EPermission.VIEW_TAGS, tenant_from="auto"))
):
    """Retrieve a single tag by its ID."""
    # Get all tenant IDs the user has access to
    user_tenant_ids = [t.id for t in current_user.tenants]
    
    # Query tag from user's accessible tenants
    tag = db.query(Tag).filter(
        Tag.id == tag_id,
        Tag.tenant_id.in_(user_tenant_ids)
    ).first()
    
    if not tag:
        raise HTTPException(status_code=404, detail=f"Tag with ID {tag_id} not found or access denied")
    return tag


@router.put("/tags/{tag_id}", response_model=TagResponse, tags=["tags"])
async def update_tag(
    tag_data: TagUpdate,
    tag_id: str = Path(description="ID of the tag to update"),
    db: Session = Depends(get_db),
    current_user: User = Depends(requires_permission(EPermission.EDIT_TAGS, tenant_from="auto"))
):
    """Update a tag's details."""
    # Get all tenant IDs the user has access to
    user_tenant_ids = [t.id for t in current_user.tenants]
    
    # Find tag in user's accessible tenants
    tag = db.query(Tag).filter(
        Tag.id == tag_id,
        Tag.tenant_id.in_(user_tenant_ids)
    ).first()
    
    if not tag:
        raise HTTPException(status_code=404, detail=f"Tag with ID {tag_id} not found or access denied")

    update_data = tag_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tag, key, value)
    
    db.commit()
    db.refresh(tag)
    return tag


@router.delete("/tags/{tag_id}", response_model=TagResponse, tags=["tags"])
async def delete_tag(
    tag_id: str = Path(description="ID of the tag to delete"),
    db: Session = Depends(get_db),
    current_user: User = Depends(requires_permission(EPermission.DELETE_TAGS, tenant_from="auto"))
):
    """Delete a tag by its ID."""
    # Get all tenant IDs the user has access to
    user_tenant_ids = [t.id for t in current_user.tenants]
    
    # Find tag in user's accessible tenants
    tag = db.query(Tag).filter(
        Tag.id == tag_id,
        Tag.tenant_id.in_(user_tenant_ids)
    ).first()
    
    if not tag:
        raise HTTPException(status_code=404, detail=f"Tag with ID {tag_id} not found or access denied")

    db.delete(tag)
    db.commit()
    return tag
