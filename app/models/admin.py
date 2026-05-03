# Importaciones.
from pydantic import BaseModel
from models.identification import Identification
from models.role import Role
from models.status import Status

class Admin(BaseModel):
    id: str | None = None
    name: str
    email: str
    address: str
    password: str
    role: Role
    status: Status = Status.active
    phones: list[str]
    identification: Identification