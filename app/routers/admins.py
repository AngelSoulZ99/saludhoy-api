# Importaciones.
from fastapi import HTTPException, status, APIRouter, Depends
from models.admin import Admin
from models.admin_response import AdminResponse
from database import db
from core.security import hash_password
from bson import ObjectId

# Instancia para el router.
router = APIRouter(prefix="/admins",
                tags=["admins"],
                responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

# Función para realizar la búsqueda de un doctor.
async def search_admin(field: str, key):

    found_admin = await db.admins.find_one({field: key})

    if found_admin is None:
        return None
    
    found_admin["_id"] = str(found_admin["_id"])
    return found_admin

# Endpoint de POST.
@router.post("/", response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
async def create_admin(admin: Admin):

    if await search_admin("email", admin.email) is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail="El administrador ya existe.")

    admin_dict = admin.model_dump()
    del admin_dict["id"]
    admin_dict["password"] = hash_password(admin_dict["password"])

    id = await db.admins.insert_one(admin_dict)
    id = id.inserted_id

    new_admin = await db.admins.find_one({"_id": id})
    new_admin["_id"] = str(new_admin["_id"])

    return AdminResponse(**new_admin)

# Endpoint de GET.
@router.get("/{id}", response_model=AdminResponse)
async def get_admin(id: str):
    found_admin = await search_admin("_id", ObjectId(id))

    if found_admin is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Administrador no encontrado.")
    
    return AdminResponse(**found_admin)

# Endpoint de PUT.
@router.put("/{id}", response_model=AdminResponse)
async def update_admin(id: str, admin: Admin):

    admin_dict = admin.model_dump()
    del admin_dict["id"]

    admin = await search_admin("_id", ObjectId(id))

    if admin is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail="El administrador no existe.")
    
    else:
        admin_update = await db.admins.find_one_and_replace({"_id": ObjectId(id)}, admin_update, return_document=True)

    admin_update["_id"] = str(admin_update["_id"])

    return AdminResponse(**admin_update)