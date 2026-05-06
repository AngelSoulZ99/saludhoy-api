# Importaciones.
from database import db
from bson import ObjectId

# Función para añadir los números de telefono a pacientes o medicos.
async def add_phone(collection: str, id: str, phone: str):

    await db[collection].update_one({"_id": ObjectId(id)}, {"$push": {"phones": phone}})