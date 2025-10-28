from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from fastapi import FastAPI
from config import settings

database = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global database
    app.mongodb_client = AsyncIOMotorClient(settings.DATABASE_URL)
    app.db = app.mongodb_client.get_default_database()
    await app.db.users.create_index("username", unique=True)
    print("✅ MongoDB conectado")
    yield
    app.mongodb_client.close()
    print("❌ MongoDB desconectado")
