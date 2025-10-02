"""
API endpoints for authentication and token management.

This module contains the '/token' endpoint for exchanging user credentials for a JWT.
"""
from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.database import user_list
from src.model.user import UserAccount
from src.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, verify_password

router = APIRouter()


def get_user(username: str) -> UserAccount:
    """Retrieve a user from the database by their username."""
    for user in user_list:
        if user.name == username:
            return user
    return None


@router.post("/token", tags=["authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate a user and return a JWT access token."""
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
