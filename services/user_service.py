from models.user_model import UserModel
from core.Security import Security
from db.Crud import Crud

class UserService:
    def __init__(self):
        self.crud = Crud()
        self.security = Security()

    async def register_user(self, username: str, enterprise: str):
        # Gera QR e secret
        data = self.security.generate_qrcode(username, enterprise)
        user = UserModel(username=username, secret=data["secret"])
        await self.crud.create(user)
        return {"qrcode": data["qrcode"], "media_type": data["media_type"]}

    async def verify_2fa(self, username: str, code: str):
        user = await self.crud.get_by_username(username)
        if not user:
            return {"status": "not_found"}

        from pyotp import TOTP
        totp = TOTP(user["secret"])
        if totp.verify(code):
            return {"status": "success"}
        return {"status": "failed"}