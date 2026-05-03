# Importaciones.
from pydantic import BaseModel, Field
from models.identification import Identification
from models.role import Role
from models.status import Status

class Admin(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: str
    address: str
    role: Role
    status: Status = Status.active
    phones: list[str]
    identification: Identification