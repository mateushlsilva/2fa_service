from fastapi import APIRouter, Depends, Response, Query, Body
from fastapi.responses import JSONResponse
from core.deps import get_db
from services.User_service import UserService
import base64
from schemas.user_schema import UserCreate, RecoveryRequest

router = APIRouter(prefix="/2fa", tags=["2FA"])

@router.post("/setup")
async def setup_2fa(user: UserCreate = Body(...), db=Depends(get_db)):
    service = UserService(db)
    data = await service.register_user(user.identifier)
    # response.headers["Content-Type"] = data["media_type"]
    # return Response(content=data["qrcode"], media_type=data["media_type"])
    qrcode_base64 = base64.b64encode(data["qrcode"]).decode("utf-8")

    return JSONResponse(content={
        "qrcode": qrcode_base64,
        "media_type": data["media_type"],
        "recovery": data["recovery"]
    })


@router.get("/verify")
async def verify_2fa(identifier: str = Query(...), code: str = Query(...), db=Depends(get_db)):
    service = UserService(db)
    return await service.verify_2fa(identifier, code)


@router.patch("/recovery/generate")
async def regenerate_recovery(req: RecoveryRequest, db=Depends(get_db)):
    service = UserService(db)
    return await service.verify_recovery(req.identifier, req.code)
