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
from ..schemas.pagination import PaginatedResponse
from ..schemas.tag import TagCreate, TagUpdate, TagResponse

router = APIRouter()


@router.get("/tag/{tenant_id}", response_model=PaginatedResponse[TagResponse], tags=["tags"])
async def get_tags(
    tenant_id: str = Path(description="ID of the tenant to retrieve tags from"),
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Number of tags per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve a paginated list of tags for a specific tenant."""
    from ..exceptions import TenantAccessError
    user_tenant_ids = {t.id for t in current_user.tenants}
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, list(user_tenant_ids))

    tags_query = db.query(Tag).filter(Tag.tenant_id == tenant_id)
    
    total_count = tags_query.count()
    
    offset = (page - 1) * page_size
    tags = tags_query.offset(offset).limit(page_size).all()
    
    total_pages = (total_count + page_size - 1) // page_size
    return PaginatedResponse(
        data=tags,
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


@router.post("/tag/{tenant_id}", response_model=TagResponse, tags=["tags"], status_code=201)
async def create_tag(
    tag_data: TagCreate,
    tenant_id: str = Path(description="ID of the tenant to create the tag in"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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


@router.get("/tag/{tenant_id}/{tag_id}", response_model=TagResponse, tags=["tags"])
async def get_tag(
    tenant_id: str = Path(description="ID of the tenant that owns the tag"),
    tag_id: str = Path(description="ID of the tag to retrieve"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve a single tag by its ID."""
    from ..exceptions import TenantAccessError
    user_tenant_ids = {t.id for t in current_user.tenants}
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, list(user_tenant_ids))

    tag = db.query(Tag).filter(Tag.id == tag_id, Tag.tenant_id == tenant_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail=f"Tag with ID {tag_id} not found in this tenant")
    return tag


@router.put("/tag/{tenant_id}/{tag_id}", response_model=TagResponse, tags=["tags"])
async def update_tag(
    tag_data: TagUpdate,
    tenant_id: str = Path(description="ID of the tenant that owns the tag"),
    tag_id: str = Path(description="ID of the tag to update"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a tag's details."""
    from ..exceptions import TenantAccessError
    user_tenant_ids = {t.id for t in current_user.tenants}
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, list(user_tenant_ids))

    tag = db.query(Tag).filter(Tag.id == tag_id, Tag.tenant_id == tenant_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail=f"Tag with ID {tag_id} not found in this tenant")

    update_data = tag_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tag, key, value)
    
    db.commit()
    db.refresh(tag)
    return tag


@router.delete("/tag/{tenant_id}/{tag_id}", response_model=TagResponse, tags=["tags"])
async def delete_tag(
    tenant_id: str = Path(description="ID of the tenant that owns the tag"),
    tag_id: str = Path(description="ID of the tag to delete"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a tag by its ID."""
    from ..exceptions import TenantAccessError
    user_tenant_ids = {t.id for t in current_user.tenants}
    if tenant_id not in user_tenant_ids:
        raise TenantAccessError(tenant_id, list(user_tenant_ids))

    tag = db.query(Tag).filter(Tag.id == tag_id, Tag.tenant_id == tenant_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail=f"Tag with ID {tag_id} not found in this tenant")

    db.delete(tag)
    db.commit()
    return tag
