from typing import List
from pydantic import BaseModel, Field
from datetime import datetime


class UserCreate(BaseModel):
    identifier: str

class UserOut(BaseModel):
    id: str = Field(alias="_id")
    identifier: str
    secret: str
    hashed_codes: List[str]
    created_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class RecoveryRequest(BaseModel):
    identifier: str
    code: str