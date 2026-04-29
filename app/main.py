# Importaciones.
from fastapi import FastAPI
from database import client, db
from contextlib import asynccontextmanager

# Ciclo de vida de la conexión de FastAPI.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lo que está antes del yield se ejecuta al arrancar.
    print("Conectandose a MongoDB...")
    yield
    # Lo que esta después del yield se ejecuta al apagar.
    print("Cerrando la conexión de MongoDB...")
    client.close()

# Creando la instancia de la aplicación.
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return "¡Hola FastAPI!"