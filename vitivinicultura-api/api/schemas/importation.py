from pydantic import BaseModel, Field
from typing import Optional


class ImportationItem(BaseModel):
    pais: str = Field(..., alias="Países")
    quantidade_kg: Optional[float] = Field(None, alias="Quantidade (Kg)")
    valor_usd: Optional[float] = Field(None, alias="Valor (US$)")
    ano: int
    subopcao: Optional[str]

    class Config:
        populate_by_name = True
        from_attributes = True
        validate_by_name = True
