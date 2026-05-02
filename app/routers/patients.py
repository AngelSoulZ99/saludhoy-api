# Importaciones.
from fastapi import APIRouter, HTTPException, status
from models.patient import Patient
from models.patient_response import PatientResponse
from database import db
from core.security import hash_password
from bson import ObjectId

# Instancia para el router.
router = APIRouter(prefix="/patients",
                tags=["patients"],
                responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

# Función para realizar la búsqueda de un paciente.
async def search_patient(field: str, key):

    patient = await db.patients.find_one({field: key})

    if patient is None:
        return None
    
    patient["_id"] = str(patient["_id"])
    return patient

# Endpoint de POST.
@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(patient: Patient):
    
    if isinstance(await search_patient("email", patient.email), Patient):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 
                            detail="El usuario ya existe.")

    patient_dict = patient.model_dump()
    del patient_dict["id"]
    patient_dict["password"] = hash_password(patient_dict["password"])

    id = await db.patients.insert_one(patient_dict)
    id = id.inserted_id

    new_pacient = await db.patients.find_one({"_id": id})
    new_pacient["_id"] = str(new_pacient["_id"])

    return PatientResponse(**new_pacient)

# Endpoint de GET.
@router.get("/{id}", response_model=PatientResponse)
async def get_patient(id: str):
    patient = await search_patient("_id", ObjectId(id))

    if patient is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Paciente no encontrado.")
    return PatientResponse(**patient)

# Endpoint de PUT.
@router.put("/{id}", response_model=PatientResponse)
async def update_patient(id: str, patient: Patient):

    patient_dict = patient.model_dump()
    del patient_dict["id"]

    patient = await search_patient("_id", ObjectId(id))

    if patient is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail="El paciente no existe")
    else:
        update_patient = await db.patients.find_one_and_replace({"_id": ObjectId(id)}, patient_dict, return_document=True)

    update_patient["_id"] = str(update_patient["_id"])

    return PatientResponse(**update_patient)