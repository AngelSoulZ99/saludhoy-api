from pydantic import BaseModel
from models.appointment_status import AppointmentStatus
from models.status_history import StatusHistory
from datetime import datetime

class Appointment(BaseModel):
    id: str | None = None
    created_at: datetime
    patient_id: str
    doctor_id: str
    admin_id: str
    office_id: str
    status_history: list[StatusHistory]
    current_state: AppointmentStatus