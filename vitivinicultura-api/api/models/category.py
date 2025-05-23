from enum import Enum
from pydantic import BaseModel


class SyncResponse(BaseModel):
    """
    Represents the status of the sync process.

    Attributes:
        status (str): The status of the synchronization,
            e.g., "started" or "completed".
    """

    status: str


class CategoryEnum(str, Enum):
    """
    Enum representing the available categories for the synchronization process.

    - exportation: Exportation category
    - importation: Importation category
    - processing: Processing category
    - production: Production category
    - trade: Trade category
    """

    exportation = "exportation"
    importation = "importation"
    processing = "processing"
    production = "production"
    trade = "trade"
