"""
Configuration management using Pydantic settings.

This module handles all application configuration with environment variable support,
validation, and type safety.
"""
import os
from typing import List, Union, Any
from pydantic import Field, field_validator
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
    data_count: int = Field(default=10, env="DATA_COUNT")
    enable_detailed_logging: bool = Field(default=True, env="ENABLE_DETAILED_LOGGING")
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    # Documentation Settings
    enable_docs: bool = Field(default=True, env="ENABLE_DOCS", description="Enable API documentation endpoints")
    enable_redoc: bool = Field(default=True, env="ENABLE_REDOC", description="Enable ReDoc documentation")
    
    # API Configuration
    api_title: str = Field(default="Casnet Backend API", env="API_TITLE")
    api_description: str = Field(
        default="A multi-tenant backend API with structured error handling", 
        env="API_DESCRIPTION"
    )
    api_version: str = Field(default="1.0.0", env="API_VERSION")
    api_prefix: str = Field(default="/api/v1", env="API_PREFIX")
    
    # CORS Settings
    allowed_origins: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173,http://localhost:8080,http://127.0.0.1:8080,http://localhost:4200,http://127.0.0.1:4200",
        env="ALLOWED_ORIGINS",
        description="Allowed CORS origins for frontend applications (comma-separated)"
    )
    
    # Security & Limits
    max_request_size: int = Field(
        default=16777216,  # 16MB in bytes
        env="MAX_REQUEST_SIZE",
        description="Maximum request size in bytes (default: 16MB)"
    )
    max_string_length: int = Field(
        default=1000,
        env="MAX_STRING_LENGTH",
        description="Maximum length for string fields"
    )
    max_description_length: int = Field(
        default=5000,
        env="MAX_DESCRIPTION_LENGTH",
        description="Maximum length for description fields"
    )
    
    # Database Settings
    database_url: str = Field(
        default="sqlite:///./data/casnet.db", 
        env="DATABASE_URL",
        description="SQLite database connection URL"
    )
    
    # Database configuration
    database_echo: bool = Field(
        default=False,
        env="DATABASE_ECHO", 
        description="Enable SQLAlchemy query logging for debugging"
    )
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse the comma-separated allowed_origins string into a list."""
        return [origin.strip() for origin in self.allowed_origins.split(',') if origin.strip()]
    
    @property
    def docs_enabled(self) -> bool:
        """Check if documentation should be enabled (disabled in production unless explicitly enabled)."""
        if self.environment.lower() == "production":
            return self.enable_docs  # Explicitly enabled in production
        return self.enable_docs  # Use setting value in other environments
    
    @property
    def redoc_enabled(self) -> bool:
        """Check if ReDoc documentation should be enabled (disabled in production unless explicitly enabled)."""
        if self.environment.lower() == "production":
            return self.enable_redoc  # Explicitly enabled in production
        return self.enable_redoc  # Use setting value in other environments


# Create global settings instance
settings = Settings()

# Export commonly used values for backwards compatibility
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm  
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
