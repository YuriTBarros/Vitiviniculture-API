import asyncio
import os
import pandas as pd

from api.core.config import settings
from api.exceptions.scraper_not_found_exception import ScraperNotFoundException
from api.models.category import SyncResponse

from api.services.scrapers.exportation_scraper import ExportationScraper
from api.services.scrapers.importation_scraper import ImportationScraper
from api.services.scrapers.production_scraper import ProductionScraper
from api.services.scrapers.processing_scraper import ProcessingScraper
from api.services.scrapers.trade_scraper import TradeScraper

# Maps category names to their corresponding scraper classes
__scrapers_registry = {
    "exportation": ExportationScraper,
    "importation": ImportationScraper,
    "production": ProductionScraper,
    "processing": ProcessingScraper,
    "trade": TradeScraper,
}


async def sync(category: str) -> SyncResponse:
    """
    Executes the scraper for the specified category, caches the data locally,
    and returns the sync status.

    Args:
        category (str): Name of the data category (e.g., "exportation").

    Returns:
        SyncResponse: An object indicating "started".
    """
    scraper_class = _get_category_class(category)
    await asyncio.to_thread(
        scraper_class.sync,
        settings.EMBRAPA_URL,
        settings.LOCAL_CACHE_FOLDER,
        f"table_{category}",
    )
    return SyncResponse(status="started")


def get_csv(category: str) -> str:
    """
    Reads and returns the cached CSV content for the given category.

    Args:
        category (str): Name of the data category.

    Returns:
        str: Raw CSV content as a string.
    """
    _get_category_class(category)  # Validate category
    filepath = os.path.join(
        settings.LOCAL_CACHE_FOLDER, f"table_{category}.csv"
    )

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def get_json(category: str) -> list[dict]:
    """
    Reads the cached JSON file for the given category and returns
        its content as a list of dictionaries.

    Args:
        category (str): Name of the data category.

    Returns:
        list[dict]: Parsed JSON data.
    """
    _get_category_class(category)  # Validate category
    filepath = os.path.join(
        settings.LOCAL_CACHE_FOLDER, f"table_{category}.json"
    )

    df = pd.read_json(filepath)
    return df.to_dict(orient="records")


def _get_category_class(category: str):
    """
    Retrieves the scraper class associated with the given category.

    Args:
        category (str): Case-insensitive category name.

    Returns:
        Instance of the corresponding scraper class.

    Raises:
        ScraperNotFoundException: If the category is not supported.
    """
    scraper_class = __scrapers_registry.get(category.lower())
    if not scraper_class:
        raise ScraperNotFoundException(
            f"Category '{category.lower()}' is not supported."
        )
    return scraper_class()
