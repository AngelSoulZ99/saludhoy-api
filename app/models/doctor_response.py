#Importaciones.
from pydantic import BaseModel, Field
from models.role import Role
from models.identification import Identification
from models.status import Status

class DoctorResponse(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: str
    address: str
    role: Role
    status: Status = Status.active
    phones: list[str]
    identification: Identification
    specialties: list[str]