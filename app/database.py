# Importaciones de motor para realizar la conexión a MongoDB.
import motor.motor_asyncio
from config import MONGO_URI, DB_NAME

# Creación del cliente asíncrono.
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

# Base de datos.
db = client[DB_NAME]