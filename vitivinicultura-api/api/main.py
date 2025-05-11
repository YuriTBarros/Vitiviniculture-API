"""
Main entry point for the vitiviniculture-api FastAPI application.
Handles configuration, route registration, and app startup.
"""

from fastapi import FastAPI

from api.core.config import settings
from api.routes import auth
from api.routes import category
from database.db import init_db

app = FastAPI(
    title="VitiViniculture API",
    description="Public API for vitiviniculture data",
    version="1.0.0",
    debug=settings.DEBUG,
)


@app.on_event("startup")
async def startup_event():
    init_db()


# Register routers
app.include_router(auth.router)
app.include_router(category.router)
