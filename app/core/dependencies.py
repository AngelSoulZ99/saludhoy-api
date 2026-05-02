from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.security import decode_access_token
from database import db
from bson import ObjectId

# Configuración del flujo OAuth2 para obtener el token.
oauth2 = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2)):
    token = decode_access_token(token)

    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                    "Credenciales invalidas.")

    if token["rol"] == "patient":
        user = await db.patient.find_one({"_id": ObjectId(token["sub"])})
    elif token["rol"] == "doctor":
        user= await db.doctor.find_one({"_id": ObjectId(token["sub"])})
    elif token["rol"] == "admin":
        user = await db.admin.find_one({"_id": ObjectId(token["sub"])})
    
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                    "Usuario no encontrado.")
    
    return user

def check_role(desired_role):
    async def verify(actual_user = Depends(get_current_user)):
        if actual_user["rol"] != desired_role:
            raise HTTPException(status.HTTP_403_FORBIDDEN, 
                                "No tiene permisos.")
        return actual_user
    return verify