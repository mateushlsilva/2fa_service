import pyotp
import qrcode
import io

class Security:

    def generate_2fa(self, username, enterprisename):
        """
        Gera um secret e uma URI compatível com Google Authenticator.
        """
        secret = pyotp.random_base32()
        otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=username,
            issuer_name=enterprisename
        )

        return {"secret": secret, "otp_uri": otp_uri}

    def generate_qrcode(self, username, enterprisename):
        data = self.generate_2fa(username, enterprisename)
        otp_uri = data["otp_uri"]

        qr = qrcode.make(otp_uri)
        buf = io.BytesIO()
        qr.save(buf, format='PNG')
        buf.seek(0)

        return {"content": buf.getvalue(), "media_type": "image/png", "secret": data["secret"]}