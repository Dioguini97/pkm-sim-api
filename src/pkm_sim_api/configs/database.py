from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

class Database:
    client = None

db = Database()
async def get_database():
    return db.client[settings.database_name]

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.mongodb_url)
    print("MONGODB_URL =", settings.mongodb_url)
    print("DATABASE_NAME =", settings.database_name)

    print("Conectado ao MongoDB!")

async def close_mongo_connection():
    db.client.close()
    print("Conexão ao MongoDB fechada!")