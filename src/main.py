"""
Main application file for the Casnet backend.

This file initializes the FastAPI application, configures middleware, and includes
the API routers for all the application's endpoints.
"""
from fastapi import FastAPI
from .routers import tenant, user, person, task, calendar, record, tag, auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(tenant.router)
app.include_router(user.router)
app.include_router(person.router)
app.include_router(task.router)
app.include_router(calendar.router)
app.include_router(record.router)
app.include_router(tag.router)
