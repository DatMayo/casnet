"""
Main application file for the Casnet backend.

This file initializes the FastAPI application, configures middleware, and includes
the API routers for all the application's endpoints.
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
from .routers import tenant, user, person, task, calendar, record, tag, auth, health
from .exceptions import BaseAPIException
from .model.error import BaseErrorResponse
from .config import settings

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version
)


# Custom middleware for request size limiting
@app.middleware("http")
async def limit_upload_size(request: Request, call_next):
    """Limit request body size to prevent large payload attacks."""
    if request.method in ["POST", "PUT", "PATCH"]:
        content_length = request.headers.get("content-length")
        if content_length:
            content_length = int(content_length)
            if content_length > settings.max_request_size:
                error_response = BaseErrorResponse(
                    error_code="REQUEST_TOO_LARGE",
                    message=f"Request body too large. Maximum size: {settings.max_request_size} bytes"
                )
                return JSONResponse(
                    status_code=413,
                    content=error_response.dict()
                )
    
    response = await call_next(request)
    return response


# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Authorization",
        "Content-Type", 
        "X-Requested-With",
        "Accept",
        "Origin",
        "User-Agent",
        "DNT",
        "Cache-Control",
        "X-Mx-ReqToken",
        "Keep-Alive",
        "X-Requested-With",
        "If-Modified-Since",
    ],
    expose_headers=[
        "X-RateLimit-Limit",
        "X-RateLimit-Remaining", 
        "X-RateLimit-Reset",
        "X-RateLimit-Reset-After"
    ]
)


@app.exception_handler(BaseAPIException)
async def api_exception_handler(request: Request, exc: BaseAPIException):
    """Handle custom API exceptions with structured error responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
        headers=getattr(exc, 'headers', None)
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle standard HTTP exceptions and convert them to structured format."""
    error_response = BaseErrorResponse(
        error_code="HTTP_EXCEPTION",
        message=exc.detail if isinstance(exc.detail, str) else "HTTP Error"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict(),
        headers=getattr(exc, 'headers', None)
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions with a structured error response."""
    error_response = BaseErrorResponse(
        error_code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred. Please try again later."
    )
    return JSONResponse(
        status_code=500,
        content=error_response.dict()
    )


# Include routers
app.include_router(health.router)  # Health checks (no auth required)
app.include_router(auth.router)
app.include_router(tenant.router)
app.include_router(user.router)
app.include_router(person.router)
app.include_router(task.router)
app.include_router(calendar.router)
app.include_router(record.router)
app.include_router(tag.router)
