# Importaciones.
from pydantic import BaseModel

class Identification(BaseModel):
    type: str
    number: str