"""
API endpoints for calendar management.

This module contains routes for creating, reading, updating, and deleting calendar events.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from ..database import calendar_list, Calendar
from ..util import get_timestamp, find_item_by_id, validate_user_tenant_access
from ..security import get_current_user
from ..model.user import UserAccount
from ..model.pagination import PaginatedResponse, paginate_data

router = APIRouter()


@router.get("/calendar/{tenant_id}", response_model=PaginatedResponse[Calendar], tags=["calendar"])
async def get_calendars(
    tenant_id: str,
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Number of calendar events per page"),
    current_user: UserAccount = Depends(get_current_user)
):
    """Retrieve a paginated list of calendar events for a specific tenant."""
    validate_user_tenant_access(tenant_id, current_user)
    
    # Filter calendar events by tenant
    tenant_calendars = [c for c in calendar_list if c.tenant and c.tenant.id == tenant_id]
    
    # Paginate the data
    paginated_calendars, pagination_meta = paginate_data(tenant_calendars, page, page_size)
    
    return PaginatedResponse(
        data=paginated_calendars,
        meta=pagination_meta
    )


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
async def update_calendar(
    tenant_id: str,
    calendar_id: str,
    title: str = Query(description="Updated title for the calendar event"),
    description: str = Query(description="Updated description for the calendar event"),
    current_user: UserAccount = Depends(get_current_user)
):
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
