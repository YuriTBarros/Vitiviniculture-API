from api.schemas.exportation import ExportationItem
from api.schemas.importation import ImportationItem
from api.schemas.production import ProductionItem
from api.schemas.trade import TradeItem
from api.schemas.processing import ProcessingItem

schemas_registry = {
    "exportation": ExportationItem,
    "importation": ImportationItem,
    "production": ProductionItem,
    "trade": TradeItem,
    "processing": ProcessingItem,
}
