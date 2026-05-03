# Importaciones.
from pydantic import BaseModel # Se importa BaseModel para crear los esquemas de los datos.
from models.identification import Identification
from models.clinical_note import ClinicalNote
from models.role import Role
from models.status import Status

class Patient(BaseModel):
    id: str | None = None
    name: str
    email: str
    address: str
    password: str
    role: Role
    status: Status = Status.active
    phones: list[str]
    identification: Identification
    medical_history: list[ClinicalNote]