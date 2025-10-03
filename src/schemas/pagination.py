"""
Pydantic schemas for paginated API responses.
"""
from typing import Generic, List, TypeVar, Optional
from pydantic import BaseModel, Field


DataT = TypeVar('DataT')


class PaginationMeta(BaseModel):
    """Metadata for a paginated response."""
    total_items: int = Field(description="Total number of items available")
    total_pages: int = Field(description="Total number of pages available")
    current_page: int = Field(description="The current page number (1-indexed)")
    page_size: int = Field(description="The number of items per page")
    has_next: bool = Field(description="Indicates if there is a next page")
    has_previous: bool = Field(description="Indicates if there is a previous page")
    next_page: Optional[int] = Field(None, description="The next page number, if available")
    previous_page: Optional[int] = Field(None, description="The previous page number, if available")


class PaginatedResponse(BaseModel, Generic[DataT]):
    """Generic schema for a paginated API response."""
    data: List[DataT] = Field(description="The list of items for the current page")
    meta: PaginationMeta = Field(description="Pagination metadata")
