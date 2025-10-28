from fastapi import HTTPException
from models.user_model import UserModel
from core.Security import Security
from db.Crud import Crud

class UserService:
    def __init__(self, db):
        self.db = db
        self.crud = Crud(db)
        self.security = Security()

    async def register_user(self, username: str):
        existing = await self.crud.get(username)
        if existing:
            raise HTTPException(status_code=400, detail="Usuário já existe")
        # Gera QR e secret
        data = self.security.generate_qrcode(username)
        recovery = self.security.generate_recovery_codes()
        user = UserModel(username=username, secret=data["secret"], hashed_codes=recovery['hashed_codes'])
        await self.crud.post(user)
        return {"qrcode": data["qrcode"], "media_type": data["media_type"], "recovery": recovery['codes']}

    async def verify_2fa(self, username: str, code: str):
        user = await self.crud.get(username)
        if not user:
            return {"status": "not_found"}

        from pyotp import TOTP
        totp = TOTP(user["secret"])
        if totp.verify(code):
            return {"status": "success"}
        return {"status": "failed"}