# Importaciones.
from enum import Enum

class AppointmentStatus(str, Enum):
    requested = "requested"
    scheduled = "scheduled"
    attended = "attended"
    cancelled = "cancelled"
    no_show = "no_show"