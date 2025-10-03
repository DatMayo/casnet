"""
Custom exception classes for structured error handling.

This module defines custom exceptions that automatically generate proper
HTTP responses with structured error models.
"""
from typing import List, Optional
from fastapi import HTTPException, status

from src.schemas.error import (
    BaseErrorResponse,
    ValidationErrorResponse,
    ValidationErrorDetail,
    AuthenticationErrorResponse,
    AuthorizationErrorResponse,
    NotFoundErrorResponse,
    ConflictErrorResponse,
    TenantAccessErrorResponse
)


class BaseAPIException(HTTPException):
    """Base class for all API exceptions."""
    
    def __init__(self, error_response: BaseErrorResponse, status_code: int):
        super().__init__(
            status_code=status_code,
            detail=error_response.dict()
        )


# Authentication & Authorization Exceptions
class AuthenticationError(BaseAPIException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication required"):
        error_response = AuthenticationErrorResponse(
            error_code="AUTHENTICATION_REQUIRED",
            message=message
        )
        super().__init__(error_response, status.HTTP_401_UNAUTHORIZED)


class InvalidCredentialsError(BaseAPIException):
    """Raised when credentials are invalid."""
    
    def __init__(self, message: str = "Invalid username or password"):
        error_response = AuthenticationErrorResponse(
            error_code="INVALID_CREDENTIALS",
            message=message
        )
        super().__init__(error_response, status.HTTP_401_UNAUTHORIZED)


class AuthorizationError(BaseAPIException):
    """Raised when user lacks required permissions."""
    
    def __init__(self, message: str, required_permissions: List[str] = None):
        error_response = AuthorizationErrorResponse(
            error_code="INSUFFICIENT_PERMISSIONS",
            message=message,
            required_permissions=required_permissions or []
        )
        super().__init__(error_response, status.HTTP_403_FORBIDDEN)


class TenantAccessError(BaseAPIException):
    """Raised when user attempts to access unauthorized tenant."""
    
    def __init__(self, tenant_id: str, user_tenants: List[str] = None):
        error_response = TenantAccessErrorResponse(
            error_code="TENANT_ACCESS_DENIED",
            message=f"Access denied: You are not assigned to tenant '{tenant_id}'",
            tenant_id=tenant_id,
            user_tenants=user_tenants or []
        )
        super().__init__(error_response, status.HTTP_403_FORBIDDEN)


# Resource Not Found Exceptions
class ResourceNotFoundError(BaseAPIException):
    """Raised when a requested resource is not found."""
    
    def __init__(self, resource_type: str, resource_id: str):
        error_response = NotFoundErrorResponse(
            error_code="RESOURCE_NOT_FOUND",
            message=f"{resource_type} with ID '{resource_id}' not found",
            resource_type=resource_type,
            resource_id=resource_id
        )
        super().__init__(error_response, status.HTTP_404_NOT_FOUND)


class TenantNotFoundError(BaseAPIException):
    """Raised when a tenant is not found."""
    
    def __init__(self, tenant_id: str):
        error_response = NotFoundErrorResponse(
            error_code="TENANT_NOT_FOUND",
            message=f"Tenant with ID '{tenant_id}' not found",
            resource_type="Tenant",
            resource_id=tenant_id
        )
        super().__init__(error_response, status.HTTP_404_NOT_FOUND)


class UserNotFoundError(BaseAPIException):
    """Raised when a user is not found."""
    
    def __init__(self, user_identifier: str):
        error_response = NotFoundErrorResponse(
            error_code="USER_NOT_FOUND",
            message=f"User '{user_identifier}' not found",
            resource_type="User",
            resource_id=user_identifier
        )
        super().__init__(error_response, status.HTTP_404_NOT_FOUND)


# Validation & Conflict Exceptions
class ValidationError(BaseAPIException):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, field_errors: List[ValidationErrorDetail] = None):
        error_response = ValidationErrorResponse(
            error_code="VALIDATION_FAILED",
            message=message,
            field_errors=field_errors or []
        )
        super().__init__(error_response, status.HTTP_400_BAD_REQUEST)


class ResourceConflictError(BaseAPIException):
    """Raised when a resource conflict occurs."""
    
    def __init__(self, message: str, conflicting_resource: str = None):
        error_response = ConflictErrorResponse(
            error_code="RESOURCE_CONFLICT",
            message=message,
            conflicting_resource=conflicting_resource
        )
        super().__init__(error_response, status.HTTP_409_CONFLICT)


class DuplicateResourceError(BaseAPIException):
    """Raised when attempting to create a duplicate resource."""
    
    def __init__(self, resource_type: str, identifier: str):
        error_response = ConflictErrorResponse(
            error_code="DUPLICATE_RESOURCE",
            message=f"{resource_type} with identifier '{identifier}' already exists",
            conflicting_resource=identifier
        )
        super().__init__(error_response, status.HTTP_409_CONFLICT)
