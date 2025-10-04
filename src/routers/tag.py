"""
API endpoints for tag management.

This module contains routes for creating, reading, updating, and deleting tags.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Tag, User
from ..dependencies import get_permission_checker, requires_permission_for_resource
from ..enum.epermission import EPermission
from ..schemas.pagination import PaginatedResponse
from ..schemas.tag import TagCreate, TagUpdate, TagResponse

router = APIRouter()


@router.get("/tags", response_model=PaginatedResponse[TagResponse], tags=["tags"])
async def get_tags(
    tenant_id: str = Query(..., description="ID of the tenant to retrieve tags from"),
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_permission_checker(EPermission.VIEW_TAGS))
):
    """Retrieve tags from a specific tenant with pagination."""
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


@router.post("/tags", response_model=TagResponse, tags=["tags"], status_code=201)
async def create_tag(
    tag_data: TagCreate,
    tenant_id: str = Query(..., description="ID of the tenant to create the tag in"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_permission_checker(EPermission.CREATE_TAGS))
):
    """Create a new tag within a specific tenant."""
    new_tag = Tag(**tag_data.model_dump(), tenant_id=tenant_id)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag


@router.get("/tags/{tag_id}", response_model=TagResponse, tags=["tags"])
async def get_tag(
    tag_id: str = Path(..., alias="resource_id", description="ID of the tag to retrieve"),
    db: Session = Depends(get_db),
    current_user: User = Depends(requires_permission_for_resource(EPermission.VIEW_TAGS))
):
    """Retrieve a single tag by its ID."""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail=f"Tag with ID {tag_id} not found")
    return tag


@router.put("/tags/{tag_id}", response_model=TagResponse, tags=["tags"])
async def update_tag(
    tag_data: TagUpdate,
    tag_id: str = Path(..., alias="resource_id", description="ID of the tag to update"),
    db: Session = Depends(get_db),
    current_user: User = Depends(requires_permission_for_resource(EPermission.EDIT_TAGS))
):
    """Update a tag's details."""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail=f"Tag with ID {tag_id} not found")

    update_data = tag_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tag, key, value)
    
    db.commit()
    db.refresh(tag)
    return tag


@router.delete("/tags/{tag_id}", response_model=TagResponse, tags=["tags"])
async def delete_tag(
    tag_id: str = Path(..., alias="resource_id", description="ID of the tag to delete"),
    db: Session = Depends(get_db),
    current_user: User = Depends(requires_permission_for_resource(EPermission.DELETE_TAGS))
):
    """Delete a tag by its ID."""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail=f"Tag with ID {tag_id} not found")

    db.delete(tag)
    db.commit()
    return tag
