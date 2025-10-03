"""
Configuration management using Pydantic settings.

This module handles all application configuration with environment variable support,
validation, and type safety.
"""
import os
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Security Settings
    secret_key: str = Field(
        default="a_very_secret_key_that_should_be_in_an_env_file_change_this_in_production",
        env="SECRET_KEY",
        description="Secret key for JWT token signing"
    )
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Development Settings
    data_count: int = Field(default=10, env="DATA_COUNT", description="Number of dummy records to generate")
    enable_detailed_logging: bool = Field(default=True, env="ENABLE_DETAILED_LOGGING")
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    # API Configuration
    api_title: str = Field(default="Casnet Backend API", env="API_TITLE")
    api_description: str = Field(
        default="A multi-tenant backend API with structured error handling", 
        env="API_DESCRIPTION"
    )
    api_version: str = Field(default="1.0.0", env="API_VERSION")
    api_prefix: str = Field(default="/api/v1", env="API_PREFIX")
    
    # CORS Settings
    allowed_origins: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://127.0.0.1:3000", 
            "http://localhost:5173",
            "http://127.0.0.1:5173"
        ],
        env="ALLOWED_ORIGINS",
        description="Allowed CORS origins for frontend applications"
    )
    
    # Database Settings (for future use)
    database_url: str = Field(
        default="sqlite:///./casnet.db", 
        env="DATABASE_URL",
        description="Database connection URL"
    )
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Parse comma-separated strings as lists
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> any:
            if field_name == 'allowed_origins':
                return [origin.strip() for origin in raw_val.split(',')]
            return cls.json_loads(raw_val)


# Create global settings instance
settings = Settings()

# Export commonly used values for backwards compatibility
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm  
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
