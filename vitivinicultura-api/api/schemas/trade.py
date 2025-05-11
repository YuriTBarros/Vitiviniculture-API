from pydantic import BaseModel, Field
from typing import Optional


class TradeItem(BaseModel):
    produto: str = Field(..., alias="Produto")
    quantidade_l: Optional[float] = Field(None, alias="Quantidade (L.)")
    ano: int
    categoria: str = Field(..., alias="Categoria")

    class Config:
        populate_by_name = True
        from_attributes = True
        validate_by_name = True
