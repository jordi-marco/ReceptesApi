from pydantic import BaseModel, Field
from typing import Optional

# --- ESQUEMES DE DADES (Pydantic - Python 3.9+ style) ---
class ReceptaBase(BaseModel):
    nom: str
    descripcio: str
    minuts: int
    ingredients: list[str] = []
    likes: int = 0
    url_imatge: Optional[str] = Field(None, alias="urlImatge")
    class Config:
        populate_by_name = True
        from_attributes = True

class ReceptaCreate(ReceptaBase):
    pass

class ReceptaResponse(ReceptaBase):
    id: int
