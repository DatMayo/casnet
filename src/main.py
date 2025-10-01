"""
Main application file for the Casnet backend.

This file initializes the FastAPI application and includes the necessary routers.
"""
from fastapi import FastAPI
from .routers import tenant, user, person, task, calendar

app = FastAPI()

app.include_router(tenant.router)
app.include_router(user.router)
app.include_router(person.router)
app.include_router(task.router)
app.include_router(calendar.router)
