"""
Error response models for structured API error handling.

This module defines Pydantic models for consistent error responses across the API,
providing clear error codes, messages, and additional context for debugging.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

from src.util import get_timestamp


class BaseErrorResponse(BaseModel):
    """Base error response model with common fields."""
    error_code: str
    message: str
    timestamp: int = Field(default_factory=get_timestamp)
    request_id: Optional[str] = None


class ValidationErrorDetail(BaseModel):
    """Details for field validation errors."""
    field: str
    message: str
    invalid_value: Any = None


class ValidationErrorResponse(BaseErrorResponse):
    """Error response for validation failures."""
    field_errors: List[ValidationErrorDetail] = []


class AuthenticationErrorResponse(BaseErrorResponse):
    """Error response for authentication failures."""
    pass


class AuthorizationErrorResponse(BaseErrorResponse):
    """Error response for authorization/permission failures."""
    required_permissions: List[str] = []
    user_permissions: List[str] = []


class NotFoundErrorResponse(BaseErrorResponse):
    """Error response for resource not found errors."""
    resource_type: str
    resource_id: str


class ConflictErrorResponse(BaseErrorResponse):
    """Error response for resource conflicts."""
    conflicting_resource: Optional[str] = None


class TenantAccessErrorResponse(AuthorizationErrorResponse):
    """Specific error response for tenant access violations."""
    tenant_id: str
    user_tenants: List[str] = []


class RateLimitErrorResponse(BaseErrorResponse):
    """Error response for rate limiting."""
    retry_after: int
    limit: int
    window: int
