#Importaciones.
from pydantic import BaseModel
from datetime import datetime

class ClinicalNote(BaseModel):
    id: str | None = None
    created_at: datetime
    description: str
    doctor_id: str
    specialty_id: str
    office_id: str