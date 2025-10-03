"""
Pydantic schemas for structured API error responses.
"""
from typing import List, Optional, Any
from pydantic import BaseModel, Field

# --- Base Error Schemas ---

class BaseErrorResponse(BaseModel):
    """Base schema for all structured error responses."""
    error_code: str = Field(description="A unique code identifying the error type")
    message: str = Field(description="A human-readable error message")

# --- Validation Error Schemas ---

class ValidationErrorDetail(BaseModel):
    """Schema for a single field's validation error."""
    field: str = Field(description="The name of the invalid field")
    message: str = Field(description="A description of the validation error")
    invalid_value: Optional[Any] = Field(None, description="The value that failed validation")

class ValidationErrorResponse(BaseErrorResponse):
    """Schema for validation errors, including details for each invalid field."""
    field_errors: List[ValidationErrorDetail] = Field(description="A list of validation errors for specific fields")

# --- Authentication and Authorization Error Schemas ---

class AuthenticationErrorResponse(BaseErrorResponse):
    """Schema for authentication-related errors."""
    pass

class AuthorizationErrorResponse(BaseErrorResponse):
    """Schema for authorization errors, including required permissions."""
    required_permissions: List[str] = Field([], description="A list of permissions required for the operation")

class TenantAccessErrorResponse(BaseErrorResponse):
    """Schema for tenant access errors."""
    tenant_id: str = Field(description="The ID of the tenant that access was denied to")
    user_tenants: List[str] = Field([], description="A list of tenants the user has access to")

# --- Resource Not Found Error Schema ---

class NotFoundErrorResponse(BaseErrorResponse):
    """Schema for errors when a resource is not found."""
    resource_type: str = Field(description="The type of the resource that was not found")
    resource_id: str = Field(description="The ID of the resource that was not found")

# --- Conflict Error Schema ---

class ConflictErrorResponse(BaseErrorResponse):
    """Schema for resource conflict errors."""
    conflicting_resource: Optional[str] = Field(None, description="The identifier of the conflicting resource")

