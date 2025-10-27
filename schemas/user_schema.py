from pydantic import BaseModel, Field
from datetime import datetime


class UserCreate(BaseModel):
    username: str

class UserOut(BaseModel):
    id: str = Field(alias="_id")
    username: str
    secret: str
    created_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
