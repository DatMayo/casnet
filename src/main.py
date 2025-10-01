"""
Main application file for the Casnet backend.

This file initializes the FastAPI application and includes the necessary routers.
"""
from fastapi import FastAPI
from .routers import tenant, user

app = FastAPI()

app.include_router(tenant.router)
app.include_router(user.router)
