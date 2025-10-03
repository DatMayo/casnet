"""
API endpoints for calendar management.

This module contains routes for creating, reading, updating, and deleting calendar events.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from ..database import calendar_list, Calendar
from ..util import get_timestamp, find_item_by_id, validate_user_tenant_access
from ..security import get_current_user
from ..model.user import UserAccount

router = APIRouter()


@router.get("/calendar/{tenant_id}", response_model=List[Calendar], tags=["calendar"])
async def get_calendars(tenant_id: str, limit: int = 100, offset: int = 0, current_user: UserAccount = Depends(get_current_user)):
    """Retrieve a list of calendar events with optional pagination."""
    validate_user_tenant_access(tenant_id, current_user)
    return [c for c in calendar_list if c.tenant and c.tenant.id == tenant_id][offset:offset + limit]


@router.post("/calendar/{tenant_id}", response_model=Calendar, tags=["calendar"], status_code=201)
async def create_calendar(tenant_id: str, calendar: Calendar, current_user: UserAccount = Depends(get_current_user)):
    """Create a new calendar event."""
    tenant = validate_user_tenant_access(tenant_id, current_user)
    if any(c.id == calendar.id for c in calendar_list):
        raise HTTPException(status_code=400, detail="A calendar event with that ID already exists")

    calendar.tenant = tenant
    calendar_list.append(calendar)
    return calendar


@router.get("/calendar/{tenant_id}/{calendar_id}", response_model=Calendar, tags=["calendar"])
async def get_calendar(tenant_id: str, calendar_id: str, current_user: UserAccount = Depends(get_current_user)):
    """Retrieve a single calendar event by its ID."""
    validate_user_tenant_access(tenant_id, current_user)
    return find_item_by_id(calendar_id, calendar_list, "Calendar", tenant_id)


@router.put("/calendar/{tenant_id}/{calendar_id}", response_model=Calendar, tags=["calendar"])
async def update_calendar(tenant_id: str, calendar_id: str, title: str, description: str, current_user: UserAccount = Depends(get_current_user)):
    """Update a calendar event's details."""
    validate_user_tenant_access(tenant_id, current_user)
    calendar = find_item_by_id(calendar_id, calendar_list, "Calendar", tenant_id)
    calendar.title = title
    calendar.description = description
    calendar.updatedAt = get_timestamp()
    return calendar


@router.delete("/calendar/{tenant_id}/{calendar_id}", response_model=Calendar, tags=["calendar"])
async def delete_calendar(tenant_id: str, calendar_id: str, current_user: UserAccount = Depends(get_current_user)):
    """Delete a calendar event by its ID and return the deleted object."""
    validate_user_tenant_access(tenant_id, current_user)
    calendar = find_item_by_id(calendar_id, calendar_list, "Calendar", tenant_id)
    calendar_list.remove(calendar)
    return calendar
