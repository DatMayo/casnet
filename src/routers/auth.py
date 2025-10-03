"""
API endpoints for authentication and token management.

This module contains the '/token' endpoint for exchanging user credentials for a JWT.
"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import User
from src.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, verify_password

router = APIRouter()


def get_user(username: str, db: Session) -> User:
    """Retrieve a user from the database by their username."""
    return db.query(User).filter(User.name == username).first()


@router.post("/token", tags=["authentication"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authenticate a user and return a JWT access token."""
    from src.exceptions import InvalidCredentialsError
    
    user = get_user(form_data.username, db)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise InvalidCredentialsError()
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
