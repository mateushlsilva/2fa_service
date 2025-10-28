import pyotp
import qrcode
import io
import secrets
import hashlib
from config import settings

class Security:

    def generate_2fa(self, username, enterprisename=settings.ENTERPRISE):
        """
        Gera um secret e uma URI compatível com Google Authenticator.
        """
        secret = pyotp.random_base32()
        otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=username,
            issuer_name=enterprisename
        )

        return {"secret": secret, "otp_uri": otp_uri}

    def generate_qrcode(self, username, enterprisename=settings.ENTERPRISE):
        data = self.generate_2fa(username, enterprisename)
        otp_uri = data["otp_uri"]

        qr = qrcode.make(otp_uri)
        buf = io.BytesIO()
        qr.save(buf, format='PNG')
        buf.seek(0)

        return {"qrcode": buf.getvalue(), "media_type": "image/png", "secret": data["secret"]}
    

    def generate_recovery_codes(self, n=5):
        codes = [secrets.token_hex(8) for _ in range(n)] 
        hashed_codes = [hashlib.sha256(code.encode()).hexdigest() for code in codes]
        return {"codes": codes, "hashed_codes": hashed_codes}