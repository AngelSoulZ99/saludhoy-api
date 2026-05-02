from fastapi import HTTPException, APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from core.security import verify_password, create_access_token
from database import db

# Definición del router.
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

async def get_user_by_email(verify_email):
    user = await db["patient"].find_one({"email": verify_email})

    if user is not None:
        return user
    
    user = await db["doctor"].find_one({"email": verify_email})
    
    if user is not None:
        return user
    
    user = await db["admin"].find_one({"email": verify_email})

    if user is not None:
        return user
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 
                            "Usuario no encontrado.")

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_email(form.username)

    if not user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 
                            "El email no es correcto.")

    if not verify_password(form.password, user["password"]):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 
                            "La contraseña no es correcta.")

    access_token = create_access_token(user["_id"], user["rol"])

    return {"access_token": access_token, "token_type": "bearer"}