from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import lifespan

app = FastAPI(title="2FA Microservice", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

