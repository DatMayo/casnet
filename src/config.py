"""
Configuration management using Pydantic settings.

This module handles all application configuration with environment variable support,
validation, and type safety.
"""
import os
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings


from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings with environment variable support."""
    
    def __init__(self):
        # Security Settings
        self.secret_key: str = os.getenv(
            "SECRET_KEY",
            "a_very_secret_key_that_should_be_in_an_env_file_change_this_in_production"
        )
        self.algorithm: str = os.getenv("ALGORITHM", "HS256")
        self.access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        
        # Development Settings
        self.data_count: int = int(os.getenv("DATA_COUNT", "10"))
        self.enable_detailed_logging: bool = os.getenv("ENABLE_DETAILED_LOGGING", "true").lower() == "true"
        self.environment: str = os.getenv("ENVIRONMENT", "development")
        
        # API Configuration
        self.api_title: str = os.getenv("API_TITLE", "Casnet Backend API")
        self.api_description: str = os.getenv(
            "API_DESCRIPTION",
            "A multi-tenant backend API with structured error handling"
        )
        self.api_version: str = os.getenv("API_VERSION", "1.0.0")
        self.api_prefix: str = os.getenv("API_PREFIX", "/api/v1")
        
        # CORS Settings - Handle both string and list formats
        allowed_origins = os.getenv("ALLOWED_ORIGINS")
        if allowed_origins:
            if isinstance(allowed_origins, str):
                self.allowed_origins = [origin.strip() for origin in allowed_origins.split(",")]
            else:
                self.allowed_origins = allowed_origins
        else:
            self.allowed_origins = [
                "http://localhost:3000",
                "http://127.0.0.1:3000",
                "http://localhost:5173",
                "http://127.0.0.1:5173",
                "http://localhost:8080",
                "http://127.0.0.1:8080",
                "http://localhost:4200",
                "http://127.0.0.1:4200"
            ]
        
        # Security & Limits
        self.max_request_size: int = int(os.getenv("MAX_REQUEST_SIZE", "16777216"))  # 16MB
        self.max_string_length: int = int(os.getenv("MAX_STRING_LENGTH", "1000"))
        self.max_description_length: int = int(os.getenv("MAX_DESCRIPTION_LENGTH", "5000"))
        
        # Database Settings
        self.database_url: str = os.getenv("DATABASE_URL", "sqlite:///./casnet.db")


# Create global settings instance
settings = Settings()

# Export commonly used values for backwards compatibility
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm  
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
