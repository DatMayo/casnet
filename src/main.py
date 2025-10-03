"""
Main application file for the Casnet backend.

This file initializes the FastAPI application, configures middleware, and includes
the API routers for all the application's endpoints.
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from .routers import tenant, user, person, task, calendar, record, tag, auth
from .exceptions import BaseAPIException
from .model.error import BaseErrorResponse

app = FastAPI(
    title="Casnet Backend API",
    description="A multi-tenant backend API with structured error handling",
    version="1.0.0"
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
app.include_router(auth.router)
app.include_router(tenant.router)
app.include_router(user.router)
app.include_router(person.router)
app.include_router(task.router)
app.include_router(calendar.router)
app.include_router(record.router)
app.include_router(tag.router)
