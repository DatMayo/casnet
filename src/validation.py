"""
Input validation and sanitization utilities.

This module provides functions to validate and sanitize user input
to prevent security issues like injection attacks, excessive data,
and malformed content.
"""
import re
from typing import Optional
from src.config import settings
from src.exceptions import ValidationError, ValidationErrorDetail


def validate_string_length(
    value: str, 
    field_name: str, 
    max_length: Optional[int] = None,
    min_length: int = 0
) -> str:
    """
    Validate string length and return sanitized string.
    
    Args:
        value: The string to validate
        field_name: Name of the field for error messages
        max_length: Maximum allowed length (uses config default if None)
        min_length: Minimum required length
        
    Returns:
        Sanitized string
        
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(value, str):
        raise ValidationError(
            message=f"Field '{field_name}' must be a string",
            field_errors=[ValidationErrorDetail(
                field=field_name,
                message="Must be a string type",
                invalid_value=type(value).__name__
            )]
        )
    
    # Use default max length from settings if not specified
    if max_length is None:
        max_length = settings.max_string_length
    
    # Trim whitespace
    value = value.strip()
    
    # Check length constraints
    if len(value) < min_length:
        raise ValidationError(
            message=f"Field '{field_name}' is too short",
            field_errors=[ValidationErrorDetail(
                field=field_name,
                message=f"Minimum length is {min_length} characters",
                invalid_value=len(value)
            )]
        )
    
    if len(value) > max_length:
        raise ValidationError(
            message=f"Field '{field_name}' is too long",
            field_errors=[ValidationErrorDetail(
                field=field_name,
                message=f"Maximum length is {max_length} characters",
                invalid_value=len(value)
            )]
        )
    
    return value


def validate_description(value: str, field_name: str = "description") -> str:
    """
    Validate description fields with larger length limits.
    
    Args:
        value: The description string to validate
        field_name: Name of the field for error messages
        
    Returns:
        Sanitized description string
    """
    return validate_string_length(
        value, 
        field_name, 
        max_length=settings.max_description_length,
        min_length=0
    )


def validate_name(value: str, field_name: str = "name") -> str:
    """
    Validate name fields (users, tenants, etc.).
    
    Args:
        value: The name string to validate  
        field_name: Name of the field for error messages
        
    Returns:
        Sanitized name string
    """
    # Names must be at least 1 character
    validated = validate_string_length(value, field_name, min_length=1)
    
    # Check for valid characters (letters, numbers, spaces, hyphens, underscores)
    if not re.match(r'^[a-zA-Z0-9\s\-_]+$', validated):
        raise ValidationError(
            message=f"Field '{field_name}' contains invalid characters",
            field_errors=[ValidationErrorDetail(
                field=field_name,
                message="Only letters, numbers, spaces, hyphens, and underscores are allowed",
                invalid_value=validated
            )]
        )
    
    return validated


def validate_email(value: Optional[str], field_name: str = "email") -> Optional[str]:
    """
    Validate email addresses.
    
    Args:
        value: The email string to validate (can be None)
        field_name: Name of the field for error messages
        
    Returns:
        Sanitized email string or None
    """
    if value is None or value.strip() == "":
        return None
    
    value = value.strip().lower()
    
    # Basic email regex (not perfect but good enough for most cases)
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, value):
        raise ValidationError(
            message=f"Field '{field_name}' is not a valid email address",
            field_errors=[ValidationErrorDetail(
                field=field_name,
                message="Must be a valid email address format",
                invalid_value=value
            )]
        )
    
    # Check length
    if len(value) > 254:  # RFC 5321 limit
        raise ValidationError(
            message=f"Field '{field_name}' is too long",
            field_errors=[ValidationErrorDetail(
                field=field_name,
                message="Email address must be 254 characters or less",
                invalid_value=len(value)
            )]
        )
    
    return value


def validate_color_code(value: str, field_name: str = "color") -> str:
    """
    Validate hex color codes.
    
    Args:
        value: The color code to validate
        field_name: Name of the field for error messages
        
    Returns:
        Sanitized color code
    """
    value = value.strip().upper()
    
    # Ensure it starts with #
    if not value.startswith('#'):
        value = '#' + value
    
    # Validate hex color pattern (#RRGGBB or #RGB)
    if not re.match(r'^#(?:[0-9A-F]{3}){1,2}$', value):
        raise ValidationError(
            message=f"Field '{field_name}' is not a valid color code",
            field_errors=[ValidationErrorDetail(
                field=field_name,
                message="Must be a valid hex color code (e.g., #FF0000 or #F00)",
                invalid_value=value
            )]
        )
    
    return value


def sanitize_input(value: str) -> str:
    """
    General input sanitization to prevent basic injection attacks.
    
    Args:
        value: String to sanitize
        
    Returns:
        Sanitized string
    """
    if not isinstance(value, str):
        return value
    
    # Remove null bytes
    value = value.replace('\x00', '')
    
    # Limit consecutive whitespace
    value = re.sub(r'\s+', ' ', value)
    
    # Trim whitespace
    value = value.strip()
    
    return value
