from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from typing import  Type
from api.services.scrapers_registry import scrapers_registry
from api.schemas.schemas_registry import schemas_registry
from api.core.security import get_current_user

router = APIRouter(prefix="/data", tags=["data"]) 

@router.get("/{category}", summary="Fetch viticulture data from Embrapa")

async def get_data_by_category(
    category: str,    
    limit: int = Query(100, description="Maximum number of results to return"),
    offset: int = Query(0, description="Offset for pagination - Where to start in the list."),
    user: dict = Depends(get_current_user)):
    """
    Retrieve JSON-formatted vitiviniculture data for a given category.

    Categories supported:
    - exportation
    - importation
    - processing
    - production
    - trade

    Each category uses a registered scraper to extract and transform raw data
    and an associated Pydantic schema to validate the returned structure.

    Args:
        category (str): The data category to retrieve.
        limit (int): Max number of results (default: 100)
        offset (int): Offset index for pagination (default: 0)
        user (User): The authenticated user making the request (injected via dependency).
    Returns:
        JSONResponse: A list of records in JSON format.
    """
    scraper_class = scrapers_registry.get(category.lower())
    schema_class: Type = schemas_registry.get(category)

    if not scraper_class or not schema_class:
        raise HTTPException(status_code=404, detail=f"Category '{category}' not supported.")
    try:
        scraper = scraper_class()
        raw_data = scraper.get_json()
        raw_data = raw_data[offset:offset + limit]
        validated_data = [schema_class(**item).dict() for item in raw_data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing data: {str(e)}")

    return JSONResponse(content=validated_data)