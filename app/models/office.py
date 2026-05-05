# Importaciones.
from pydantic import BaseModel, Field

class Office(BaseModel):
    id: str | None = Field(default=None, alias="_id")
    name: str
    specialties: list[str]