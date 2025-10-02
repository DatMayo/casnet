"""
API endpoints for calendar management.

This module contains routes for creating, reading, updating, and deleting calendar events.
"""
import uuid
from typing import List
from fastapi import APIRouter, HTTPException
from ..database import calendar_list, Calendar
from ..util import get_timestamp, find_item_by_id, find_tenant_by_id

router = APIRouter()


@router.get("/calendar/{tenant_id}", response_model=List[Calendar], tags=["calendar"])
async def get_calendars(tenant_id: str, limit: int = 100, offset: int = 0):
    """Retrieve a list of calendar events with optional pagination."""
    find_tenant_by_id(tenant_id)
    return [c for c in calendar_list if c.tenant and c.tenant.id == tenant_id][offset:offset + limit]


@router.post("/calendar/{tenant_id}", response_model=Calendar, tags=["calendar"], status_code=201)
async def create_calendar(tenant_id: str, calendar: Calendar):
    """Create a new calendar event."""
    tenant = find_tenant_by_id(tenant_id)
    if any(c.id == calendar.id for c in calendar_list):
        raise HTTPException(status_code=400, detail="A calendar event with that ID already exists")

    calendar.tenant = tenant
    calendar_list.append(calendar)
    return calendar


@router.get("/calendar/{tenant_id}/{calendar_id}", response_model=Calendar, tags=["calendar"])
async def get_calendar(tenant_id: str, calendar_id: str):
    """Retrieve a single calendar event by its ID."""
    return find_item_by_id(calendar_id, calendar_list, "Calendar", tenant_id)


@router.put("/calendar/{tenant_id}/{calendar_id}", response_model=Calendar, tags=["calendar"])
async def update_calendar(tenant_id: str, calendar_id: str, title: str, description: str):
    """Update a calendar event's details."""
    calendar = find_item_by_id(calendar_id, calendar_list, "Calendar", tenant_id)
    calendar.title = title
    calendar.description = description
    calendar.updatedAt = get_timestamp()
    return calendar


@router.delete("/calendar/{tenant_id}/{calendar_id}", response_model=Calendar, tags=["calendar"])
async def delete_calendar(tenant_id: str, calendar_id: str):
    """Delete a calendar event by its ID and return the deleted object."""
    calendar = find_item_by_id(calendar_id, calendar_list, "Calendar", tenant_id)
    calendar_list.remove(calendar)
    return calendar
