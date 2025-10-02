"""
Security module for handling JWT authentication and password hashing.

This module contains all the necessary components for securing the application,
including token creation, verification, and password management.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.model.user import UserAccount

# --- Configuration ---
SECRET_KEY = "a_very_secret_key_that_should_be_in_an_env_file"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["sha256_crypt", "bcrypt"], deprecated="auto")

# --- OAuth2 Scheme ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# --- Utility Functions ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a plain password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a new JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserAccount:
    """Decode the JWT and return the current user."""
    from src.routers.auth import get_user # Break circular import

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user
