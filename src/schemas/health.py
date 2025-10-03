"""
Pydantic schemas for health check API responses.
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class HealthResponse(BaseModel):
    """Basic health check response."""
    status: str = Field("healthy", description="Indicates the health status of the application")

class DetailedHealthResponse(HealthResponse):
    """Detailed health check response including version and environment."""
    version: str = Field(description="The version of the application")
    environment: str = Field(description="The environment the application is running in")
    timestamp: datetime = Field(description="The current server timestamp")
    uptime_seconds: float = Field(description="The number of seconds the server has been running")
    data_status: Dict[str, Any] = Field({}, description="Status of various data components")

class ReadinessResponse(BaseModel):
    """Kubernetes readiness probe response."""
    ready: bool = Field(description="Indicates if the application is ready to serve traffic")
    message: str = Field(description="A message indicating the readiness status")

class LivenessResponse(BaseModel):
    """Kubernetes liveness probe response."""
    alive: bool = Field(description="Indicates if the application is alive")
    message: str = Field(description="A message indicating the liveness status")
