"""
API endpoints for calendar management.

This module contains routes for creating, reading, updating, and deleting calendar events.
"""
import uuid
from typing import List
from fastapi import APIRouter, HTTPException
from ..database import calendar_list, Calendar
from ..util import get_timestamp, find_item_by_id

router = APIRouter()


@router.get("/calendar", response_model=List[Calendar], tags=["calendar"])
async def get_calendars(limit: int = 100, offset: int = 0):
    """Retrieve a list of calendar events with optional pagination."""
    return calendar_list[offset:offset + limit]


@router.post("/calendar", response_model=Calendar, tags=["calendar"], status_code=201)
async def create_calendar(calendar: Calendar):
    """Create a new calendar event."""
    if any(c.id == calendar.id for c in calendar_list):
        raise HTTPException(status_code=400, detail="A calendar event with that ID already exists")

    calendar_list.append(calendar)
    return calendar


@router.get("/calendar/{calendar_id}", response_model=Calendar, tags=["calendar"])
async def get_calendar(calendar_id: str):
    """Retrieve a single calendar event by its ID."""
    return find_item_by_id(calendar_id, calendar_list, "Calendar")


@router.put("/calendar/{calendar_id}", response_model=Calendar, tags=["calendar"])
async def update_calendar(calendar_id: str, title: str, description: str):
    """Update a calendar event's details."""
    calendar = find_item_by_id(calendar_id, calendar_list, "Calendar")
    calendar.title = title
    calendar.description = description
    calendar.updatedAt = get_timestamp()
    return calendar


@router.delete("/calendar/{calendar_id}", response_model=Calendar, tags=["calendar"])
async def delete_calendar(calendar_id: str):
    """Delete a calendar event by its ID and return the deleted object."""
    calendar = find_item_by_id(calendar_id, calendar_list, "Calendar")
    calendar_list.remove(calendar)
    return calendar
