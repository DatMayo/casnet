"""
Defines the Pydantic models for API pagination responses.

This module contains the pagination metadata models that provide
comprehensive information about paginated data responses.
"""
from typing import List, TypeVar, Generic
from pydantic import BaseModel, Field

# Generic type for paginated data
T = TypeVar('T')


class PaginationMeta(BaseModel):
    """Metadata for paginated responses."""
    total_items: int = Field(description="Total number of items across all pages")
    total_pages: int = Field(description="Total number of pages available")
    current_page: int = Field(description="Current page number (1-indexed)")
    page_size: int = Field(description="Number of items per page")
    has_next: bool = Field(description="Whether there is a next page available")
    has_previous: bool = Field(description="Whether there is a previous page available")
    next_page: int | None = Field(default=None, description="Next page number if available")
    previous_page: int | None = Field(default=None, description="Previous page number if available")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper."""
    data: List[T] = Field(description="The actual data items for this page")
    meta: PaginationMeta = Field(description="Pagination metadata")


def create_pagination_meta(
    total_items: int,
    page: int,
    page_size: int
) -> PaginationMeta:
    """
    Helper function to create pagination metadata.
    
    Args:
        total_items: Total number of items across all pages
        page: Current page number (1-indexed)
        page_size: Number of items per page
        
    Returns:
        PaginationMeta object with calculated pagination information
    """
    total_pages = (total_items + page_size - 1) // page_size  # Ceiling division
    has_next = page < total_pages
    has_previous = page > 1
    
    return PaginationMeta(
        total_items=total_items,
        total_pages=total_pages,
        current_page=page,
        page_size=page_size,
        has_next=has_next,
        has_previous=has_previous,
        next_page=page + 1 if has_next else None,
        previous_page=page - 1 if has_previous else None
    )


def paginate_data(data: List[T], page: int, page_size: int) -> tuple[List[T], PaginationMeta]:
    """
    Helper function to paginate data and create metadata.
    
    Args:
        data: The complete list of data to paginate
        page: Current page number (1-indexed)
        page_size: Number of items per page
        
    Returns:
        Tuple of (paginated_data, pagination_meta)
    """
    total_items = len(data)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    paginated_data = data[start_idx:end_idx]
    meta = create_pagination_meta(total_items, page, page_size)
    
    return paginated_data, meta
