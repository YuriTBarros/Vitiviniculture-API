from pydantic import BaseModel, Field
from typing import Optional

class ExportationItem(BaseModel):
    pais: str = Field(..., alias="Países")
    quantidade_kg: Optional[float] = Field(None, alias="Quantidade (Kg)")
    valor_usd: Optional[float] = Field(None, alias="Valor (US$)")
    ano: int
    subopcao: Optional[str]

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
        orm_mode = True