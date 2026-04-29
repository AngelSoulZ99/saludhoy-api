#Importaciones.
from pydantic import BaseModel
from models.role import Role
from models.identification import Identification

class Doctor(BaseModel):
    id: str | None = None
    name: str
    email: str
    address: str
    password: str
    role: Role
    phones: list[str]
    identification: Identification
    specialties: list[str]