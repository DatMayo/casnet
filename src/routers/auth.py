"""
API endpoints for authentication and token management.

This module contains authentication endpoints:
- POST /auth/login - Authenticate user and get JWT access token
- POST /auth/logout - Logout current user (client-side token removal)
- POST /auth/refresh - Refresh current user's access token
- GET /auth/me - Get current authenticated user information with tenants
"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import User
from src.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, verify_password, get_current_user
from src.schemas.user import UserResponse

router = APIRouter()


def get_user(username: str, db: Session) -> User:
    """Retrieve a user from the database by their username."""
    return db.query(User).filter(User.name == username).first()


@router.post("/login", tags=["authentication"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate a user and return a JWT access token.
    
    **Endpoint**: `POST /auth/login`
    
    **Request Body** (form data):
    - username: User's login name
    - password: User's password
    
    **Response**:
    - access_token: JWT token for API authentication
    - token_type: Always "bearer"
    - expires_in: Token expiration time in seconds
    
    **Usage**: Include the token in subsequent requests:
    `Authorization: Bearer {access_token}`
    """
    from src.exceptions import InvalidCredentialsError
    
    user = get_user(form_data.username, db)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise InvalidCredentialsError()
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert to seconds
    }


@router.get("/me", response_model=UserResponse, tags=["authentication"])
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get information about the currently authenticated user.
    
    **Endpoint**: `GET /auth/me`
    
    **Authentication**: Required (Bearer token)
    
    **Response**: Complete user profile including:
    - User ID and username
    - Account timestamps (created_at, updated_at)
    - Full list of tenants the user has access to
    
    **Frontend Usage Examples**:
    - Display current user name in UI header
    - Populate tenant dropdown/selector
    - Implement role-based access control
    - Show user-specific dashboard content
    
    **Security**: Only returns data for the authenticated user.
    """
    return current_user


@router.post("/logout", tags=["authentication"])
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Logout the current user.
    
    **Endpoint**: `POST /auth/logout`
    
    **Authentication**: Required (Bearer token)
    
    **Note**: With JWT tokens, logout is typically handled client-side by:
    1. Removing the token from client storage (localStorage, cookies, etc.)
    2. Optionally calling this endpoint for server-side logging/analytics
    
    **Response**: Success confirmation message
    """
    return {"message": "Successfully logged out", "user": current_user.name}


@router.post("/refresh", tags=["authentication"])
async def refresh_token(
    current_user: User = Depends(get_current_user)
):
    """
    Refresh the current user's access token.
    
    **Endpoint**: `POST /auth/refresh`
    
    **Authentication**: Required (Bearer token)
    
    **Response**: New access token with updated expiration
    - access_token: New JWT token for API authentication
    - token_type: Always "bearer"
    - expires_in: Token expiration time in seconds
    
    **Usage**: Replace the old token with the new one in client storage
    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.name}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer", 
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert to seconds
    }
