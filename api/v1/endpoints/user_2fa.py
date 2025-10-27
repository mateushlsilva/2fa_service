from fastapi import APIRouter, Depends, Response, Query
from core.deps import get_db
from services.User_service import UserService

router = APIRouter(prefix="/2fa", tags=["2FA"])

@router.post("/setup")
async def setup_2fa(username: str, enterprise: str, response: Response, db=Depends(get_db)):
    service = UserService(db)
    data = await service.register_user(username, enterprise)

    response.headers["Content-Type"] = data["media_type"]
    return Response(content=data["qrcode"], media_type=data["media_type"])

@router.get("/verify")
async def verify_2fa(username: str = Query(...), code: str = Query(...), db=Depends(get_db)):
    service = UserService(db)
    return await service.verify_2fa(username, code)