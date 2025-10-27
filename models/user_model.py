from typing import Optional
from datetime import datetime


class UserModel:
    def __init__(self, username: str, secret: str, created_at: Optional[datetime] = None):
        self.username = username
        self.secret = secret
        self.created_at = created_at or datetime.now(datetime.timezone.utc)

    def to_dict(self):
        return {
            "username": self.username,
            "secret": self.secret,
            "created_at": self.created_at,
        }
