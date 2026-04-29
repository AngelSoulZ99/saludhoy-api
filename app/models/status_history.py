# Importaciones.
from pydantic import BaseModel
from models.appointment_status import AppointmentStatus
from datetime import datetime
from models.role import Role

class StatusHistory(BaseModel):
    id: str | None = None
    appointment_status : AppointmentStatus
    changed_at: datetime
    changed_by: Role