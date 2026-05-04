# Importaciones.
from pydantic import BaseModel, Field

class Specialty(BaseModel):
    id: str | None = Field(default=None, alias="_id")
    name: str
    description: str