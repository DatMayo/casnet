"""
API endpoints for calendar management.

This module contains routes for creating, reading, updating, and deleting calendar events.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Calendar, User
from ..dependencies import get_permission_checker, requires_permission_for_resource
from ..enum.epermission import EPermission
from ..schemas.pagination import PaginatedResponse
from ..schemas.calendar import CalendarCreate, CalendarUpdate, CalendarResponse

router = APIRouter()


@router.get("/calendar", response_model=PaginatedResponse[CalendarResponse], tags=["calendar"])
async def get_calendar_events(
    tenant_id: str = Query(..., description="ID of the tenant to retrieve calendar events from"),
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_permission_checker(EPermission.VIEW_CALENDAR))
):
    """Retrieve calendar events from a specific tenant with pagination."""
    events_query = db.query(Calendar).filter(Calendar.tenant_id == tenant_id)
    total_count = events_query.count()
    offset = (page - 1) * page_size
    events = events_query.offset(offset).limit(page_size).all()
    total_pages = (total_count + page_size - 1) // page_size
    return PaginatedResponse(
        data=events,
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


@router.post("/calendar", response_model=CalendarResponse, tags=["calendar"], status_code=201)
async def create_calendar_event(
    calendar_data: CalendarCreate,
    tenant_id: str = Query(..., description="ID of the tenant to create the event in"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_permission_checker(EPermission.CREATE_CALENDAR))
):
    """Create a new calendar event within a specific tenant."""
    new_event = Calendar(**calendar_data.model_dump(), tenant_id=tenant_id)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


@router.get("/calendar/{event_id}", response_model=CalendarResponse, tags=["calendar"])
async def get_calendar_event(
    event_id: str = Path(..., alias="resource_id", description="ID of the event to retrieve"),
    db: Session = Depends(get_db),
    current_user: User = Depends(requires_permission_for_resource(EPermission.VIEW_CALENDAR))
):
    """Retrieve a single calendar event by its ID."""
    event = db.query(Calendar).filter(Calendar.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail=f"Event with ID {event_id} not found")
    return event


@router.put("/calendar/{event_id}", response_model=CalendarResponse, tags=["calendar"])
async def update_calendar_event(
    calendar_data: CalendarUpdate,
    event_id: str = Path(..., alias="resource_id", description="ID of the event to update"),
    db: Session = Depends(get_db),
    current_user: User = Depends(requires_permission_for_resource(EPermission.EDIT_CALENDAR))
):
    """Update a calendar event's details."""
    event = db.query(Calendar).filter(Calendar.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail=f"Event with ID {event_id} not found")

    update_data = calendar_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(event, key, value)
    
    db.commit()
    db.refresh(event)
    return event


@router.delete("/calendar/{event_id}", response_model=CalendarResponse, tags=["calendar"])
async def delete_calendar_event(
    event_id: str = Path(..., alias="resource_id", description="ID of the event to delete"),
    db: Session = Depends(get_db),
    current_user: User = Depends(requires_permission_for_resource(EPermission.DELETE_CALENDAR))
):
    """Delete a calendar event by its ID."""
    event = db.query(Calendar).filter(Calendar.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail=f"Event with ID {event_id} not found")

    db.delete(event)
    db.commit()
    return event
