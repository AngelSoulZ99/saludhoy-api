# Importaciones.
from pydantic import BaseModel

class Office(BaseModel):
    id: str | None = None
    name: str
    specialties: list[str]