"""
Main entry point for the vitiviniculture-api FastAPI application.
Handles configuration, route registration, and app startup.
"""

import asyncio

from fastapi import FastAPI

from api.core.config import settings
from api.routes import auth
from api.routes import category
from database.db import init_db

from api.background_jobs.sync_categories_job import periodic_sync_job

app = FastAPI(
    title="VitiViniculture API",
    description="Public API for vitiviniculture data",
    version="1.0.0",
    debug=settings.DEBUG,
)


@app.on_event("startup")
async def startup_event():
    init_db()
    if settings.ENV == "PROD":
        asyncio.create_task(periodic_sync_job())


# Register routers
app.include_router(auth.router)
app.include_router(category.router)