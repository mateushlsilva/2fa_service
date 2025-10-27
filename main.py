from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import lifespan
from api.v1.endpoints.user_2fa import router as user

app = FastAPI(title="2FA Microservice", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user)