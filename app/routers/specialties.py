# Importaciones.
from fastapi import HTTPException, status, APIRouter, Depends
from models.specialty import Specialty
from core.dependencies import check_role
from database import db
from bson import ObjectId

# Instancia para el router.
router = APIRouter(prefix="/specialties",
                tags=["specialties"],
                responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}},
                dependencies=[Depends(check_role("admin"))])

# Función para realizar la búsqueda de una especialidad.
async def search_specialty(field: str, key):

    specialty = await db.specialties.find_one({field: key})

    if specialty is None:
        return None
    
    specialty["_id"] = str(specialty["_id"])
    return specialty

# Endpoint de POST.
@router.post("/", response_model=Specialty)
async def create_specialty(specialty: Specialty):

    if await search_specialty("name", specialty.name) is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail="La especialidad ya existe.")
    
    specialty_dict = specialty.model_dump()
    del specialty_dict["id"]

    id = await db.specialties.insert_one(specialty_dict)
    id = id.inserted_id

    new_specialty = await db.specialties.find_one({"_id": id})
    new_specialty["_id"] = str(new_specialty["_id"])

    return Specialty(**new_specialty)

# Endpoint de GET.
@router.get("/{id}", response_model=Specialty)
async def get_specialty(id: str):
    
    specialty = await search_specialty("_id", ObjectId(id))

    if specialty is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="No se encontro la especialidad.")
    
    return Specialty(**specialty)

# Endpoint de PUT.
@router.put("/{id}", response_model=Specialty)
async def update_specialty(id: str, specialty: Specialty):

    specialty_dict = specialty.model_dump()
    del specialty_dict["id"]

    specialty = await search_specialty("_id", ObjectId(id))

    if specialty is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="La especialidad no existe.")
    
    else:
        specialty_update = await db.specialties.find_one_and_replace({"_id": ObjectId(id)}, specialty_dict, return_document=True)

    specialty_update["_id"] = str(specialty_update["_id"])

    return Specialty(**specialty_update)