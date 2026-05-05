# Importaciones.
from fastapi import APIRouter, status, HTTPException
from models.office import Office
from database import db
from bson import ObjectId

# Instacia para el router.
router = APIRouter(prefix="/offices",
                tags=["offices"],
                responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

# Función para realizar la búsqueda de un consultorio.
async def search_office(field: str, key):

    office_search = await db.offices.find_one({field: key})

    if office_search is None:
        return None

    office_search["_id"] = str(office_search["_id"])
    return office_search

# Función para realizar la búsqueda de una especialidad.
async def search_specialty(id: str):

    specialty_search = await db.specialties.find_one({"_id": ObjectId(id)})

    if specialty_search is None:
        return None
    
    return specialty_search

# Endpoint de POST.
@router.post("/", response_model=Office, status_code=status.HTTP_201_CREATED)
async def create_office(office: Office):

    for specialty_id in office.specialties:
        if await search_specialty(specialty_id) is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, 
                                detail=f"La especialidad {specialty_id} no existe.")
    
    if await search_office("name", office.name) is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 
                            detail="La oficina ya existe.")
    
    office_dict = office.model_dump()
    del office_dict["id"]

    id = await db.offices.insert_one(office_dict)
    id = id.inserted_id

    new_office = await db.offices.find_one({"_id": id})
    new_office["_id"] = str(new_office["_id"])
    
    return Office(**new_office)

# Endpoint de GET.
@router.get("/{id}", response_model=Office)
async def get_office(id: str):
    found_office = await search_office("_id", ObjectId(id))

    if found_office is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Oficina no encontrada.")
    
    return Office(**found_office)