from fastapi import HTTPException
from models.user_model import UserModel
from core.Security import Security
from db.Crud import Crud

class UserService:
    def __init__(self, db):
        self.db = db
        self.crud = Crud(db)
        self.security = Security()

    async def register_user(self, identifier: str):
        existing = await self.crud.get(identifier)
        if existing:
            raise HTTPException(status_code=400, detail="Usuário já existe")
        # Gera QR e secret
        data = self.security.generate_qrcode(identifier)
        recovery = self.security.generate_recovery_codes()
        user = UserModel(identifier=identifier, secret=data["secret"], hashed_codes=recovery['hashed_codes'])
        await self.crud.post(user)
        return {"qrcode": data["qrcode"], "media_type": data["media_type"], "recovery": recovery['codes']}

    async def verify_2fa(self, identifier: str, code: str):
        user = await self.crud.get(identifier)
        if not user:
            return {"status": "not_found"}

        from pyotp import TOTP
        totp = TOTP(user["secret"])
        if totp.verify(code):
            return {"status": "success"}
        return {"status": "failed"}
    
    async def verify_recovery(self, identifier: str, code_input: str):
        user = await self.crud.get(identifier)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário inixistente")
        verify = self.security.verify_recovery_code(user['hashed_codes'], code_input)
        if verify == None:
            raise HTTPException(status_code=404, detail="Código inixistente")
        user['hashed_codes'].remove(verify)
        await self.crud.put(identifier, user)
        return {"status": "success"}