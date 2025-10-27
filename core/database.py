from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from fastapi import FastAPI
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = AsyncIOMotorClient(settings.DATABASE_URL)
    print("✅ MongoDB conectado")
    yield
    app.mongodb_client.close()
    print("❌ MongoDB desconectado")
