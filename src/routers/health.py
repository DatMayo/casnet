"""
Health check endpoints for monitoring and deployment.

This module provides endpoints to check the application's health status,
dependencies, and readiness for serving requests.
"""
import time
from datetime import datetime, timezone
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from src.config import settings
from src.database import get_db
from src.models import User, Tenant
from ..schemas.health import HealthResponse, DetailedHealthResponse, ReadinessResponse, LivenessResponse

router = APIRouter()


# Track application start time for uptime calculation
_start_time = time.time()


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    tags=["health"],
    summary="Basic health check",
    description="Simple health check endpoint that returns application status"
)
async def health_check():
    """
    Basic health check endpoint.
    
    Returns a simple status indicating the application is running.
    This endpoint is typically used by load balancers and monitoring systems.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc),
        version=settings.api_version,
        environment=settings.environment
    )


@router.get(
    "/health/detailed",
    response_model=DetailedHealthResponse,
    status_code=status.HTTP_200_OK,
    tags=["health"],
    summary="Detailed health check",
    description="Comprehensive health check with application metrics and status details"
)
async def detailed_health_check(db: Session = Depends(get_db)):
    """
    Detailed health check endpoint.
    
    Returns comprehensive information about the application status,
    including uptime, data status, and configuration status.
    """
    current_time = time.time()
    uptime = current_time - _start_time
    
    # Get actual database counts
    tenant_count = db.query(Tenant).count()
    user_count = db.query(User).count()
    
    return DetailedHealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc),
        version=settings.api_version,
        environment=settings.environment,
        uptime_seconds=uptime,
        data_status={
            "tenants_loaded": tenant_count,
            "users_loaded": user_count,
            "database_initialized": user_count > 0,  # Should have at least admin user
            "admin_account_exists": db.query(User).filter(User.name == "admin").first() is not None
        },
        configuration_status={
            "database_url": settings.database_url,
            "logging_enabled": settings.enable_detailed_logging,
            "cors_configured": len(settings.allowed_origins_list) > 0,
            "allowed_origins": settings.allowed_origins_list,
            "environment": settings.environment
        }
    )


@router.get(
    "/health/ready",
    response_model=ReadinessResponse,
    status_code=status.HTTP_200_OK,
    tags=["health"], 
    summary="Readiness check",
    description="Indicates if the application is ready to serve requests"
)
async def readiness_check():
    """
    Readiness check endpoint.
    
    Returns HTTP 200 if the application is ready to serve requests,
    or HTTP 503 if the application is not yet ready.
    
    This is useful for Kubernetes readiness probes and deployment systems.
    """
    # Check if essential data is loaded
    if len(tenant_list) == 0:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Application not ready: tenant data not loaded"
        )
    
    if len(user_list) == 0:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Application not ready: user data not loaded"
        )
    
    return ReadinessResponse(
        status="ready", 
        message="Application is ready to serve requests"
    )


@router.get(
    "/health/live",
    response_model=LivenessResponse,
    status_code=status.HTTP_200_OK,
    tags=["health"],
    summary="Liveness check",
    description="Indicates if the application process is alive"
)
async def liveness_check():
    """
    Liveness check endpoint.
    
    Simple endpoint that indicates the application process is alive.
    This is useful for Kubernetes liveness probes.
    
    If this endpoint returns anything other than 200, the container should be restarted.
    """
    return LivenessResponse(
        status="alive", 
        message="Application is running"
    )
