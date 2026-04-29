# Importaciones.
from pydantic import BaseModel

class Specialty(BaseModel):
    id: str | None = None
    name: str
    description: str