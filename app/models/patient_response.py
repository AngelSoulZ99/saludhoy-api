# Importaciones.
from pydantic import BaseModel, Field
from models.identification import Identification
from models.clinical_note import ClinicalNote
from models.role import Role

class PatientResponse(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: str
    address: str
    role: Role
    phones: list[str]
    identification: Identification
    medical_history: list[ClinicalNote]