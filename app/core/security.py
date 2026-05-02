from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from config import ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import jwt, JWTError
from fastapi import status, HTTPException

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para hashear la contraseña.
def hash_password(password):
    return crypt.hash(password)

# Función para verificar la contraseña.
def verify_password(password, hashed_password):
    return crypt.verify(password, hashed_password)

# Función para crear el token de acceso.
def create_access_token(user_id, role_user):

    access_token = {"sub": user_id,
                    "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
                    "rol": role_user}
    
    return jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM)

# Función para decodificar el token.
def decode_access_token(token):
    exception = HTTPException(status.HTTP_401_UNAUTHORIZED,
                            "Credenciales de autenticación invalidas",
                            {"WWW-Authenticate":"Bearer"})
    
    try:
        token_access = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return  token_access
    except JWTError:
        raise exception