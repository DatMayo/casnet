"""
API endpoints for tag management.

This module contains routes for creating, reading, updating, and deleting tags.
"""
import uuid
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from ..database import tag_list, Tag
from ..util import get_timestamp, find_item_by_id, find_tenant_by_id
from ..security import get_current_user
from ..model.user import UserAccount

router = APIRouter()


@router.get("/tag/{tenant_id}", response_model=List[Tag], tags=["tags"])
async def get_tags(tenant_id: str, limit: int = 100, offset: int = 0, current_user: UserAccount = Depends(get_current_user)):
    """Retrieve a list of tags with optional pagination."""
    find_tenant_by_id(tenant_id)
    return [t for t in tag_list if t.tenant and t.tenant.id == tenant_id][offset:offset + limit]


@router.post("/tag/{tenant_id}", response_model=Tag, tags=["tags"], status_code=201)
async def create_tag(tenant_id: str, tag: Tag, current_user: UserAccount = Depends(get_current_user)):
    """Create a new tag."""
    tenant = find_tenant_by_id(tenant_id)
    if any(t.id == tag.id for t in tag_list):
        raise HTTPException(status_code=400, detail="A tag with that ID already exists")

    tag.tenant = tenant
    tag_list.append(tag)
    return tag


@router.get("/tag/{tenant_id}/{tag_id}", response_model=Tag, tags=["tags"])
async def get_tag(tenant_id: str, tag_id: str, current_user: UserAccount = Depends(get_current_user)):
    """Retrieve a single tag by its ID."""
    return find_item_by_id(tag_id, tag_list, "Tag", tenant_id)


@router.put("/tag/{tenant_id}/{tag_id}", response_model=Tag, tags=["tags"])
async def update_tag(tenant_id: str, tag_id: str, name: str, color: str, current_user: UserAccount = Depends(get_current_user)):
    """Update a tag's details."""
    tag = find_item_by_id(tag_id, tag_list, "Tag", tenant_id)
    tag.name = name
    tag.color = color
    tag.updatedAt = get_timestamp()
    return tag


@router.delete("/tag/{tenant_id}/{tag_id}", response_model=Tag, tags=["tags"])
async def delete_tag(tenant_id: str, tag_id: str, current_user: UserAccount = Depends(get_current_user)):
    """Delete a tag by its ID and return the deleted object."""
    tag = find_item_by_id(tag_id, tag_list, "Tag", tenant_id)
    tag_list.remove(tag)
    return tag
