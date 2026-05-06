# Importaciones.
from fastapi import HTTPException, status, APIRouter
from models.doctor import Doctor, DoctorStatusUpdate, PhoneUpdate
from models.doctor_response import DoctorResponse
from database import db
from core.security import hash_password
from bson import ObjectId
from services import phone_service

# Instancia para el router.
router = APIRouter(prefix="/doctors",
                tags=["doctors"],
                responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

# Función para realizar la búsqueda de un doctor.
async def search_doctor(field: str, key):

    doctor = await db.doctors.find_one({field: key})

    if doctor is None:
        return None
    
    doctor["_id"] = str(doctor["_id"])
    return doctor

# Endpoint de POST.
@router.post("/", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
async def create_doctor(doctor: Doctor):

    if await search_doctor("email", doctor.email) is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail="El doctor ya existe.")

    doctor_dict = doctor.model_dump()
    del doctor_dict["id"]
    doctor_dict["password"] = hash_password(doctor_dict["password"])

    id = await db.doctors.insert_one(doctor_dict)
    id = id.inserted_id

    new_doctor = await db.doctors.find_one({"_id": id})
    new_doctor["_id"] = str(new_doctor["_id"])

    return DoctorResponse(**new_doctor)

# Endpoint de GET.
@router.get("/{id}", response_model=DoctorResponse)
async def get_doctor(id: str):
    doctor = await search_doctor("_id", ObjectId(id))

    if doctor is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Doctor no encontrado.")
    
    return DoctorResponse(**doctor)

# Endpoint de PUT.
@router.put("/{id}", response_model=DoctorResponse)
async def update_doctor(id: str, doctor: Doctor):

    doctor_dict = doctor.model_dump()
    del doctor_dict["id"]

    doctor = await search_doctor("_id", ObjectId(id))

    if doctor is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail="El doctor no existe.")
    
    else:
        doctor_update = await db.doctors.find_one_and_replace({"_id": ObjectId(id)}, doctor_dict, return_document=True)

    doctor_update["_id"] = str(doctor_update["_id"])

    return DoctorResponse(**doctor_update)

@router.patch("/{id}", response_model=DoctorResponse)
async def update_state_doctor(id: str, new_status: DoctorStatusUpdate):

    doctor = await search_doctor("_id", ObjectId(id))

    if doctor is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail="El doctor no existe.")
    
    else:
        await db.doctors.update_one({"_id": ObjectId(id)}, {"$set": {"status": new_status.status}})

    update_status = await search_doctor("_id", ObjectId(id))

    return DoctorResponse(**update_status)

# Endpoint de PATCH de telefonos.
@router.patch("/phones/{id}", response_model=DoctorResponse)
async def add_phones_doctor(id:str, new_phone: PhoneUpdate):

    found_doctor = await search_doctor("_id", ObjectId(id))

    if found_doctor is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail="El doctor no existe.")
    
    else:
        await phone_service.add_phone("doctors", id, new_phone.phone)

    update_doctor = await search_doctor("_id", ObjectId(id))

    return DoctorResponse(**update_doctor)