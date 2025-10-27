import pyotp
import qrcode
import io

class Security:

    def generate_2fa(self, username, enterprisename):
        secret = pyotp.random_base32()
        otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=username,
            issuer_name=enterprisename
        )

        return otp_uri

    def generate_qrcode(self, username, enterprisename):
        otp_uri = self.generate_2fa(username, enterprisename)

        qr = qrcode.make(otp_uri)
        buf = io.BytesIO()
        qr.save(buf, format='PNG')
        buf.seek(0)

        return {"content": buf.getvalue(), "media_type": "image/png"}