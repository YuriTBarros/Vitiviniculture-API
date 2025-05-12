import asyncio
import os
import pandas as pd
from typing import Optional

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
    "processing": ProcessingScraper,
    "production": ProductionScraper,
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


def get_csv(
    category: str, offset: Optional[int] = None, limit: Optional[int] = None
) -> str:
    """
    Reads the cached CSV file for the given category and returns
    its paginated content as a CSV string.

    If offset and limit are not provided, returns the entire dataset.

    Args:
        category (str): Name of the data category.
        offset (int, optional): Number of items to skip. Default is 0.
        limit (int, optional): Maximum number of items to return.
            Default is 100.

    Returns:
        str: Paginated CSV content or full dataset if no pagination
            is requested.
    """
    _get_category_class(category)

    filepath = os.path.join(
        settings.LOCAL_CACHE_FOLDER, f"table_{category}.csv"
    )
    df = pd.read_csv(filepath)

    if offset is None and limit is None:
        paginated_df = df
    else:
        paginated_offset = offset if offset is not None else 0
        paginated_limit = limit if limit is not None else 100
        paginated_df = df.iloc[
            paginated_offset : paginated_offset + paginated_limit
        ]

    return paginated_df.to_csv(index=False)


def get_json(
    category: str, offset: Optional[int] = None, limit: Optional[int] = None
) -> list[dict]:
    """
    Reads the cached JSON file for the given category and returns
    its paginated content as a list of dictionaries.

    If offset and limit are not provided, returns the entire dataset.

    Args:
        category (str): Name of the data category.
        offset (int, optional): Number of items to skip. Default is 0.
        limit (int, optional): Maximum number of items to return.
            Default is 100.

    Returns:
        list[dict]: Paginated JSON data or full dataset if no pagination
            is requested.
    """
    _get_category_class(category)

    filepath = os.path.join(
        settings.LOCAL_CACHE_FOLDER, f"table_{category}.json"
    )
    df = pd.read_json(filepath)

    if offset is None and limit is None:
        paginated_df = df
    else:
        paginated_offset = offset if offset is not None else 0
        paginated_limit = limit if limit is not None else 100
        paginated_df = df.iloc[
            paginated_offset : paginated_offset + paginated_limit
        ]

    return paginated_df.to_dict(orient="records")


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
