"""
Defines the Pydantic models for health check responses.

This module contains the response models for various health check endpoints,
providing structured health status information.
"""
from datetime import datetime
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response model for basic health check endpoints."""
    status: str
    timestamp: datetime
    version: str
    environment: str


class DetailedHealthResponse(HealthResponse):
    """Extended health response with comprehensive application metrics."""
    uptime_seconds: float
    data_status: dict
    configuration_status: dict


class ReadinessResponse(BaseModel):
    """Response model for readiness check endpoint."""
    status: str
    message: str


class LivenessResponse(BaseModel):
    """Response model for liveness check endpoint."""
    status: str
    message: str
