from pydantic import BaseModel, Field
from typing import Optional


class ProcessingItem(BaseModel):
    cultivo: str = Field(..., alias="Cultivar")
    quantidade_kg: Optional[float] = Field(None, alias="Quantidade (Kg)")
    valor_usd: Optional[float] = Field(None, alias="Valor (US$)")
    ano: int
    subopcao: Optional[str]
    categoria: str = Field(..., alias="Categoria")

    class Config:
        populate_by_name = True
        from_attributes = True
        validate_by_name = True
