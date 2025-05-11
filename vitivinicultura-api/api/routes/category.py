from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    status,
    Request,
)
from fastapi.responses import JSONResponse, PlainTextResponse

from api.models.category import SyncResponse

from api.core.security import get_current_user
from api.exceptions.scraper_not_found_exception import ScraperNotFoundException
from api.services import category_service

router = APIRouter(prefix="/category", tags=["category"])


@router.post(
    "/{category}/sync",
    summary="Fetch viticulture data from Embrapa",
    status_code=status.HTTP_202_ACCEPTED,
)
async def sync_category(
    category: str,
    background_tasks: BackgroundTasks,
    user: str = Depends(get_current_user),
) -> SyncResponse:
    """
    Triggers the scraper to fetch and store new viticulture data for a specific
        category asynchronously.

    Valid categories:
        - exportation
        - importation
        - processing
        - production
        - trade

    Args:
        category (str): The viticulture data category.
        background_tasks (BackgroundTasks): Used to run the sync process in
            the background.
        user (str): Authenticated user (injected via Depends).

    Returns:
        SyncResponse: Confirmation that the sync process has been initiated.

    Raises:
        HTTPException:
            - 404 if no scraper exists for the specified category.
    """
    try:
        background_tasks.add_task(category_service.sync, category)
        return SyncResponse(status="started")
    except ScraperNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.get("/{category}", summary="Fetch viticulture data from cached data")
def get_category(
    category: str,
    request: Request,
    user: str = Depends(get_current_user),
):
    """
    Return cached viticulture data in the format requested by the client
        (CSV or JSON).

    Acceptable categories:
        - exportation
        - importation
        - processing
        - production
        - trade

    Supported content types via Accept header:
        - application/json (default)
        - text/csv

    Args:
        category (str): Category of viticulture data.
        request (Request): FastAPI request object (used to inspect headers).
        user (str): Authenticated user.

    Returns:
        JSONResponse or PlainTextResponse: The data in requested format.

    Raises:
        HTTPException:
            - 404 if the category is not supported.
            - 406 if an unsupported media type is requested.
    """
    try:
        accept = request.headers.get("accept", "")

        if "text/csv" in accept:
            csv_content = category_service.get_csv(category)
            return PlainTextResponse(
                content=csv_content, media_type="text/csv"
            )

        elif "application/json" in accept or "*/*" in accept or not accept:
            json_content = category_service.get_json(category)
            return JSONResponse(content=json_content)

        else:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=(
                    "Unsupported response type. "
                    "Use 'application/json' or 'text/csv'."
                ),
            )

    except ScraperNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
