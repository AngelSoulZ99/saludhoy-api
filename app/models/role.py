#Importaciones.
from enum import Enum

class Role(str, Enum):
    patient = "patient"
    doctor = "doctor"
    admin = "admin"