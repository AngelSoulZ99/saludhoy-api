# Importaciones.
from pydantic import BaseModel
from models.identification import Identification
from models.role import Role

class Admin(BaseModel):
    id: str | None = None
    name: str
    email: str
    address: str
    password: str
    role: Role
    phones: list[str]
    identification: Identification