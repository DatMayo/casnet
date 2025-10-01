"""
Utility functions for the application.

This module contains common helper functions, such as timestamp generation,
that are used across the application.
"""
import datetime
from typing import List, TypeVar
from fastapi import HTTPException

T = TypeVar('T')


def get_timestamp():
    """Returns the current timestamp in milliseconds."""
    now = datetime.datetime.now()
    return int(now.timestamp() * 1000)


def find_item_by_id(item_id: str, item_list: List[T], item_name: str) -> T:
    """Find an item in a list by its ID or raise a 404 error."""
    for item in item_list:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail=f"{item_name} not found")
